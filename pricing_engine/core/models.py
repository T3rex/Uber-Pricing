from django.db import models
from django.contrib.auth import get_user_model
from .services.pricing_service import PricingService


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
    dap_ride = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dbp_ride = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tmf_ride = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wc_ride = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    
    total_distance = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="ride_created", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="ride_updated", on_delete=models.SET_NULL)

    def __str__(self):
        return f"Ride #{self.id} - {self.start_time.date()} - ₹{self.total_price}"

    def calculate_price(self):
        [dap, dbp, tmf, wc] = PricingService.calculate_price(self)
        self.dap_ride = dap
        self.dbp_ride = dbp
        self.tmf_ride = tmf
        self.wc_ride = wc
        self.total_price = dap + dbp + tmf + wc
        self.save()

        
class PricingConfigChangeLog(models.Model):
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=[('CREATE', 'CREATE'), ('UPDATE', 'UPDATE'), ('DELETE', 'DELETE')])
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    change_summary = models.TextField(blank=True, help_text="Describe what was changed.")

    def __str__(self):
        return f"{self.model_name} {self.action} by {self.changed_by} at {self.timestamp}"

        
            



        
