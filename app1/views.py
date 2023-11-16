from django.shortcuts import render,redirect
from django.urls import path
from django.http import HttpResponse
from app1.models import Product,Cart,Buy
from app1.forms import CartForm
from app1.app1 import *
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm

def index(request):
    p=Product.objects.all() #to import all the objects from models
    if request.GET.get('s'):
        query=request.GET.get('s')
        p=Product.objects.filter(title=query)
    context={'p':p} #to import into templates
    return render(request,'index.html',context) 
def detail(request,product_id,slug):
    d=Product.objects.get(id=product_id)
    if request.method=="POST":
        f=CartForm(request,request.POST)
        if f.is_valid():
            request.form_data=f.cleaned_data
            add_to_cart(request)
            return redirect('app1:cart_view')
    f=CartForm(request,initial={'product_id':product_id})
    context={'d':d,'f':f}
    return render(request,'detail.html',context)
def cart_view(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        item_id=request.POST.get('item_id')
        cd=Cart.objects.get(id=item_id)
        cd.delete()
    c=get_cart(request)
    t=total(request)
    co=item_count(request)
    context={'c':c,'t':t}
    return render(request,'cart.html',context)
def order(request):

    # What you want the button to do.
    items=get_cart(request)
    for i in items:
        b=Buy(product_id=i.product_id,quantity=i.quantity,price=i.price)
        b.save()
    paypal_dict = {
        "business": "sb-ifrjl28146035@business.example.com",
        "amount": total(request),
        "item_name": cart_id(request),
        "invoice":str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('app1:return_view')),
        "cancel_return": request.build_absolute_uri(reverse('app1:cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,"items":items,"total":total(request)}
    return render(request, "order.html", context)
def return_view(request):
    return HttpResponse('Transaction successful')
def cancel_view(request):
    return HttpResponse('Transaction cancelled')
