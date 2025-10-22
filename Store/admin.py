from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product,ReviewRating,Size

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price', 'stock', 'category', 'modified_date','is_available',)
    prepopulated_feilds = {'slug': ('product_name',)}

    
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating,)
admin.site.register(Size)
