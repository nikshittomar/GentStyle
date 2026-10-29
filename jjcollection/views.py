from Store.models import Product
from Category.models import Category, SubCategory
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

def home(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # ✅ Add pagination (show 8 products per page — adjust if you want)
    paginator = Paginator(products, 16)
    page = request.GET.get('page')
    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    context = {
        'product': paged_products,
        'category': categories,
    }
    return render(request, 'index.html', context)
