from django import forms
from .models import Order

# class OrderStatusForm(forms.ModelForm):
#     def __init__(self,*args,**kwargs):
#          super().__init__(*args, **kwargs)
             
#     class Meta:
#         model = Order
#         fields = ['status']
#         widgets = {
#             'status': forms.Select(attrs={'class':'form-control'})
#         }