from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('FullName', 'email', 'number', 'created')
    search_fields = ('FullName', 'email', 'number')
    list_filter = ('created',)
    ordering = ('-created',)
@admin.register(ReviewForm)
class ReviewFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'star', 'review', 'created')
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'created')
    search_fields = ('category','created')
    ordering = ('-category',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'created')
    search_fields = ('product','created')
    ordering = ('-product',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # FIX: 'Product' → 'product'  (field names are case-sensitive; capital P caused AttributeError)
    list_display  = ('user', 'product', 'quantity', 'created')
    search_fields = ('product__product', 'user__username')  # FIX: use related field lookups
    ordering      = ('-created',)         # FIX: was ('-product') which is invalid on Cart
 


