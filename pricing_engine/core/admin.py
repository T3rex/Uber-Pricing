from django.contrib import admin
from .forms import DAPForm,DBPForm,TMFForm,WCForm
from .models import PricingModule,DistanceBasePrice, DistanceAdditionalPrice,TimeMultiplierFactor,WaitingCharges

# Register your models here.

admin.site.register(PricingModule)


@admin.register(DistanceBasePrice)
class DBPAdmin(admin.ModelAdmin):
    form =DBPForm
    list_display = ['day_of_week', 'base_distance', 'base_price', 'is_active', 'pricing_module','created_at']

@admin.register(DistanceAdditionalPrice)
class DAPAdmin(admin.ModelAdmin):
    form = DAPForm
    list_display = ['day_of_week', 'start_km', 'end_km', 'price_per_km', 'is_active', 'pricing_module','created_at']

@admin.register(TimeMultiplierFactor)
class TMFAdmin(admin.ModelAdmin):
    form = TMFForm
    list_display = ['day_of_week', 'start_minute', 'end_minute', 'multiplier', 'is_active', 'pricing_module','created_at']

@admin.register(WaitingCharges)
class WCAdmin(admin.ModelAdmin):
    form =WCForm
    list_display = ['day_of_week', 'price_per_unit', 'cycle_minutes', 'is_active', 'pricing_module','created_at']


