from django import forms
from .models import Brand, Product, Product_varient,product_image,attribute,attribute_values
from django.core.exceptions import ValidationError
from django.contrib import messages



class brand_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

    class Meta:
        model = Brand
        fields = '__all__'

class attribute_form(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

    class Meta:
        model = attribute
        fields = '__all__'

class attribute_value_form(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

    class Meta:
        model = attribute_values
        fields = '__all__'
        exclude = ['attr_is_active']
        


class product_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_slug','is_active']



class Product_varient_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'

    class Meta:
        model = Product_varient
        fields = '__all__'
        exclude = ['vari_is_active','attribute_name', 'varient_slug']
        widgets = {
            'discount_percentage': forms.TextInput(attrs={'min': 0, 'max': 100}),
            'description': forms.Textarea(),
        }
    
    def clean_discount_percentage(self):                                # cleanning method syntax clean_<name of the field>
        discount_percentage = self.cleaned_data['discount_percentage']
        if not (0 <= discount_percentage <= 100):
            raise ValidationError("Dis. percentage between 0 - 100.")
        return discount_percentage
