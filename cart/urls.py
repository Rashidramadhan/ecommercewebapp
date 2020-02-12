from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),

    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path('add/(int:<product_id>)', views.cart_add, name='cart_add'),
    # path('add/(int:<product_id>)', views.dummy_cart_add, name='dummy_cart_add'),
    path('remove/(int:<product_id>)', views.cart_remove, name='cart_remove'),

# from django.conf.urls import url
# from . import views
#
# app_name = 'cart'
#
# urlpatterns = [
#     url(r'^$', views.cart_detail, name='cart_detail'),
#     url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
#     url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]