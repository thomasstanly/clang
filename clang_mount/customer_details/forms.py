from django import forms
from .models import Profile_image

class ProfileImage(forms.ModelForm):
    def __init(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-class'

    class Meta:
        model = Profile_image
        fields = '__all__'
        exclude =['user']