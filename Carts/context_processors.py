from .models import Cart, CartItem
from .views import _cart_id



from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0

    # Don't run for admin panel pages
    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            # Logged-in users: get cart items linked to this user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Guests: get cart items linked to session cart
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            else:
                cart_items = []

        # Count total quantity
        for item in cart_items:
            cart_count += item.quantity

    except Exception:
        cart_count = 0

    return dict(cart_count=cart_count)
    