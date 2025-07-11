from django.contrib import admin
from .product import Product
from .category import Category
class categoryinfo(admin.ModelAdmin):
    list_display=["name"]
class productinfo(admin.ModelAdmin):
    list_display=["name","category","price"]
# Register your models here.
admin.site.register(Product,productinfo)
admin.site.register(Category,categoryinfo)

