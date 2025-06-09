from django.contrib import admin
from core.utils.logger import log_pricing_config_change
from .forms import DAPForm,DBPForm,TMFForm,WCForm,PMForm,RideFormAdmin
from .models import PricingModule,DistanceBasePrice, DistanceAdditionalPrice
from .models import PricingConfigChangeLog,TimeMultiplierFactor,WaitingCharges,Ride
# Register your models here.



@admin.register(DistanceBasePrice)
class DBPAdmin(admin.ModelAdmin):
    form = DBPForm
    list_display = ['id', 'day_of_week', 'base_distance', 'base_price', 'is_active', 'pricing_module', 'created_at', 'created_by', 'updated_by']
    readonly_fields = ('created_by', 'updated_by')  

    def save_model(self, request, obj, form, change):
        # Set user fields
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user

        super().save_model(request, obj, form, change)

        # Log the action
        action = 'UPDATE' if change else 'CREATE'
        summary = f"Base price: {obj.base_price}, Base distance: {obj.base_distance}, Day: {obj.day_of_week}"
        log_pricing_config_change(obj, action=action, user=request.user, summary=summary)

    def delete_model(self, request, obj):
        summary = f"Deleted base price config for {obj.day_of_week} (Base price: {obj.base_price})"
        log_pricing_config_change(obj, action='DELETE', user=request.user, summary=summary)
        super().delete_model(request, obj)


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

        action= 'UPDATE' if change else 'CREATE'
        summary = f"Start km: {obj.start_km}, End KM: {obj.end_km}, Day: {obj.day_of_week},Price per km :{obj.price_per_km}, Is Active:{obj.is_active}"
        log_pricing_config_change(obj,action=action,user=request.user,summary=summary)
    
    def delete_model(self, request, obj):
        summary = f"Deleted Distance Additional Price config for {obj.day_of_week} (Base price: {obj.price_per_km} and slab [{obj.start_km}-{obj.end_km}])"
        log_pricing_config_change(obj, action='DELETE', user=request.user, summary=summary)
        super().delete_model(request, obj)


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

        action= 'UPDATE' if change else 'CREATE'
        summary = f"Start minute: {obj.start_minute}, End minute: {obj.end_minute}, Day: {obj.day_of_week},Multiplier :{obj.multiplier}, Is Active:{obj.is_active}"
        log_pricing_config_change(obj,action=action,user=request.user,summary=summary)
    
    def delete_model(self, request, obj):
        summary = f"Deleted Time Multiplier Factor config for {obj.day_of_week} (Multiplier: {obj.multiplier} and slab [{obj.start_minute}-{obj.end_minute}])"
        log_pricing_config_change(obj, action='DELETE', user=request.user, summary=summary)
        super().delete_model(request, obj)

        

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

        action= 'UPDATE' if change else 'CREATE'
        summary = f"Day: {obj.day_of_week}, Price per unit: {obj.price_per_unit}, Cycle minutes: {obj.cycle_minutes}, Is Active:{obj.is_active}"
        log_pricing_config_change(obj,action=action,user=request.user,summary=summary)

    def delete_model(self, request, obj):
        summary = f"Deleted Waiting Charges config for {obj.day_of_week} (Price per unit: {obj.price_per_unit} and cycle minutes: {obj.cycle_minutes})"
        log_pricing_config_change(obj, action='DELETE', user=request.user, summary=summary)
        super().delete_model(request, obj)    


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

        action= 'UPDATE' if change else 'CREATE'
        summary = f"Name: {obj.name}, Is Active: {obj.is_active}"
        log_pricing_config_change(obj,action=action,user=request.user,summary=summary)

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    form =RideFormAdmin
    list_display = ['id','start_time', 'end_time','waiting_time_minutes','total_distance','dap_ride','dbp_ride','tmf_ride','wc_ride','total_price','pricing_module','created_at','created_by','updated_by']
    readonly_fields = list_display 

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)




@admin.register(PricingConfigChangeLog)
class PricingConfigChangeLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'action', 'changed_by', 'timestamp')
    readonly_fields = ('model_name', 'object_id', 'action', 'changed_by', 'timestamp', 'change_summary')
    list_filter = ('model_name', 'action', 'changed_by')

