import calendar
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class DayOfWeek(models.TextChoices):
    MONDAY = 'Monday', 'Monday'
    TUESDAY = 'Tuesday', 'Tuesday'
    WEDNESDAY = 'Wednesday', 'Wednesday'
    THURSDAY = 'Thursday', 'Thursday'
    FRIDAY = 'Friday', 'Friday'
    SATURDAY = 'Saturday', 'Saturday'
    SUNDAY = 'Sunday', 'Sunday'
class PricingModule(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="pm_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="pm_updated", on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
    def get_dap_for_day(self, day):
        return self.dap_entries.filter(day_of_week=day, is_active=True)

    
class DistanceBasePrice(models.Model):
    pricing_module = models.ForeignKey(PricingModule,on_delete=models.CASCADE,related_name='dbp_entries')
    day_of_week = models.CharField(max_length=10,choices=DayOfWeek.choices)
    base_price = models.DecimalField(max_digits=10,decimal_places=2)
    base_distance = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="dbp_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="dbp_updated", on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.day_of_week} - {self.base_price} for {self.base_distance} km as per {self.pricing_module} pricing module"
    
class DistanceAdditionalPrice(models.Model):
    pricing_module = models.ForeignKey(PricingModule, on_delete=models.CASCADE, related_name='dap_entries')
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_km = models.DecimalField(max_digits=5, decimal_places=2)
    end_km = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="dap_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="dap_updated", on_delete=models.SET_NULL)

    class Meta:
        ordering = ['start_km']  # slabs are processed in order

    def __str__(self):
        return f"{self.day_of_week}: {self.start_km}-{self.end_km} km @ {self.price_per_km}/km"


class TimeMultiplierFactor(models.Model):
    pricing_module = models.ForeignKey(PricingModule,on_delete=models.CASCADE,related_name="tmf_entries")
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_minute = models.PositiveIntegerField()
    end_minute = models.PositiveIntegerField()
    multiplier = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="tmf_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="tmf_updated", on_delete=models.SET_NULL)

    class Meta:
        ordering = ['start_minute']

    def __str__(self):
        return f"{self.day_of_week}: {self.start_minute}-{self.end_minute} min → x{self.multiplier}"
    
class WaitingCharges(models.Model):
    pricing_module = models.ForeignKey(PricingModule, on_delete=models.CASCADE, related_name='wc_entries')
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    cycle_minutes = models.PositiveIntegerField()  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="wc_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="wc_updated", on_delete=models.SET_NULL)
    

    def __str__(self):
        return f"{self.day_of_week}: ₹{self.price_per_unit} per {self.cycle_minutes} min"


class Ride(models.Model):
    pricing_module = models.ForeignKey(PricingModule, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    waiting_time_minutes = models.PositiveIntegerField(default=0)
    total_distance = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="ride_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="ride_updated", on_delete=models.SET_NULL)

    def __str__(self):
        return f"Ride #{self.id} - {self.start_time.date()} - ₹{self.calculated_price}"

    def calculate_price(self):
        day_index = self.start_time.weekday()  
        day_of_week = calendar.day_name[day_index]

        # === DBP Calculation ===
        dbp_object = DistanceBasePrice.objects.filter(
            pricing_module=self.pricing_module,
            day_of_week=day_of_week,
            is_active=True
        ).first()

        base_price = Decimal('0.00')
        base_distance = Decimal('0.00')

        if dbp_object:
            base_price = dbp_object.base_price
            base_distance = dbp_object.base_distance

        dbp = base_price  

        # === DAP Calculation ===
        additional_distance = max(Decimal('0.00'), self.total_distance - base_distance)
        dap_slabs = DistanceAdditionalPrice.objects.filter(
            pricing_module=self.pricing_module,
            day_of_week=day_of_week,
            is_active=True
        ).order_by('start_km')

        dap = Decimal('0.00')
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

        # === TMF Calculation ===
        ride_minutes = int((self.end_time - self.start_time).total_seconds() / 60)
        tmf_slabs = TimeMultiplierFactor.objects.filter(
            pricing_module=self.pricing_module,
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

        # === WC Calculation ===
        wc_object = WaitingCharges.objects.filter(
            pricing_module=self.pricing_module,
            day_of_week=day_of_week
        ).first()

        wc = Decimal('0.00')
        if wc_object:
            total_units = Decimal(self.waiting_time_minutes) / Decimal(wc_object.cycle_minutes)
            wc = wc_object.price_per_unit * total_units

        # === Final Price ===
        self.calculated_price = (dbp + dap) + tmf + wc

        



        
            



        
