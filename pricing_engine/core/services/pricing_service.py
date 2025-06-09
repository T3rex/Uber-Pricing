import calendar
from decimal import Decimal


class PricingService:

    @staticmethod
    def calculate_price(ride):
        from core.models import (
            DistanceBasePrice,
            DistanceAdditionalPrice,
            TimeMultiplierFactor,
            WaitingCharges
        )
        pricing_module = ride.pricing_module
        start_time = ride.start_time
        end_time = ride.end_time
        total_distance = ride.total_distance
        waiting_minutes = ride.waiting_time_minutes

        day_of_week = calendar.day_name[start_time.weekday()]

        # === DBP ===
        dbp_obj = DistanceBasePrice.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day_of_week,
            is_active=True
        ).first()
        dbp = Decimal('0.00')
        base_distance = dbp_obj.base_distance if dbp_obj else Decimal('0.00')
        base_price = dbp_obj.base_price if dbp_obj else Decimal('0.00')
        if total_distance > base_distance:
            dbp = base_price
        else:
            dbp = (total_distance / base_distance) * base_price if base_distance > 0 else Decimal('0.00')

        # === DAP ===
        additional_distance = max(Decimal('0.00'), total_distance - base_distance)
        dap = Decimal('0.00')
        if additional_distance>Decimal('0.00'):
            dap_slabs = DistanceAdditionalPrice.objects.filter(
                pricing_module=pricing_module,
                day_of_week=day_of_week,
                is_active=True
            ).order_by('start_km')
            
            remaining_dist = additional_distance
            for slab in dap_slabs:
                slab_range = slab.end_km - slab.start_km
                if remaining_dist > slab_range:
                    dap += slab_range * slab.price_per_km
                    remaining_dist -= slab_range
                else:
                    dap += remaining_dist * slab.price_per_km
                    remaining_dist = Decimal('0.00')
                    break

            if remaining_dist > 0 and dap_slabs.exists():
                dap += remaining_dist * dap_slabs.last().price_per_km

        # === TMF ===
        ride_minutes = int((end_time - start_time).total_seconds() / 60)
        tmf_slabs = TimeMultiplierFactor.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day_of_week,
            is_active=True
        ).order_by('start_minute')

        tmf = Decimal('0.00')
        remaining_minutes = ride_minutes
        for slab in tmf_slabs:
            slab_range = slab.end_minute - slab.start_minute
            if remaining_minutes > slab_range:
                tmf += slab_range * slab.multiplier
                remaining_minutes -= slab_range
            else:
                tmf += remaining_minutes * slab.multiplier
                remaining_minutes = 0
                break

        if remaining_minutes > 0 and tmf_slabs.exists():
            tmf += remaining_minutes * tmf_slabs.last().multiplier

        # === WC ===
        wc_obj = WaitingCharges.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day_of_week,
            is_active=True
        ).first()

        wc = Decimal('0.00')
        if wc_obj:
            units = Decimal(waiting_minutes) / Decimal(wc_obj.cycle_minutes)
            wc = wc_obj.price_per_unit * units

        return {"dap":dap,"dbp": dbp,"tmf": tmf,"wc": wc}
