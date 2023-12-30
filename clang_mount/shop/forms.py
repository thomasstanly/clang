from typing import Any
from django import forms

class PriceRangeFilterForm(forms.Form):
    min_price = forms.IntegerField(label='Min Price', required=False,widget=forms.NumberInput(attrs={'value':100}))
    max_price = forms.IntegerField(label='Max Price', required=False,widget=forms.NumberInput(attrs={'value':3000}))

    def clean(self):
        cleaned_data = super().clean()

        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price is not None and max_price is not None:
            if min_price > max_price:
               raise forms.ValidationError('Min Price must be less than or equal to Max Price')
            if min_price < 100:
                raise forms.ValidationError("Min value is 100")
        else:
            raise forms.ValidationError("dasds")

        return cleaned_data