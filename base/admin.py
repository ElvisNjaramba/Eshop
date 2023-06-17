from django.contrib import admin
from .models import Product, Supplier

# Register your models here.
admin.site.register(Product)
admin.site.register(Supplier)