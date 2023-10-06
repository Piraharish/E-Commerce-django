from django.conf import settings
from django.http import  JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import razorpay
from shop.form import AddressForm, CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
 
 
def home(request):
  products=Product.objects.filter(trending=1)
  return render(request,"shop/index.html",{"products":products})
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_id = data['pid']
                product_status = Product.objects.filter(id=product_id).exists()
                if product_status:
                    if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                        return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
                    else:
                        Favourite.objects.create(user=request.user, product_id=product_id)
                        return JsonResponse({'status': 'Product Added to Favourite'}, status=200)
                else:
                    return JsonResponse({'status': 'Product not found'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
 
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
        data=json.load(request)
        product_qty=data['product_qty']
        product_id=data['pid']
        #print(request.user.id)
        product_status=Product.objects.get(id=product_id)
        if product_status:
          if Cart.objects.filter(user=request.user.id,product_id=product_id):
            return JsonResponse({'status':'Product Already in Cart'}, status=200)
          else:
            if product_status.quantity>=product_qty:
              Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
              return JsonResponse({'status':'Product Added to Cart'}, status=200)
            else:
              return JsonResponse({'status':'Product Stock Not Available'}, status=200)
      else:
        return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   
def update_cart_item_quantity(request, item_id, new_quantity):
    # Get the cart item
    cart_item = Cart.objects.get(pk=item_id)

    # Update the quantity
    cart_item.product_qty = new_quantity
    cart_item.save()

    return JsonResponse({'message': 'Quantity updated successfully'})
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})
 
def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":catagory})
 
def collectionsview(request,name):
  if(Catagory.objects.filter(name=name,status=0)):
      products=Product.objects.filter(category__name=name)
      return render(request,"shop/products/index.html",{"products":products,"category_name":name})
  else:
    messages.warning(request,"No Such Catagory Found")
    return redirect('collections')
 
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"shop/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')
    
def product_detail(request, cname, pname):
    product = get_object_or_404(Product, category__name=cname, name=pname)
    return render(request, 'shop/products/product_details.html', {'products': product})

def address(request):
    return render(request, "shop/address.html")

def orders(request):
    user_orders = Order.objects.filter(user=request.user)
    context = {'orders': user_orders}
    return render(request, "shop/orders.html",context)

class add_address(View):
    def get(self,request):
      form = AddressForm()
      return render(request, 'address.html',locals())
    def post(self,request):
      form = AddressForm(request.POST)
      if form.is_valid():
          address = form.save(commit=False)
          address.user = request.user  # Assign the current user
          address.save()
      return render(request, 'address.html',locals())
    
def save_address(request):
    #print("View executed")
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            #print("Form is valid and processing...")
            # Create a new Address instance and populate it with form data
            address = form.save(commit=False)
            address.user = request.user  # Assuming you have user authentication
            address.save()
            messages.success(request,"Address Saved Successfully !")
            return render(request, 'shop/address.html', {'form': form,})
        else:
           messages.warning(request,"Enter Required Fields Correctly")
            #if not form.cleaned_data.get('save_address'):
                #form.add_error('save_address', 'Please check the Save My Address checkbox.')
    else:
        form = AddressForm()

    context = {'form': form}
    return render(request, 'shop/address.html', context)

@login_required
def saved_addresses(request):
    addresses = Address.objects.filter(user=request.user)  # Fetch addresses for the logged-in user
    context = {'addresses': addresses}
    return render(request, 'shop/saved_addresses.html', context)

def editAddress(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('saved_addresses')  # Redirect to the saved addresses page
        else:
           print("Form has validation errors:", form.errors)
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
        'address_id': address_id,
    }
    return render(request, 'shop/edit_address.html', context)

@login_required
def checkout(request):
    user_id = request.user.id
    print(user_id)
    user=request.user
    cart_items = Cart.objects.filter(user=user)
    famount = 0
    total = 0
    amount = 0
    for item in cart_items:
        item.total = item.product_qty * item.product.selling_price
        amount += item.total
    for p in cart_items:
      value = p.product_qty * p.product.selling_price
      famount = famount+value
      value1 = p.product_qty * p.product.selling_price
      total = total+value1
    if famount < 500:
      famount += 50
    totalamount = famount
    cart_total = totalamount
    razoramount = int(cart_total*100)
    request.session['cart_total'] = cart_total
    delivery_addresses = Address.objects.filter(user=request.user)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    data = { "amount":razoramount, "currency":"INR", "receipt":"order_rcptid_12"}
    payment_response = client.order.create(data=data)
    print(payment_response)
    order_id = payment_response['id']
    order_status = payment_response['status']
    if order_status == 'created':
      payment = Payment(user=user,amount=totalamount,razorpay_order_id=order_id,payment_status= order_status,
      )
      print("Stored Payment:", payment)
      payment.save()
    print("stored")
    context = {
        'cart_items': cart_items,'total': total,'amount':amount,'cart_total': cart_total,'delivery_addresses': delivery_addresses,'razoramount':razoramount,'order_id':order_id,'user_id':user_id,
    }
    print("passed")
    print(user)
    return render(request, "shop/checkout.html",context)

def payment_done(request):
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')
    if user.is_authenticated:
      customer = user.first_name
      print("called")
      order_id = request.GET.get('order_id')
      payment_id = request.GET.get('payment_id')
      print("Order ID:", order_id)
      print("Payment ID:", payment_id)
      print(user)

      try:
          payment = Payment.objects.get(razorpay_order_id=order_id)
          payment.paid = True
          payment.payment_id = payment_id
          payment.save()

          cart = Cart.objects.filter(user=user)
          print(cart)
          for c in cart:
              Order.objects.create(
                  user=c.user,
                  customer=customer,
                  product=c.product,
                  quantity=c.product_qty,
                  payment=payment,
              )
              c.delete()
          print(c.user)    
          print("removed from cart")
          return redirect('payment_success')
      except Payment.DoesNotExist:
          return redirect('payment_failure')
    else:
        return redirect('login')

@login_required
def payment_success(request):
    user=request.user
    return render(request, 'payment/success.html')

@login_required
def payment_failure(request):
    user=request.user
    return render(request, 'payment/failure.html')