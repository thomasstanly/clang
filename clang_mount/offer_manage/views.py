from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CategoryOffer,BrandOffer
from .forms import categoryOfferform,brandOfferform
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView,CreateView,FormView


class Category_Offer(ListView,FormView):
    model = CategoryOffer
    template_name = 'cus_admin/page-category-offer.html'
    form_class = categoryOfferform
    success_url = reverse_lazy('offer_app:category_offer')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categoryoffers"] = CategoryOffer.objects.filter(is_active=True)
        return context
    
class Category_Offer_Create(CreateView):
    model = CategoryOffer
    template_name = 'cus_admin/page-category-offer.html'
    form_class = categoryOfferform
    success_url = reverse_lazy('offer_app:category_offer')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Category Offer Added")
        return super().form_valid(form)

class Category_Offer_Update(UpdateView):
    model = CategoryOffer
    template_name = 'cus_admin/page-category-offer.html'
    form_class = categoryOfferform
    success_url = reverse_lazy('offer_app:category_offer')

    def form_valid(self, form):
        messages.success(self.request,"Category Offer Updated")
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category_offer_id'] = self.kwargs['pk']
        context["categoryoffers"] = CategoryOffer.objects.filter(is_active=True)
        return context
    
class Category_Offer_Delete(DeleteView):
    model = CategoryOffer
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('offer_app:category_offer')



class Brand_Offer(ListView,FormView):
    model = BrandOffer
    template_name = 'cus_admin/page-brand-offer.html'
    form_class = brandOfferform
    success_url = reverse_lazy('offer_app:brand_offer')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["brandoffers"] = BrandOffer.objects.filter(is_active=True)
        return context
    
class Brand_Offer_Create(CreateView):
    model = BrandOffer
    template_name = 'cus_admin/page-brand-offer.html'
    form_class = brandOfferform
    success_url = reverse_lazy('offer_app:brand_offer')

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Brand Offer Added")
        return super().form_valid(form)

class Brand_Offer_Update(UpdateView):
    model = BrandOffer
    template_name = 'cus_admin/page-brand-offer.html'
    form_class = brandOfferform
    success_url = reverse_lazy('offer_app:brand_offer')

    def form_valid(self,form):
        messages.success(self.request,"Brand Offer Updated")
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_offer_id'] = self.kwargs['pk']
        context["brandoffers"] = BrandOffer.objects.filter(is_active=True)
        return context

class Brand_Offer_Delete(DeleteView):
    model = BrandOffer
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('offer_app:brand_offer')