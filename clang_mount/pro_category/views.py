from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Categories

# Create your views here.
def categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        categories = Categories.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cus_admin/page-categories.html',context)
    else:
         return redirect('admin_app:admin_login')
    
def add_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            category = request.POST['category']
            description = request.POST['description']
            image = request.FILES['image']
            try:
                if Categories.objects.get(category_title=category):
                    messages.warning(request,"category is taken")
                    return redirect('category_app:add_categories')
            except:
                pass
            categories = Categories(category_img=image,category_title=category,description=description)
            categories.save()
            return redirect('category_app:admin_categories')
        return render(request,'cus_admin/page-categories-add.html')
    else:
         return redirect('admin_app:admin_login')

def edit_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            category = Categories.objects.get(id=id)
            category_title = request.POST.get('category')
            description = request.POST.get('description')
            category_img = request.FILES.get('image')
            if category_title:
                category.category_title = category_title
            if description:
                category.description = description
            if category_img:
                category.category_img = category_img
            category.save()
            messages.success(request,"Category updated")
            return redirect('category_app:admin_categories')
            
        
        category = Categories.objects.get(id=id)
        context = {
            'category' : category
        }
        return render(request,'cus_admin/page-categories-edit.html',context)
    else:
        return redirect('admin_app:admin_login')

def delete_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Categories.objects.get(id=id)
        category.delete()
        return redirect('category_app:admin_categories')