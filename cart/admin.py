from django.contrib import admin

from .models import CartItemsModel

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'added_at']
    list_filter = ['added_at']

admin.site.register(CartItemsModel, CartItemsAdmin)
