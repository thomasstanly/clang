from django import forms
from .models import Brand, Product, Product_varient,product_image,attribute,attribute_values



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
        exclude = ['is_active']
        


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
        exclude = ['is_active','attribute_name', 'varient_slug']

