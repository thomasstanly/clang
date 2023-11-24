from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from admin_side.models import User
from .models import Address

class profileForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for filed_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','date_of_birth','phone','email']
        exclude = ['id','password', 'is_staff', 'is_superuser', 'is_active', 'joined_on','user_name','last_login']
        widgets = {
            'date_of_birth':forms.widgets.DateInput(attrs={'type':'date','placeholder': 'YYYY-MM-DD'})
        }

class AddressForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name,filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['user']

class PasswordForm(PasswordChangeForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for filed_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'
    
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
