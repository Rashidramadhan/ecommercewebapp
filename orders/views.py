from django.shortcuts import render
from .models import OrderModel, DeliveryDetailsModel, SalesModel
from .forms import OrderForm, DeliveryDetailsForm, SalesForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddProductForm
from shop.models import Product
from cart.models import CartItemsModel



@login_required
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderModel.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
        else:
            form_errors = form.errors

            form = OrderForm()
            return render(request, 'orders/order/create.html', {'form': form, 'form_errors': form_errors})

    else:
        form = OrderForm()
    return render(request, 'orders/order/create.html', {'form': form})



@login_required
def dummy_order_create(request):
    print('-------------------------------------------insided dummy data view')
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        # form2 = SalesModel(request.POST)
        if form.is_valid():
            # order = form.save()
            order_id = generate_order_id()

            for item in cart:
                print(item, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..')
                products = Product.objects.filter(name=item['product']).values()[0]
                old_qty = int(products['stock'])
                sold_qty = int(item['quantity'])
                new_qty = old_qty - sold_qty
                if new_qty >= 0:
                    count = Product.objects.filter(name=item['product']).update(stock=new_qty)
                    if count == 1:
                        print('record updated', item['product'])
                    print('-------------------checking order id----------------------', order_id)


                    OrderModel.objects.create(
                        order_id=order_id,
                        item=item['product'],
                        price=item['price'],
                        username=request.user,
                        quantity=item['quantity'],
                        paid='True'
                    )

                else:
                    pass
                    # errors = ' Sorry, available stop for {} is {} '.format(item['product'])
                # update available stock

                # delete items in cart_table in db
                if CartItemsModel.objects.filter(product=item['product'], added_by=request.user).exists():
                    CartItemsModel.objects.filter(product=item['product'], added_by=request.user).delete()
                else:
                    # ignore
                    pass


                print('----------------------------------------#####')
                # print(item['product'], 'OLD STOCK: ',  products['quantity'])
                # print(item['product'], 'OLD STOCK: ',  products['stock'], ' NEW STOCK: ', products['stock'], '-',  item['quantity'])


                # calculate total
            total_amount = 0
            data = OrderModel.objects.filter(order_id=order_id).values()
            print('data recieved>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', data)
            for item_recieved in data:
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
                qty = item_recieved['quantity']
                price = item_recieved['price']
                total_amount = total_amount + int(qty)*price



                # print(' Calculated total for {} is : {}x{} = {} '.format(item_recived['item'], qty, price, total_amount))
            print(' Calculated total ##### is :', total_amount)






            SalesModel.objects.create(
                order_id=order_id,
                username=request.user,
                payment_option='M-PESA',
                total_amount=total_amount

            )
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': 'order', 'order_id': order_id})
        else:
            print('-------------------------------form is NOT valid', form.errors)

            form_errors = form.errors

            form = OrderForm()
            return render(request, 'orders/order/create.html', {'form': form, 'form_errors': form_errors})

    else:
        form = OrderForm()
    return render(request, 'orders/order/create.html', {'form': form})


@login_required
def make_purchase(request):
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")

    order_form = OrderForm(request.POST)
    sales_form = SalesForm(request.POST)
    print('nothing ')
    if request.method == 'POST':
        print('-------post---')
        order_form = OrderForm(request.POST)
        sales_form = SalesForm(request.POST)
        if sales_form.is_valid() and order_form.is_valid():
            username = request.user
            order_id = generate_order_id()
            payment_option = sales_form.cleaned_data['payment_option']
            items = order_form.cleaned_data['item']
            paid = confirm_payment()
            total_amount = sales_form.cleaned_data['total_amount']

            count1 = OrderModel.objects.create(username=username, item=items, order_id=order_id, paid=paid)
            count2 = SalesModel.objects.create(username=username, total_amount=total_amount, order_id=order_id, payment_option=payment_option)

            print('------------------------------',count1, '================', count2)
            if count1 and count2:
                data_saved = "data_saved"
                return render(request, 'orders/order/paid_success.html', {})



        else:
            print('----------error----------------', order_form.errors)
            print('----------error----------------', sales_form.errors)

    # print(sales_form.cleaned_data)
    # print(order_form.cleaned_data)
    return render(request, 'orders/order/create.html', {})


@login_required
def delivery_view(request):
    form = DeliveryDetailsForm(request.POST)
    data_saved = False
    print('nothing request.user============================================', request.user)
    if request.method == 'POST':

        form = DeliveryDetailsForm(request.POST)

        if form.is_valid():
            print('-------post---', form.cleaned_data)

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

        else:
             print('----------error----------------', form.errors)

    else:
        print("GET REQUEST ...........................")

        if DeliveryDetailsModel.objects.filter(username=request.user).exists():
            user_details = DeliveryDetailsModel.objects.get_queryset()
            print(user_details, ' get')

    return render(request, 'cart/cart_details.html', {'form': form, 'data_saved': data_saved})


def generate_order_id():
    from random import randrange
    import datetime
    order_id = randrange(10)

    return 'ODR{}'.format(datetime.datetime.now())

@login_required
def confirm_payment(request):
    # query api to confirm payment
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    if DeliveryDetailsModel.objects.filter(username=request.user).exists():
            delivery_details = DeliveryDetailsModel.objects.filter(username=request.user).values()[0]
            print(delivery_details, ' get')

            return render(request, 'cart/cart_details.html', {'cart': cart, 'delivery_details': delivery_details})

    return render(request, 'cart/cart_details.html', {'cart': cart, 'delivery_details': ''})


    # return render(request, 'orders/order/create_new_address.html', {})


# @login_required
# def make_orders(request):
#     if request.method == 'POST':
#         print('............................ in post')
#         form = OrdersForm(request.POST)
#         if form.is_valid():
#             print('............................ in post, form valid')
#
#             order = form.save()
#
#             return render(request, 'orders/order/purchase.html', {'order': order})
#     else:
#         print('............................ in get')
#         form = OrdersForm()
#         purchase = form.save()
#
#         return render(request, 'orders/order/purchase.html', {'purchase': purchase})




