import uuid
from app1.models import Cart,Product
from django.db.models import Sum 
def cart_id(request):
    if 'cart_id' not in request.session:
        request.session['cart_id']=str(uuid.uuid4())
    return request.session['cart_id']
def get_cart(request):
    return Cart.objects.filter(cart_id=cart_id(request))
def add_to_cart(request):
    quantity_id=request.form_data['product_id'] #accessing product_id from form
    quantity=request.form_data['quantity'] #accessing quantity from form

    p=Product.objects.get(id=quantity_id)
    c=get_cart(request)

    item=False #initialising cart item 
    for i in c: #if product exist ,update quantity
        if i.product_id==quantity_id:
            i.update_quantity(quantity)
            item=True

    if not item:
        ca=Cart(cart_id=cart_id(request),price=p.price,quantity=quantity,product_id=quantity_id)
        ca.save() #adding item manually
def item_count(request):
    return get_cart(request).aggregate(count=Sum('quantity'))
def total(request):
    items=get_cart(request)
    t=0
    for i in items:
        t+=i.total()
    return t