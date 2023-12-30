from django import forms
from .models import CategoryOffer,BrandOffer

class categoryOfferform(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, values in self.fields.items():
            values.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = CategoryOffer
        fields = '__all__'
        exclude = ['is_active']
        widgets = {
            'offer_expire_date': forms.DateInput(attrs={'type': 'date'}),
        }

class brandOfferform(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, values in self.fields.items():
            values.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = BrandOffer 
        fields = '__all__'
        exclude = ['is_active']
        widgets = {
            'offer_expire_date': forms.DateInput(attrs={'type': 'date'}),
        }