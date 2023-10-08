from django.db import models

# Create your models here.
from django.contrib.auth.models import User #default user model

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,null=True, blank=True) #a customer can have one user and a user can have one customer
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    #this is the name with which we will see in the admin panel
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    
    #we wrote the bellow function, so that if anyone doesnt upload a image in the admin panel in the Product section they it will not give errorw
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)#many to one realtionship, a single customer can have more than one orders or multiple orders
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) #complete is false then it is a open cart i.e u can add items in it, if it is true that is a close cart
    transaction_id = models.CharField(max_length=100,null=True)
    razor_pay_order_id = models.CharField(max_length=100, null = True, blank = True)
    razor_pay_payment_id = models.CharField(max_length=100, null = True, blank = True)
    razor_pay_payment_signature = models.CharField(max_length=100, null = True, blank = True)

    def __str__(self):
        return str(self.id)
    
    @property #main item total amount
    def get_cart_total(self):
        orderitems  = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property #main item total items
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property 
    def shipping(self):
        shipping = False
        orderitems= self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping= True
        
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property #this propety is for if we add multiple object of same type, then to get the total amount of that 
    def get_total(self):
        total = self.product.price*self.quantity
        return total
    



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

