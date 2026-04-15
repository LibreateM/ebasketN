from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum,Count, F
from django.db.models.functions import TruncMonth
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import PasswordResetRequestForm, SetNewPasswordForm
from django.urls import reverse
import json
from django.http import HttpResponse
import cloudinary
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.core.files.storage import default_storage
import os
def check_env(request):
    
    return HttpResponse(
        f"CLOUDINARY_URL: {os.getenv('CLOUDINARY_URL')}"
    )
def test_storage(request):  
    
    return HttpResponse(
        f"SETTING: {settings.DEFAULT_FILE_STORAGE} \n STORAGE: {default_storage}"
    )
def test_cloudinary(request):
    cfg = cloudinary.config()
    return HttpResponse(
        f"cloud: {cfg.cloud_name}, storage: {default_storage}"
    )
# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'subpages/about.html')
def address(request):
    return render(request,'subpages/address.html')
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = 0
    for item in cart_items:
        item.total = item.product.price * item.quantity   # attach dynamically
        total += item.total
 
    return render(request, 'subpages/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })
def category(request):
    key = Category.objects.all()
    return render(request,'subpages/category.html',{'category': key})
def contact(request):
    if request.method == 'POST':
      FullName = request.POST.get('FullName')
      number = request.POST.get('number')
      message = request.POST.get('message')
      email = request.POST.get('email')
      Contact.objects.create(FullName=FullName, number=number, message=message,email=email)
      messages.success(request, "Your Message should be recorded our team contact soon")
      return redirect('contact')
    return render(request,'subpages/contact.html')
@login_required
def done(request):
    order = Order.objects.filter(user=request.user).last()

    address = Address.objects.filter(user=request.user).last()

    return render(request, 'subpages/done.html', {
        'order': order,
        'address': address
    })
def faq(request):
    return render(request,'subpages/faq.html')    
@login_required
def order_summary(request):
    buy_now = request.session.get('buy_now')

    total = 0

    # 🔥 PRIORITY 1 → BUY NOW
    if buy_now:
        product = get_object_or_404(Product, id=buy_now['product_id'])
        qty = buy_now['quantity']

        cart_items = [{
            'product': product,
            'quantity': qty,
            'total': product.price * qty
        }]

        total = product.price * qty

    # 🛒 PRIORITY 2 → CART
    else:
        cart_items = Cart.objects.filter(user=request.user).select_related('product')

        for item in cart_items:
            item.total = item.product.price * item.quantity
            total += item.total

    # address & payment
    add = Address.objects.filter(user=request.user)
    pay = PaymentMethod.objects.filter(user=request.user).last()

    return render(request, 'subpages/order_summary.html', {
        'cart_items': cart_items,
        'total': total,
        'add': add,
        'pay': pay
    })

def password(request):
    return render(request,'subpages/password.html')   
@login_required
def payment_method(request):
    if request.method == 'POST':
        method = request.POST.get('method_type')

        payment = PaymentMethod(user=request.user, method_type=method)

        if method == 'card':
            payment.card_owner = request.POST.get('card_owner', '')

        elif method == 'paypal':
            payment.paypal_type = request.POST.get('paypal_type', 'domestic')

        elif method == 'netbanking':
            payment.bank_name = request.POST.get('bank_name', '')

        payment.save()
        return redirect('order_summary')

    return render(request,'subpages/payment_method.html')    
def privacy(request):
    return render(request,'subpages/privacy.html')    
def product(request,id):
    product = get_object_or_404(Product, id=id)  
    return render(request,'subpages/product.html',{'product': product})
def productlist1(request):
    return render(request,'subpages/productlist1.html')    
   
@login_required
def profile(request):
    wish = Wish.objects.filter(user=request.user).count()
    cart = Cart.objects.filter(user=request.user).count()
    order = Order.objects.filter(user=request.user).count()
    recent_orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')[:3] 
    order1 = Order.objects.filter(user=request.user).aggregate(total=Sum('total_price'))['total'] or 0
    payment_data = Order.objects.filter(user=request.user).values('payment_method').annotate(count=Count('id'))
    category_data = OrderItem.objects.filter(
        order__user=request.user
    ).values('product__category__category').annotate(
        total=Count('id')
    )
    monthly_data = Order.objects.filter(
    user=request.user
).annotate(month=TruncMonth('created')).values('month').annotate(
    total=Count('id')
).order_by('month')
    labels = []
    data = []
    cat_labels = []
    cat_data = []
    months = []
    month_count = []

    for item in payment_data:
        labels.append(item['payment_method'])
        data.append(item['count'])
    for item in category_data:
        cat_labels.append(item['product__category__category'])
        cat_data.append(item['total'])
    for item in monthly_data:
        months.append(item['month'].strftime("%b")) 
        month_count.append(item['total'])
    context={
        'wish':wish,
        'cart':cart,
        'order':order,
        'order1':order1,
        'recent':recent_orders,
        'payment_labels': labels,
        'payment_data': data,
        'cat_labels': cat_labels,
        'cat_data': cat_data,
        'months': months,
        'month_count': month_count,
    }
    return render(request,'subpages/profile.html',context)    

def review(request):
    reviews = ReviewForm.objects.all().order_by('-id')
    return render(request,'subpages/review.html', {'reviews': reviews})    
def review_form(request):
    if request.method == 'POST':
      name = request.POST.get('name')
      review = request.POST.get('review')
      star = int(request.POST.get('star'))
      ReviewForm.objects.create( name=name, star=star, review=review)
      return redirect('review')
    return render(request,'subpages/review_form.html')  
 
def search(request):
    query = request.GET.get('q')
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            Q(product=query) 
        )
    return render(request,'subpages/search.html',{
        'products': products,
        'query': query
    })    
