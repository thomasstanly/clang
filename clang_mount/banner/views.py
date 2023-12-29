from django.shortcuts import render
from django.views import View

class Banner(View):

    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request,'cus_Admin/page-banner.html')
