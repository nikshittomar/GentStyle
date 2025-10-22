from Store.models import Product
from Category.models import Category, SubCategory
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages


def home(request):
    product=Product.objects.all().filter(is_available=True)
    category = Category.objects.all() 
    context = {
        'product':product,
        'category':category,
    }
    return render(request, 'index.html', context)
def catalogue(request, category_slug=None, subcategory_slug=None):
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
    return render(request, 'catalogue.html', context)


