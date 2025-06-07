from django.contrib import admin
from .models import PricingModule,DistanceBasePrice, DistanceAdditionalPrice

# Register your models here.

admin.site.register(PricingModule)
admin.site.register(DistanceBasePrice)
admin.site.register(DistanceAdditionalPrice)

