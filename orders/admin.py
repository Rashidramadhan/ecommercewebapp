from django.contrib import admin

# Register your models here.
from .models import OrderModel, DeliveryDetailsModel, SalesModel


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'username', 'item',  'created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated']

admin.site.register(OrderModel, OrderAdmin)



class DeliveryDetailsAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'address']


admin.site.register(DeliveryDetailsModel, DeliveryDetailsAdmin)


class SalesModelAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'username', 'payment_option', 'total_amount',  'payment_date']
    list_filter = ['payment_date']


admin.site.register(SalesModel, SalesModelAdmin)
