from contextlib import nullcontext
from itertools import product
from django.db import models
from django.contrib.auth.models import User
import datetime
import os

# Create your models here.

STATE_CHOICES =(
('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chandigarh','Chandigarh' ),
('Chattisgarh','Chattisgarh'),
('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
('Daman and Diu','Daman and Diu'),
('Delhi','Delhi'),
('Goa','Goa'),
('Gujrat','Gujrat'),
('Haryana','Haryana') ,
('Himachal Pradesh','Himachal Pradesh') ,
('Jammu & Kashmir','Jammu & Kashmir'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Lakshadweep','Lakshadweep'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra') ,
('Manipur','Manipur'),
('Meghalaya','Meghalaya') ,
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisa','Odisa'),
('Puducherry','Puducherry'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamilnadu','Tamilnadu'),
('Telangana','Telangana') ,
('Tripura','Tripura') ,
('Uttarakhand','Uttarakhand'),
('Uttar Pradesh','Uttar Pradesh'),
('West Bengal','West Bengal'),
)

def getFileName(requset,filename):
  now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
  new_filename="%s%s"%(now_time,filename)
  return os.path.join('uploads/',new_filename)
 
class Catagory(models.Model):
  name=models.CharField(max_length=150,null=False,blank=False)
  image=models.ImageField(upload_to=getFileName,null=True,blank=True)
  description=models.TextField(max_length=500,null=False,blank=False)
  status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
  created_at=models.DateTimeField(auto_now_add=True)
 
  def __str__(self) :
    return self.name
 
class Product(models.Model):
  category=models.ForeignKey(Catagory,on_delete=models.CASCADE)
  name=models.CharField(max_length=150,null=False,blank=False)
  vendor=models.CharField(max_length=150,null=False,blank=False)
  product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
  quantity=models.IntegerField(null=False,blank=False)
  original_price=models.FloatField(null=False,blank=False)
  selling_price=models.FloatField(null=False,blank=False)
  description=models.TextField(max_length=500,null=False,blank=False)
  status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
  trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
  created_at=models.DateTimeField(auto_now_add=True)
 
  def __str__(self) :
    return self.name
 
class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)
 
  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price
 
class Favourite(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
        
class Address(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    district = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    address_type = models.CharField(max_length=10, choices=[('home', 'Home'), ('work', 'Work')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    def __str__(self):
      return f"{self.first_name} {self.last_name}"

STATUS_CHOICES = (
   ('Accepted','Accepted'),
   ('Packed','Packed'),
   ('On the Way','On the Way'),
   ('Delivered','Delivered'),
   ('Cancel','Cancel'),
   ('Pending','Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=255,blank=True,null=True)
    payment_status = models.CharField(max_length=20,blank=True,null=True)
    payment_id = models.CharField(max_length=255,blank=True,null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_status}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.ordered_date}"
    