def terms(request):
    return render(request,'subpages/terms.html')    
@login_required
def wish(request):
    wishlist_items = Wish.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request,'subpages/wish.html',context)    


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('registration')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('profile')

    return render(request, 'subpages/registration.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'subpages/login.html')
def user_logout(request):
    auth_logout(request)
    return redirect('login')
   

@login_required
def edit(request):
    if request.method == 'POST':
        user = request.user

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if email == "":
            messages.error(request, "email cannot be empty")
            return redirect('edit')
        user.username = email
        user.email = email
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile')
    return render(request, 'subpages/edit.html')  


def validate_file_extension(file_type):
    def validate(file):
        allowed_extensions = {
            'image': ['jpg', 'jpeg', 'png', 'gif'],
            'documents': ['pdf', 'doc', 'docx']
        }

        if file_type not in allowed_extensions:
            raise ValueError('Invalid file type')

        if not file.name.lower().endswith(tuple(allowed_extensions[file_type])):
            raise ValidationError(f'Please select a valid {file_type} file')

    return validate

def categoryform(request):
    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')
    if request.method == 'POST':
        category = request.POST.get('category')
        pic = None

        if request.FILES.get('pic'):
            try:
                validate_file_extension('image')(request.FILES.get('pic'))
                pic = request.FILES.get('pic')
            except ValidationError as e:
                return render(request, 'dashboard/category.html', {
                    'error_message': str(e)
                })

        Category.objects.create(category=category, pic=pic)
        return redirect('dashboard') 
    return render(request, 'dashboard/category.html')

def productform(request):
    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')
    categories = Category.objects.all()
    if request.method == 'POST':
        product = request.POST.get('product')
        star = int(request.POST.get('star'))
        price = int(request.POST.get('price'))
        category_id = request.POST.get('category')
        pic = None
        category = Category.objects.get(id=category_id)
        if request.FILES.get('pic'):
            try:
                validate_file_extension('image')(request.FILES.get('pic'))
                pic = request.FILES.get('pic')
            except ValidationError as e:
                return render(request, 'dashboard/product.html', {
                    'error_message': str(e)
                })

        Product.objects.create(product=product, pic=pic,category=category,star=star,price=price)
        return redirect('dashboard')  

    return render(request, 'dashboard/product.html',{'categories':categories})

def product_by_category(request, id):
    products = Product.objects.filter(category_id=id)
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'subpages/productlist1.html', {'products': page_obj,'page_obj': page_obj})
@login_required
def add_to_cart(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)
        qty = int(request.POST.get('qty', 1))
 
        qty = max(1, min(qty, 99))
 
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
        )
 
        if created:
            cart_item.quantity = qty
        else:
            cart_item.quantity = min(cart_item.quantity + qty, 99)
 
        cart_item.save()
 
        if request.POST.get('buy_now'):
            return redirect('order_summary')
 
        return redirect('cart')
 
    return redirect('category')
@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    wishlist_item, created = Wish.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        print("Added to wishlist")
    else:
        print("Already in wishlist")

    return redirect('wish')
    
@login_required
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wish.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect('wish')
    
def address(request):
    if request.method == 'POST':
      delete= Address.objects.all()
      delete.delete()
      name=request.POST.get('name')
      number=request.POST.get('number')
      add1=request.POST.get('add1')
      add2=request.POST.get('add2')
      city=request.POST.get('city')
      state=request.POST.get('state')
      zipcode=request.POST.get('zipcode')
      country=request.POST.get('country')
      Address.objects.create(user=request.user,name=name,number=number, add1=add1,add2=add2,city=city,state=state,zipcode=zipcode,country=country)
      return redirect('order_summary')
    return render(request,'subpages/address.html')

@login_required
def buy_now(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)
        qty = int(request.POST.get('qty', 1))

        request.session['buy_now'] = {
            'product_id': product.id,
            'quantity': qty
        }

        return redirect('order_summary')

    return redirect('category')

@login_required
def place_order(request):
    buy_now = request.session.get('buy_now')
    pay = PaymentMethod.objects.filter(user=request.user).last()

    # ⚡ BUY NOW FLOW
    if buy_now:
        product = get_object_or_404(Product, id=buy_now['product_id'])
        qty = buy_now['quantity']

        total = product.price * qty

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            payment_method=pay
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price=product.price
        )

        del request.session['buy_now']   # 🔥 IMPORTANT

        return redirect('done')

    # 🛒 CART FLOW
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        payment_method=pay
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return redirect('done')  


