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
        


class product_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class'] = ''

    class Meta:
        model = Product
        fields = '__all__'



class Product_varient_form(forms.ModelForm):
    class Meta:
        model = Product_varient
        fields = '__all__'
        exclude = ['is_active', 'product_variant_slug', 'product']
        widgets = {
            'product': forms.RadioSelect,
            'model_id': forms.TextInput(attrs={'class': "form-control"}),
            'attributes': forms.CheckboxSelectMultiple,
            'sale_price': forms.TextInput(attrs={'class': "form-control"}),
            'stock': forms.TextInput(attrs={'class': "form-control"}),
            'thumbnail_image': forms.ClearableFileInput,
            'max_price': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
        }

class product_image_Form(forms.ModelForm):
    
    class Meta:
        model = product_image
        fields = "__all__"

