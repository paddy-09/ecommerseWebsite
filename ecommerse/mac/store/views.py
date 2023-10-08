from django.shortcuts import render

from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

import razorpay
from django.conf import settings

# cart={
#     'i' :{'quantity': 1}
# } 
# Create your views here
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
       
    products = Product.objects.all()
    context={'products':products, 'cartItems': cartItems}
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context={'items':items, 'order':order,'cartItems': cartItems} #these are the parameters we render
    return render(request,'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    x = (order.get_cart_total)*100
    client = razorpay.Client(auth = (settings.KEY , settings.SECRET))
    payment = client.order.create({'amount' : int(x) , 'currency' : 'INR', 'payment_capture':1})
    order.razor_pay_order_id = payment['id']
    order.save()
    print('*********')
    print(payment)
    print('*********')
    context={'items':items, 'order':order,'cartItems': cartItems, 'payment': payment} #these are the parameters we render
    return render(request,'store/checkout.html',context)

def updateItem(request):
    print(request.body)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('productId:', productId)

    customer= request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer= customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order, product = product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer= customer,complete=False)
    else:
        customer , order = guestOrder(request,data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete=True
        order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['address'],
                state= data['shipping']['address'],
                zipcode=data['shipping']['address']
            )

    return JsonResponse('Payment submitted...', safe = False)