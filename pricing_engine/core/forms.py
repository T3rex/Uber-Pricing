from django import forms
from .models import DistanceBasePrice,DistanceAdditionalPrice,TimeMultiplierFactor,WaitingCharges, PricingModule,Ride



class PMForm(forms.ModelForm):
    class Meta:
        model = PricingModule
        fields = '__all__'

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pricing_module', 'start_time', 'end_time', 'waiting_time_minutes', 'total_distance']
        

class DBPForm(forms.ModelForm):
    class Meta:
        model = DistanceBasePrice
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        pricing_module = cleaned_data.get('pricing_module')
        day = cleaned_data.get('day_of_week')
        price = cleaned_data.get('base_price')
        distance = cleaned_data.get('base_distance')
        is_active = cleaned_data.get('is_active')
        current_id = self.instance.id

        #price must be positve
        if price is not None and price < 0:
            raise forms.ValidationError("Price must be positive",code="invalid")
        
        #distance must be positve
        if distance is not None and distance < 0:
            raise forms.ValidationError("Distance must be greater than or equal 0",code="invalid")

        #prevent DBP on same day and price module whether active or incactive
        duplicate = DistanceBasePrice.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day,           
        ).exclude(id=current_id)

        if duplicate.exists():
            raise forms.ValidationError(
                "DBP already exists for this day and pricing module.",
                code="invalid"
            )
        
        return cleaned_data


class DAPForm(forms.ModelForm):
    class Meta:
        model = DistanceAdditionalPrice
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        pricing_module = cleaned_data.get('pricing_module')
        day = cleaned_data.get('day_of_week')
        start_km = cleaned_data.get('start_km')
        end_km = cleaned_data.get('end_km')
        price = cleaned_data.get('price_per_km')
        current_id = self.instance.id

        #price must be positive
        if price is not None and price <= 0:
            raise forms.ValidationError("Price per KM must be greater than 0.", code="invalid")
        
        #price must be positive
        if start_km is not None and start_km < 0:
            raise forms.ValidationError("Start KM must be greater than equal to 0.", code="invalid")
        
        #price must be positive
        if end_km is not None and end_km <= 0:
            raise forms.ValidationError("ENd KM must be greater than 0.", code="invalid")
        
        #prevent duplicate slabs (same start & end)
        duplicate = DistanceAdditionalPrice.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day,
            start_km=start_km,
            end_km=end_km
        ).exclude(id=current_id)

        if duplicate.exists():
            raise forms.ValidationError("Duplicate DAP slab already exists.", code="invalid")

        #start must before end
        if start_km >= end_km:
            raise forms.ValidationError("Start KM must be less than End KM.", code="invalid")

        # Check for overlap
        overlapping = DistanceAdditionalPrice.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day,
        ).exclude(id=current_id).filter(
            start_km__lt=end_km,
            end_km__gt=start_km
        )

        if overlapping.exists():
            raise forms.ValidationError("Overlapping DAP slab found.", code="invalid")

        # Check for gaps
        slabs = list(
            DistanceAdditionalPrice.objects.filter(
                pricing_module=pricing_module,
                day_of_week=day
            ).exclude(id=current_id)
        )
        
        slabs.append(
            DistanceAdditionalPrice(
                pricing_module=pricing_module,
                day_of_week=day,
                start_km=start_km,
                end_km=end_km,
            )
        )
        slabs.sort(key=lambda s: s.start_km)

        expected_start = 0
        for slab in slabs:
            if slab.start_km != expected_start:
                if expected_start==0:
                    raise forms.ValidationError("First slab must start from 0",code="invalid")
                raise forms.ValidationError("Gap detected between slabs.", code="invalid")
            expected_start = slab.end_km

        return cleaned_data

class TMFForm(forms.ModelForm):
    class Meta:
        model = TimeMultiplierFactor
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        pricing_module = cleaned_data.get('pricing_module')
        day = cleaned_data.get('day_of_week')
        start_minute = cleaned_data.get('start_minute')
        end_minute = cleaned_data.get('end_minute')
        multiplier = cleaned_data.get('multiplier')
        current_id = self.instance.id

        # Validation checks
        if multiplier is not None and multiplier < 0:
            raise forms.ValidationError('Multiplier must be greater than or equal to 0')

        if start_minute is not None and start_minute < 0:
            raise forms.ValidationError('Start minute must be >= 0')

        if end_minute is not None and end_minute <= 0:
            raise forms.ValidationError('End minute must be > 0')

        if start_minute >= end_minute:
            raise forms.ValidationError('Start minute must be less than end minute')

        # Prevent duplicate slabs
        duplicate = TimeMultiplierFactor.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day,
            start_minute=start_minute,
            end_minute=end_minute
        ).exclude(id=current_id)

        if duplicate.exists():
            raise forms.ValidationError("Duplicate TMF slab already exists.", code="invalid")

        # Check for overlap
        overlapping = TimeMultiplierFactor.objects.filter(
            pricing_module=pricing_module,
            day_of_week=day,
        ).exclude(id=current_id).filter(
            start_minute__lt=end_minute,
            end_minute__gt=start_minute
        )

        if overlapping.exists():
            raise forms.ValidationError("Overlapping TMF slab found.", code="invalid")

        # Check for gaps
        slabs = list(
            TimeMultiplierFactor.objects.filter(
                pricing_module=pricing_module,
                day_of_week=day
            ).exclude(id=current_id)
        )

        slabs.append(
            TimeMultiplierFactor(
                pricing_module=pricing_module,
                day_of_week=day,
                start_minute=start_minute,
                end_minute=end_minute,
            )
        )
        slabs.sort(key=lambda s: s.start_minute)

        expected_start = 0
        for slab in slabs:
            if slab.start_minute != expected_start:
                if expected_start == 0:
                    raise forms.ValidationError("First slab must start from 0", code="invalid")
                raise forms.ValidationError("Gap detected between slabs.", code="invalid")
            expected_start = slab.end_minute

        return cleaned_data


class WCForm(forms.ModelForm):
    class Meta:
        model = WaitingCharges
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        pricing_module = cleaned_data.get('pricing_module')
        day = cleaned_data.get('day_of_week')
        price = cleaned_data.get('price_per_unit')
        unit = cleaned_data.get('cycle_minutes')
        current_id = self.instance.id

        #price must be greater than or equal to 0
        if price is not None and price<0:
            raise forms.ValidationError('Price per unit must be greater than or equal to 0',code='inavlid')
        
        #cycle_minutes must be greater than 0
        if unit is not None and unit<=0:
            raise forms.ValidationError('Cycle_minutes must be greater than 0',code='invalid')
        
        #prevent dulplicate
        duplicate = WaitingCharges.objects.filter(
            pricing_module=pricing_module,
            day_of_week= day
        ).exclude(id=current_id)

        if duplicate.exists():
            raise forms.ValidationError('Entry for this day and pricing module already exist',code='invalid')
        
        return cleaned_data
        
        
