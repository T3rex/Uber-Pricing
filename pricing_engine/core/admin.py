from django.contrib import admin
from .forms import DAPForm,DBPForm,TMFForm,WCForm,PMForm,RideForm
from .models import PricingModule,DistanceBasePrice, DistanceAdditionalPrice,TimeMultiplierFactor,WaitingCharges,Ride

# Register your models here.



@admin.register(DistanceBasePrice)
class DBPAdmin(admin.ModelAdmin):
    form =DBPForm
    list_display = ['id','day_of_week', 'base_distance', 'base_price', 'is_active', 'pricing_module','created_at','created_by','updated_by']
    readonly_fields = ('created_by', 'updated_by')  

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DistanceAdditionalPrice)
class DAPAdmin(admin.ModelAdmin):
    form = DAPForm
    
    list_display = ['id','day_of_week', 'start_km', 'end_km', 'price_per_km', 'is_active', 'pricing_module','created_at','created_by','updated_by']   
    readonly_fields = ('created_by', 'updated_by')  

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(TimeMultiplierFactor)
class TMFAdmin(admin.ModelAdmin):
    form = TMFForm
    list_display = ['id','day_of_week', 'start_minute', 'end_minute', 'multiplier', 'is_active', 'pricing_module','created_at','created_by','updated_by']
    readonly_fields = ('created_by', 'updated_by')  

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(WaitingCharges)
class WCAdmin(admin.ModelAdmin):
    form =WCForm
    list_display = ['id','day_of_week', 'price_per_unit', 'cycle_minutes', 'is_active', 'pricing_module','created_at','created_by','updated_by']
    readonly_fields = ('created_by', 'updated_by')  

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PricingModule)
class PricingModuleAdmin(admin.ModelAdmin):
    form =PMForm
    list_display = ['id','name', 'is_active','created_at','created_by','updated_by']
    readonly_fields = ('created_by', 'updated_by')  

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Ride)
class PricingModuleAdmin(admin.ModelAdmin):
    form =RideForm
    list_display = ['id','start_time', 'end_time','waiting_time_minutes','total_distance','calculated_price','pricing_module','created_at','created_by','updated_by']
    readonly_fields = list_display 

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
