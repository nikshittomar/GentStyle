
from django.urls import path
from . import views
from .views import *

from django.urls import path


urlpatterns = [
    # All Products
    path('', views.store, name='store'),
    
    path('catalogue/', views.catalogue, name='catalogue'),
    path('sizechart/', sizechart, name="sizechart"),
    path("contact/", views.contact_view, name="contact"),
    
    # Virtual Try-On
        path(
        'virtual-tryon/<int:product_id>/',
        views.virtual_tryon,
        name='virtual_tryon',
    ),
    # Subcategory products
    path('subcategory/<slug:subcategory_slug>/', views.store, name='products_by_sub_category'),

    # Category products
    path('<slug:category_slug>/', views.store, name='products_by_category'),

    # Product detail (with subcategory)
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', 
         views.product_detail, name="product_detail_with_subcategory"),

    # Product detail (without subcategory)
    path('<slug:category_slug>/<slug:product_slug>/', 
         views.product_detail, name="product_detail"),
    # Review submission
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    

    path('catalogue/', views.catalogue, name='catalogue'),
    path('catalogue/<slug:category_slug>/', views.catalogue, name='catalogue_by_category'),
    path('catalogue/<slug:category_slug>/<slug:subcategory_slug>/', views.catalogue, name='catalogue_by_subcategory'),

]


