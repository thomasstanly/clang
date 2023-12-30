from typing import Any
from django import forms
from django.core.validators import MinValueValidator

class PriceRangeFilterForm(forms.Form):
    min_price = forms.IntegerField(label='Min Price', required=False,validators=[MinValueValidator(500, message='Min value is 500')])
    max_price = forms.IntegerField(label='Max Price', required=False)

    def clean(self):
        cleaned_data = super().clean()

        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price is not None and max_price is not None:
            if min_price > max_price:
               raise forms.ValidationError('Min Price must be less than or equal to Max Price', code='min_max_relation')
        else:
           raise forms.ValidationError('Please enter a value in both fields', code='empty_fields')

        return cleaned_data