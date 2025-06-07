from django.db import models

# Create your models here.

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
    is_Active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"{self.day_of_week}: ₹{self.price_per_unit} per {self.cycle_minutes} min"


class Ride(models.Model):
    pricing_module = models.ForeignKey(PricingModule,on_delete=models.PROTECT)
    start_time = models.DateField()
    end_time = models.DateField()
    waiting_time_minutes = models.PositiveIntegerField(default=0)
    total_distance = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ride #{self.id} - {self.start_time.date()} - ₹{self.calculated_price or 'Unbilled'}"