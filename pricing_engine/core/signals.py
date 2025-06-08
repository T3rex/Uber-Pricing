from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import (
    PricingModule, DistanceBasePrice, DistanceAdditionalPrice,
    TimeMultiplierFactor, WaitingCharges
)

@receiver(post_migrate)
def create_initial_pricing_configs(sender, **kwargs):
    if sender.name != 'core':
        return

    if not PricingModule.objects.exists():
        pm = PricingModule.objects.create(name="Default Module", is_active=True)
        print("✔️ Default PricingModule created")

        # DBP
        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Monday",
            base_price=80,
            base_distance=3,
            is_active=True
        )
        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Tuesday",
            base_price=60,
            base_distance=3,
            is_active=True
        )
        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Wednesday",
            base_price=50,
            base_distance=3,
            is_active=True
        )
        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Thursday",
            base_price=50,
            base_distance=3,
            is_active=True
        )
        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Friday",
            base_price=70,
            base_distance=3,
            is_active=True
        )
        print("✔️ DBPs created")

        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Saturday",
            base_price=90,
            base_distance=3,
            is_active=True
        )
        DistanceBasePrice.objects.create(
            pricing_module=pm,
            day_of_week="Sunday",
            base_price=100,
            base_distance=3,
            is_active=True
        )
        print("✔️ DBPs created")

        # DAP
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Monday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Monday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Tuesday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Tuesday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )

        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Wednesday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Wednesday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )

        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Thursday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Thursday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )

        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Friday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Friday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )

        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Saturday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Saturday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )

        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Sunday",
            start_km=0,
            end_km=10,
            price_per_km=30,
            is_active=True
        )      
        DistanceAdditionalPrice.objects.create(
            pricing_module=pm,
            day_of_week="Sunday",
            start_km=10,
            end_km=30,
            price_per_km=35,
            is_active=True
        )
        
        print("✔️ DAP slabs created")

        # TMF
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Monday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Monday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )

        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Tuesday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Tuesday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )

        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Wednesday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Wednesday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )

        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Thursday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Thursday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )

        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Friday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Friday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )

        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Saturday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Saturday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )

        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Sunday",
            start_minute=0,
            end_minute=30,
            multiplier=1.0,
            is_active=True
        )
        TimeMultiplierFactor.objects.create(
            pricing_module=pm,
            day_of_week="Sunday",
            start_minute=30,
            end_minute=60,
            multiplier=1.25,
            is_active=True
        )
        print("✔️ TMF slabs created")

        # WC
        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Monday",
            price_per_unit=5,
            cycle_minutes=3
        )

        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Tuesday",
            price_per_unit=5,
            cycle_minutes=3
        )

        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Wednesday",
            price_per_unit=5,
            cycle_minutes=3
        )

        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Thursday",
            price_per_unit=5,
            cycle_minutes=3
        )


        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Friday",
            price_per_unit=5,
            cycle_minutes=3
        )


        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Saturday",
            price_per_unit=5,
            cycle_minutes=3
        )

        WaitingCharges.objects.create(
            pricing_module=pm,
            day_of_week="Sunday",
            price_per_unit=5,
            cycle_minutes=3
        )
        print("✔️ WC config created")
