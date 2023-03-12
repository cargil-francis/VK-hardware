from django.shortcuts import render,redirect
from .models import Category,Product,Cart,Address,Order,Userdetails
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
import decimal
from django.utils.decorators import method_decorator
from django.views import View
from .forms import AddressForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from VKhardwares.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET




# Create your views here.


def index(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:4]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'index.html', context)

#product

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'product.html', context)

def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'category_products.html', context)



#Add cart


@login_required
def add_to_cart(request, product_id):
    user = request.user
    # product_id = request.GET.get('prod_id')
    product_id = product_id
    print(product_id)
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    
    return redirect('hardware:cart')

@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('hardware:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('hardware:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('hardware:cart')





@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)
    print(amount)

    ## -- RAZORPAY INTEGRATION -- ##
    import razorpay
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    total_amount = amount + shipping_amount
    DATA = {
        "amount": int(total_amount)*100,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
             "key1": "value3",
            "key2": "value2"
        }
    }
    payment=client.order.create(data=DATA)
    ## --  ---  -- ##

    context = {
        'user' : user,
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
        'payment' : payment,
    }
    
    return render(request, 'cart.html', context)

#User Profile


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'addresses':addresses, 'orders':orders})



@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('hardware:profile')

@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('hardware:profile')

@csrf_exempt
def success(request):
    user_id=request.POST.get('user_id')
    user=get_object_or_404(User,id=user_id)
    address=Address.objects.filter(user=user)
    for a in address:
        ad = a
    Userdetails(user=user,locality=ad.locality,city=ad.city,state=ad.state).save()
    address=Userdetails.objects.filter(user=user)
    for a in address:
        ad = a
    cart=Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user, address=ad, product=c.product, quantity=c.quantity).save()
        c.delete()
        #product = Product.objects.filter(id=c.product.id)
        #product.stock -= c.quantity
    return render(request,'index.html')
    
    