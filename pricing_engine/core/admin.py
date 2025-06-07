from django.contrib import admin
from .forms import DAPForm,DBPForm
from .models import PricingModule,DistanceBasePrice, DistanceAdditionalPrice,TimeMultiplierFactor,WaitingCharges

# Register your models here.

admin.site.register(PricingModule)
admin.site.register(TimeMultiplierFactor)
admin.site.register(WaitingCharges)


@admin.register(DistanceBasePrice)
class DBPAdmin(admin.ModelAdmin):
    form =DBPForm
    list_display = ['day_of_week', 'base_distance', 'base_price', 'is_active', 'pricing_module','created_at']

@admin.register(DistanceAdditionalPrice)
class DAPAdmin(admin.ModelAdmin):
    form = DAPForm
    list_display = ['day_of_week', 'start_km', 'end_km', 'price_per_km', 'is_active', 'pricing_module','created_at']



