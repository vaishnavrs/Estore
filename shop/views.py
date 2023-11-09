from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Products,Category
from django.core.paginator import Paginator,EmptyPage,InvalidPage


# Create your views here.
def allProdCat(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list =Products.objects.all().filter(category=c_page,available=True)
    else:
        products_list=Products.objects.all().filter(available=True)
    paginator=Paginator(products_list,6)
    try:
        page_num=int(request.GET.get('page','1'))
    except:
        page_num=1
    try:
        products=paginator.page(page_num)
    except(EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)

    
    return render(request,'category.html',{'category':c_page,'products':products})

def ProductDetail(request,c_slug,product_slug):
    try:
        product=Products.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,"Product.html",{"products":product})