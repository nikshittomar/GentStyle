from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from Category.models import Category,SubCategory
from Carts.models import CartItem
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from Carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from Store.forms import ReviewForm
from django.contrib import messages
from Orders.models import OrderProduct

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product, Category,Size


def sizechart(request):
    sizes = {
        "Coat": [
            {"Size":"XS","Chest":"34","Shoulder":"17","Sleeve":"23","Length":"27"},
            {"Size":"S","Chest":"36","Shoulder":"17.5","Sleeve":"24","Length":"28"},
            {"Size":"M","Chest":"38","Shoulder":"18","Sleeve":"24.5","Length":"29"},
            {"Size":"L","Chest":"40","Shoulder":"18.5","Sleeve":"25","Length":"30"},
            {"Size":"XL","Chest":"42","Shoulder":"19","Sleeve":"25.5","Length":"31"},
            {"Size":"XXL","Chest":"44","Shoulder":"19.5","Sleeve":"26","Length":"32"},
            {"Size":"XXXL","Chest":"46","Shoulder":"20","Sleeve":"26.5","Length":"33"},
        ],
        "Pant": [
            {"Size":"XS","Waist":"28","Hip":"34","Inseam":"28","Length":"39"},
            {"Size":"S","Waist":"30","Hip":"36","Inseam":"29","Length":"40"},
            {"Size":"M","Waist":"32","Hip":"38","Inseam":"30","Length":"41"},
            {"Size":"L","Waist":"34","Hip":"40","Inseam":"31","Length":"42"},
            {"Size":"XL","Waist":"36","Hip":"42","Inseam":"32","Length":"43"},
            {"Size":"XXL","Waist":"38","Hip":"44","Inseam":"33","Length":"44"},
            {"Size":"XXXL","Waist":"40","Hip":"46","Inseam":"34","Length":"45"},
        ],
        "Shirt": [
            {"Size":"XS","Chest":"34","Shoulder":"17","Sleeve":"23","Length":"27"},
            {"Size":"S","Chest":"36","Shoulder":"17.5","Sleeve":"24","Length":"28"},
            {"Size":"M","Chest":"38","Shoulder":"18","Sleeve":"24.5","Length":"29"},
            {"Size":"L","Chest":"40","Shoulder":"18.5","Sleeve":"25","Length":"30"},
            {"Size":"XL","Chest":"42","Shoulder":"19","Sleeve":"25.5","Length":"31"},
            {"Size":"XXL","Chest":"44","Shoulder":"19.5","Sleeve":"26","Length":"32"},
            {"Size":"XXXL","Chest":"46","Shoulder":"20","Sleeve":"26.5","Length":"33"},
        ],
        "Sherwani": [
            {"Size":"XS","Chest":"34","Shoulder":"17","Sleeve":"24","Length":"42"},
            {"Size":"S","Chest":"36","Shoulder":"17.5","Sleeve":"24.5","Length":"43"},
            {"Size":"M","Chest":"38","Shoulder":"18","Sleeve":"25","Length":"44"},
            {"Size":"L","Chest":"40","Shoulder":"18.5","Sleeve":"25.5","Length":"45"},
            {"Size":"XL","Chest":"42","Shoulder":"19","Sleeve":"26","Length":"46"},
            {"Size":"XXL","Chest":"44","Shoulder":"19.5","Sleeve":"26.5","Length":"47"},
            {"Size":"XXXL","Chest":"46","Shoulder":"20","Sleeve":"27","Length":"48"},
        ],
        "Vest Coat": [
            {"Size":"XS","Chest":"34","Shoulder":"16","Length":"25"},
            {"Size":"S","Chest":"36","Shoulder":"16.5","Length":"26"},
            {"Size":"M","Chest":"38","Shoulder":"17","Length":"27"},
            {"Size":"L","Chest":"40","Shoulder":"17.5","Length":"28"},
            {"Size":"XL","Chest":"42","Shoulder":"18","Length":"29"},
            {"Size":"XXL","Chest":"44","Shoulder":"18.5","Length":"30"},
            {"Size":"XXXL","Chest":"46","Shoulder":"19","Length":"31"},
        ],
        "Nehru Jacket": [
            {"Size":"XS","Chest":"34","Shoulder":"16","Length":"26"},
            {"Size":"S","Chest":"36","Shoulder":"16.5","Length":"27"},
            {"Size":"M","Chest":"38","Shoulder":"17","Length":"28"},
            {"Size":"L","Chest":"40","Shoulder":"17.5","Length":"29"},
            {"Size":"XL","Chest":"42","Shoulder":"18","Length":"30"},
            {"Size":"XXL","Chest":"44","Shoulder":"18.5","Length":"31"},
            {"Size":"XXXL","Chest":"46","Shoulder":"19","Length":"32"},
        ],
        "Indo Western": [
            {"Size":"XS","Chest":"34","Shoulder":"17","Sleeve":"24","Length":"39"},
            {"Size":"S","Chest":"36","Shoulder":"17.5","Sleeve":"24.5","Length":"40"},
            {"Size":"M","Chest":"38","Shoulder":"18","Sleeve":"25","Length":"41"},
            {"Size":"L","Chest":"40","Shoulder":"18.5","Sleeve":"25.5","Length":"42"},
            {"Size":"XL","Chest":"42","Shoulder":"19","Sleeve":"26","Length":"43"},
            {"Size":"XXL","Chest":"44","Shoulder":"19.5","Sleeve":"26.5","Length":"44"},
            {"Size":"XXXL","Chest":"46","Shoulder":"20","Sleeve":"27","Length":"45"},
        ],
        "Safari Suit": [
            {"Size":"XS","Chest":"34","Shoulder":"17","Sleeve":"23","Length":"28"},
            {"Size":"S","Chest":"36","Shoulder":"17.5","Sleeve":"24","Length":"29"},
            {"Size":"M","Chest":"38","Shoulder":"18","Sleeve":"24.5","Length":"30"},
            {"Size":"L","Chest":"40","Shoulder":"18.5","Sleeve":"25","Length":"31"},
            {"Size":"XL","Chest":"42","Shoulder":"19","Sleeve":"25.5","Length":"32"},
            {"Size":"XXL","Chest":"44","Shoulder":"19.5","Sleeve":"26","Length":"33"},
            {"Size":"XXXL","Chest":"46","Shoulder":"20","Sleeve":"26.5","Length":"34"},
        ],
    }
    context={
         "sizes": sizes,
    }

    return render(request, "sizechart.html", context)

