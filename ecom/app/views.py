from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, Order
from .forms import CustomerRegistrationForm, ProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Products and Info
class ProductView(View):
    def get(self, request):
        total_items = 0
        user = request.user
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        smartphones = Product.objects.filter(category='SP')
        if user.is_authenticated:
            total_items = len(Cart.objects.filter(user= user))
        return render(request, 'app/home.html', {'topwears': topwears,
        'bottomwears':bottomwears,
        'smartphones':smartphones, 'total_items':total_items})

class ProductDetailView(View):
    def get(self, request, product_id):
        total_items = 0
        user = request.user
        if user.is_authenticated:
            total_items = len(Cart.objects.filter(user= user))
        product = Product.objects.get(pk=product_id)
        in_cart = False
        if user.is_authenticated:
            in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'in_cart':in_cart, 'total_items':total_items})



# Products in user cart
@login_required
def add_to_cart(request):
    user= request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
        total_items = 0
        user = request.user
        if user.is_authenticated:
            total_items = len(Cart.objects.filter(user= user))
        if user.is_authenticated:
            cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_has_items = [item for item in Cart.objects.all() if item.user == user]
        if cart_has_items:
            for item in cart_has_items:
                temp = (item.quantity * item.product.discounted_price)
                amount += temp
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'cart': cart, 'total_amount': total_amount, 'amount': amount, 'total_items':total_items})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    user = request.user
    if request.method=="GET":
        product_id = request.GET['product_id']
        item = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        item.quantity+=1
        item.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_has_items = [item for item in Cart.objects.all() if item.user == request.user]
        for item in cart_has_items:
            temp = (item.quantity * item.product.discounted_price)
            amount += temp

        data = {
            'quantity': item.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)

def minus_cart(request):
    user = request.user
    if request.method=="GET":
        product_id = request.GET['product_id']
        item = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        item.quantity-=1
        item.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_has_items = [item for item in Cart.objects.all() if item.user == request.user]
        for item in cart_has_items:
            temp = (item.quantity * item.product.discounted_price)
            amount += temp

        data = {
            'quantity': item.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)

def removeitem(request):
    total_items = 0 
    if request.method=="GET":
        product_id = request.GET['product_id']
        item = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        item.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_has_items = [item for item in Cart.objects.all() if item.user == request.user]
        for item in cart_has_items:
            temp = (item.quantity * item.product.discounted_price)
            amount += temp
            total_items +=1

        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount,
            'total_items':total_items,
        }
        return JsonResponse(data)

@login_required
def checkout(request):
    user = request.user
    total_items = 0
    if user.is_authenticated:
        total_items = len(Cart.objects.filter(user= user))
    addr = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_has_items = [item for item in Cart.objects.all() if item.user == request.user]
    if cart_has_items:
        prices = []
        for item in cart_has_items:
            temp = (item.quantity * item.product.discounted_price)
            amount += temp
            prices.append(temp)
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'addr':addr, 'total_amount': total_amount, 'cart_items':cart_items, 'prices':prices, 'total_items':total_items})

def payment(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for item in cart:
        Order(user=user, customer=customer, product=item.product, quantity=item.quantity).save()
        item.delete()
    return redirect ('orders')

@login_required
def orders(request):
    total_items = 0
    user = request.user
    if user.is_authenticated:
        total_items = len(Cart.objects.filter(user= user))
    orders = Order.objects.filter(user=user)
    return render(request, 'app/orders.html', {'orders':orders, 'total_items':total_items})



# Profile and Addresses
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        total_items = 0
        user = request.user
        if user.is_authenticated:
            total_items = len(Cart.objects.filter(user= user))
        form = ProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'total_items':total_items})

    def post(self, request):
        success=False
        form = ProfileForm(request.POST)
        total_items = 0
        user = request.user
        if user.is_authenticated:
            total_items = len(Cart.objects.filter(user= user))
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            data = Customer(user=user, name=name, locality=locality, city=city, state=state, pincode=pincode)
            data.save()
            messages.success(request, 'New address added successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'total_items':total_items})

@login_required
def address(request):
    total_items = 0
    user = request.user
    if user.is_authenticated:
        total_items = len(Cart.objects.filter(user= user))
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addresses':addresses, 'active':'btn-primary', 'total_items':total_items})

@login_required
def delete_address(request, addr_id):
    address = Customer.objects.filter(id=addr_id)
    address.delete()
    return redirect('/address')



def buy_now(request):
    return render(request, 'app/buynow.html')



# Adding products to categories & organised through filters
def phone(request, data=None):
    total_items = 0
    user = request.user
    if user.is_authenticated:
        total_items = len(Cart.objects.filter(user= user))
    if data==None:
        smartphones = Product.objects.filter(category='SP')
    elif data=='Chu' or data=='PLA' or data=='Cons':
        smartphones = Product.objects.filter(category='SP').filter(brand=data)
    elif data=='below':
        smartphones = Product.objects.filter(category='SP').filter(discounted_price__lt=10000)
    elif data=='above':
        smartphones = Product.objects.filter(category='SP').filter(discounted_price__gt=10000)
    return render(request, 'app/phone.html', {'smartphones':smartphones, 'total_items':total_items})

def topwear(request, data=None):
    total_items = 0
    user = request.user
    if user.is_authenticated:
        total_items = len(Cart.objects.filter(user= user))
    if data==None:
        topwears = Product.objects.filter(category='TW')
    elif data=='Zara' or data=='Nike' or data=='Adidas' or data=='XOXO' or data=='Puma':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=2000)
    elif data=='above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=2000)
    return render(request, 'app/topwear.html', {'topwears':topwears, 'total_items':total_items})

def bottomwear(request, data=None):
    total_items = 0
    user = request.user
    if user.is_authenticated:
        total_items = len(Cart.objects.filter(user= user))
    if data==None:
        bottomwears = Product.objects.filter(category='BW')
    elif data=='Zara' or data=='Supreme' or data=='Levis' or data=='Adidas':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=2000)
    elif data=='above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=2000)
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears, 'total_items':total_items})



# Registering Users
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        success=False
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        username = request.POST['username']
        return render(request, 'app/customerregistration.html', {'form':form, 'success':success,'username':username})

