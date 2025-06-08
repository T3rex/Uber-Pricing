from core.models import PricingConfigChangeLog

def log_pricing_config_change(instance, action, user=None, summary=""):
    model_name = instance.__class__.__name__
    PricingConfigChangeLog.objects.create(
        model_name=model_name,
        object_id=instance.pk or 0,
        action=action,
        changed_by=user,
        change_summary=summary
    )