def adminlogin(request):
  if request.method == 'POST':
    admin1=request.POST.get('admin1')
    password=request.POST.get('password')
    if admin1=='admin' and password=='admin123':
        request.session['admin_logged_in'] = True   
        return redirect('dashboard')
    else:
        messages.error(request, "Alas Your Admin Name And Password Not Matched!!")
  return render(request,'dashboard/AdminLogin.html')
  
def admin_logout(request):
    request.session.flush()  
    return redirect('adminlogin')


import json
from django.db.models import Sum
from django.db.models.functions import TruncMonth

def dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    monthly_data = Order.objects.annotate(
        month=TruncMonth('created')
    ).values('month').annotate(
        total=Sum('total_price')
    ).order_by('month')

    category_data = OrderItem.objects.values(
        'product__category__category'
    ).annotate(
        total=Sum(F('price') * F('quantity'))
    )

    months = []
    revenue_data = []

    for item in monthly_data:
        months.append(item['month'].strftime("%b"))
        revenue_data.append(float(item['total']))

    cat_labels = []
    cat_data = []

    for item in category_data:
        cat_labels.append(item['product__category__category'])
        cat_data.append(float(item['total'] or 0))

    recent_orders = OrderItem.objects.select_related('order', 'product').order_by('-id')[:5]

    top_products = OrderItem.objects.values(
        'product__product'
    ).annotate(
        total=Sum('price')
    ).order_by('-total')[:5]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,

        'months': json.dumps(months),
        'revenue_data': json.dumps(revenue_data),

        'cat_labels': json.dumps(cat_labels),
        'cat_data': json.dumps(cat_data),

        'recent_orders': recent_orders,
        'top_products': top_products,
    }

    return render(request, 'dashboard/dashboard.html', context)


def password_reset_request(request):
    """Step 1: User enters their registered email."""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
 
            # Check if the email belongs to a registered user
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                # Security: show same message even if email not found
                messages.success(
                    request,
                    "If that email is registered, a password reset link has been sent."
                )
                return redirect('password_reset_request')
 
            # Invalidate any existing unused tokens for this user
            PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
 
            # Create a fresh token
            reset_token = PasswordResetToken.objects.create(user=user)
 
            # Build the reset URL
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'token': reset_token.token})
            )
 
            # Send email
            send_mail(
                subject="Password Reset Request",
                message=(
                    f"Hello {user.username},\n\n"
                    f"We received a request to reset your password.\n"
                    f"Click the link below to set a new password (valid for 1 hour):\n\n"
                    f"{reset_url}\n\n"
                    f"If you did not request this, please ignore this email.\n\n"
                    f"Thanks,\nThe Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
 
            messages.success(
                request,
                "If that email is registered, a password reset link has been sent."
            )
            return redirect('password_reset_request')
    else:
        form = PasswordResetRequestForm()
 
    return render(request, 'eapp/password_reset_request.html', {'form': form})
 
 
def password_reset_confirm(request, token):
    """Step 2: User clicks the link and sets a new password."""
    try:
        reset_token = PasswordResetToken.objects.select_related('user').get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('password_reset_request')
 
    if not reset_token.is_valid():
        messages.error(request, "This reset link has expired or already been used.")
        return redirect('password_reset_request')
 
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
 
            # Update password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
 
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
 
            messages.success(request, "Your password has been changed successfully. You can now log in.")
            return redirect('login')
    else:
        form = SetNewPasswordForm()
 
    return render(request, 'eapp/password_reset_confirm.html', {'form': form, 'token': token})

    
def admin_users(request):
    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    users = User.objects.all().order_by('-id')

    user_data = []

    for user in users:
        total_orders = Order.objects.filter(user=user).count()
        total_cart = Cart.objects.filter(user=user).count()
        total_wishlist = Wish.objects.filter(user=user).count()
        total_spent = Order.objects.filter(user=user).aggregate(
            total=Sum('total_price')
        )['total'] or 0

        user_data.append({
            'user': user,
            'orders': total_orders,
            'cart': total_cart,
            'wishlist': total_wishlist,
            'spent': total_spent,
        })

    return render(request, 'dashboard/users.html', {'user_data': user_data})

def admin_contacts(request):
    if not request.session.get('admin_logged_in'):
        return redirect('adminlogin')

    contacts = Contact.objects.all().order_by('-id')

    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        email = request.POST.get('email')
        reply_message = request.POST.get('reply_message')

        contact = Contact.objects.get(id=contact_id)


        ContactReply.objects.create(
            contact=contact,
            reply_message=reply_message
        )

        send_mail(
            subject="Reply from Admin",
            message=reply_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Reply sent successfully!")
        return redirect('admin_contacts')

    return render(request, 'dashboard/contacts.html', {
        'contacts': contacts
    })