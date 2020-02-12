from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from orders.models import DeliveryDetailsModel
from orders.forms import DeliveryDetailsForm
from .models import CartItemsModel



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # add to db
        if CartItemsModel.objects.filter(product=product, added_by=request.user).exists():
            CartItemsModel.objects.filter(product=product,  added_by=request.user).update(quantity=cd['quantity'])
        else:
            CartItemsModel.objects.create(product=product, quantity=cd['quantity'], added_by=request.user)

        # add to cart
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        print('--------------update', cd)

    return redirect('cart:cart_detail')
    # return HttpResponseRedirect('product_list')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    print('item removed from cart.........', product)
    # delete item in db -- adds to stock
    if CartItemsModel.objects.filter(product=product, added_by=request.user).exists():
        CartItemsModel.objects.filter(product=product, added_by=request.user).delete()
    else:
        # ignore
        pass

    # remove the item from cart
    cart.remove(product)

    return redirect('cart:cart_detail')

# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
#     return render(request, 'cart/detail.html', {'cart': cart})


def cart_detail(request):
    cart = Cart(request)
    products = Product.objects.filter(available=True)
    print('-----------------inside cart detail -----------------------', cart)

    for item in cart:
        print('?????????????????????????????????????????', item)
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        # item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart/cart_details.html', {'cart': cart, 'products': products})
    # return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def cart_checkout(request):
    print('===============================================cart po', request.method)

    if request.method == 'POST':
        print('===============================================cart POST', request.method)

        form = DeliveryDetailsForm(request.POST)
        if form.is_valid():
            print('===============================================cart VALID', request.method)

            if DeliveryDetailsModel.objects.filter(username=request.user).exists():
                delivery_details = DeliveryDetailsModel.objects.filter(username=request.user).values()[0]
                print(delivery_details, ' get')
                count = DeliveryDetailsModel.objects.filter(username=request.user).update(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    )
                if count == 1:
                    data_saved = True

            else:
                DeliveryDetailsModel.objects.create(username=request.user,
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                phone_number=form.cleaned_data['phone_number'],
                                                address=form.cleaned_data['address'],
                                                )
                data_saved = True
            print('----------------------------form', form.cleaned_data)
        else:
            print('==========================cart errors', form.errors)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    if DeliveryDetailsModel.objects.filter(username=request.user).exists():
            delivery_details = DeliveryDetailsModel.objects.filter(username=request.user).values()[0]
            print(delivery_details, ' get')

            return render(request, 'cart/cart_details.html', {'cart': cart, 'delivery_details': delivery_details})

    return render(request, 'cart/cart_details.html', {'cart': cart, 'delivery_details': ''})
