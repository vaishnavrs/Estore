from django.shortcuts import render
from shop.models import Products
from django.db.models import Q
# Create your views here.

def search_result(request):
    products=None
    query=None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Products.objects.filter(Q(name__contains=query)|Q(description__contains=query))
        return render(request,"search.html",{'products':products,'query':query})

    