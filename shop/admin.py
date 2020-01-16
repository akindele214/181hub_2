from django.contrib import admin
from .models import Product, ProductImage

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'prod_name')
    search_fields = ('prod_name', 'prod_details', 'prod_price')
    date_hierarchy = ('date_posted')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('prod', 'image')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)