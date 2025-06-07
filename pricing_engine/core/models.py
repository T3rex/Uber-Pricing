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
    
class DistanceBasePrice(models.Model):
    pricing_module = models.ForeignKey(PricingModule,on_delete=models.CASCADE,related_name='dbp_entries')
    day_of_week = models.CharField(max_length=10,choices=DayOfWeek.choices)
    base_price = models.DecimalField(max_digits=10,decimal_places=2)
    base_distance = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.day_of_week} - {self.base_price} for {self.base_distance} km"
    
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


