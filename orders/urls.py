from django.urls import path
from .import views


app_name = 'orders'



urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('purchase/', views.make_purchase, name='purchase'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('payment/', views.confirm_payment, name='payment'),
    path('dummy_order_create/', views.dummy_order_create, name='dummy_order_create'),
]