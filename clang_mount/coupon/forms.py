from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for filed, values in self.fields.items():
            values.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'description', 'dis_percentage', 'min_amount', 'expiry_date']
        exclude = ['is_active']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }