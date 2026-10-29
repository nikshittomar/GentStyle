from django.shortcuts import render, redirect,get_object_or_404
from Store.models import Product,Size
from Carts.models import Cart, CartItem
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem, Size

from django.shortcuts import render, redirect, get_object_or_404
from Store.models import Product, Size
from Carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Get or create session cart ID
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# ------------------ ADD TO CART ------------------ #
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size = None

    size_id = request.GET.get('size') or request.POST.get('size')
    if size_id:
        size = get_object_or_404(Size, id=size_id, is_active=True)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user,
            size=size,
            defaults={'quantity': 1, 'sub_total': product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.sub_total = cart_item.quantity * product.price
            cart_item.save()
    else:
        cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            size=size,
            defaults={'quantity': 1, 'sub_total': product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.sub_total = cart_item.quantity * product.price
            cart_item.save()

    return redirect('cart')


# ------------------ REMOVE ONE QUANTITY ------------------ #
def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_id = request.GET.get('size')
    size = None
    if size_id:
        size = get_object_or_404(Size, id=size_id, is_active=True)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, size=size)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, size=size)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.sub_total = cart_item.quantity * product.price
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


# ------------------ REMOVE ENTIRE CART ITEM ------------------ #
def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_id = request.GET.get('size')
    size = None
    if size_id:
        size = get_object_or_404(Size, id=size_id, is_active=True)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, size=size)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, size=size)

        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


# ------------------ VIEW CART ------------------ #
def cart(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    sub_total = 0
    cart_items = None

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if cart_items:
            for cart_item in cart_items:
                # Always recalc sub_total in case product price changed
                cart_item.sub_total = cart_item.product.price * cart_item.quantity
                cart_item.save()

                sub_total += cart_item.sub_total
                total += cart_item.sub_total
                quantity += cart_item.quantity

            tax = (5 * total) / 100  # example 5% tax
            grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'sub_total': sub_total
    }
    return render(request, 'cart.html', context)

def search(request):
    products = []
    product_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(product_description__icontains=keyword) | 
                Q(product_name__icontains=keyword)
            )
            product_count = products.count()

    context = {
        'product': products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)

@login_required(login_url='login')
def checkout(request, tax=0, total=0, grand_total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            # Logged-in users: get cart items linked to this user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Guests: get cart items linked to session cart
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)
