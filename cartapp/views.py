from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Products
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
def add_cart(request,product_id):
    product=Products.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity<cart_item.product.stock:
            cart_item.quantity+=1
        cart_item.save()
    except:
        cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
        cart_item.save()
    return redirect('cartapp:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart in cart_items:
            total+=(cart.product.price*cart.quantity)
            counter+=cart.quantity
    except ObjectDoesNotExist:
        pass
    context={'cart_items':cart_items,'total':total,'counter':counter}
    return render(request,"cart.html",context)

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Products,id=product_id)
    item=CartItem.objects.get(product=product,cart=cart)

    if item.quantity>1:
        item.quantity-=1
        item.save()
    else:
        item.delete()
    return redirect('cartapp:cart_detail')


def full_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Products,id=product_id)
    item=CartItem.objects.get(product=product,cart=cart)
    item.delete()
    return redirect('cartapp:cart_detail')