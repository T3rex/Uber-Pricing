from django.db import models

# Create your models here.
class PricingModule(models.Model):
    name = models.CharField(max_length=100)
    is_Active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

