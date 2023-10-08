import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}

    print('Cart:',cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False,' razor_pay_order_id': 0 ,'razor_pay_payment_id': 0, 'razor_pay_payment_signature': 0}
    cartItems = order['get_cart_items']

   
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id = i)
            total = (product.price*cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] +=cart[i]['quantity']

            item = {
                'product' : {
                    'id':product.id,
                    'name': product.name,
                    'price':product.price,
                    'imageURL': product.imageURL ,   
                },
                'quantity' : cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    #first we gonna see if the user is authenticated user or not(i.e if he is logged in or not)

    if request.user.is_authenticated:
        customer = request.user.customer #one to one relo
        order,created = Order.objects.get_or_create(customer= customer,complete=False)
        items=order.orderitem_set.all() #Queryset,how many diff items we have in the cart
        cartItems = order.get_cart_items
    else:#if the user is not logged in or authenticated toh it gives error cause order was not defined isliye error diya
        #items = []
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
        print('User is not logged in..')
        print('COOKIES:', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        cookieData = cookieCart(request)
        items = cookieData['items']

        customer,created = Customer.objects.get_or_create(
            email = email,
        )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer = customer,
            complete = False,
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity = item['quantity']
            )

        return customer,order