def store(request, category_slug=None, subcategory_slug=None):
    products = Product.objects.filter(is_available=True)
    links = Category.objects.prefetch_related('subcategories').all()

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcats = SubCategory.objects.filter(category=category)
        products = products.filter(category=category) | products.filter(sub_category__in=subcats)

    # Filter by subcategory
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = products.filter(sub_category=subcategory)

    # ✅ Add pagination here (3 products per page, change if needed)
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'links': links,
        'product': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)

def product_detail(request, category_slug, product_slug, subcategory_slug=None):
    try:
        if subcategory_slug:  
            # Product under subcategory
            single_product = Product.objects.get(
                category__slug=category_slug,
                subcategory__slug=subcategory_slug,
                slug=product_slug
            )
        else:  
            # Product directly under main category
            single_product = Product.objects.get(
                category__slug=category_slug,
                slug=product_slug
            )

        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), 
            product=single_product
        ).exists()
    except Product.DoesNotExist:
        single_product = None
        in_cart = False

    # Check if the user has ordered this product before
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(
            user=request.user, 
            product_id=single_product.id
        ).exists()
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    sizes = Size.objects.active()
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'sizes': sizes,
    }
    return render(request, 'product_detail.html', context)

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
 

    context = {
        'single_product': single_product,
        'in_cart' : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
    
    }
    return render(request, 'product_detail.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)




def contact_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("msg")

        if email and message:
            ContactMessage.objects.create(email=email, message=message)
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")  # Redirect to same page after submit

        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, "contact.html")  # your template name
