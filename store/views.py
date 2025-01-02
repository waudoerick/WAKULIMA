from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .models import *
from . utils import cookieCart, cartData, guestOrder
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .decorators import unauthenticated_user,allowed_users
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
@allowed_users(allowed_roles=['ADMIN'])
def thepdf(request):
    order = Order.objects.all()
    template = get_template('store/ordersreport.html')
    content = template.render({'order':order})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(content.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
@allowed_users(allowed_roles=['ADMIN'])
def topdf(request):
    delivery = DeliveryAddress.objects.all()
    template = get_template('store/report.html')
    content =template.render({'delivery':delivery})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(content.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
        
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request): 

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print ('Action:', action)
    print('productId:',productId)
     
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()  
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        
         
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        DeliveryAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['county'],
            
          
        )

    return JsonResponse('Payment complete!', safe=False)


