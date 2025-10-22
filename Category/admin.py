from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display  = ('category_name', 'slug')
admin.site.register(Category, CategoryAdmin)

class  Sub_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('sub_category_name',)}
    list_display  = ('sub_category_name', 'slug')
admin.site.register(SubCategory, Sub_CategoryAdmin)