from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Product, Brand
from cart.forms import CartAddProductForm
from cart.models import CartItemsModel
from cart.cart import Cart
from django.db.models import Sum


def product_list(request, category_slug=None):
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
        'cart': cart,
        'category': category,
        'categories': categories,
        'products': products
        }

    return render(request, 'shop/product_list.html', context)




def product_detail(request, id, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # get current stock value
    products = Product.objects.filter(id=id).values()[0]
    print('................in product detail')
    if CartItemsModel.objects.filter(product=products['name']).exists():
        items = CartItemsModel.objects.filter(product=products['name']).aggregate(Sum('quantity'))
        items_from_cart = int(items['quantity__sum'])
    else:
        items_from_cart = 0

    stock_from_products = int(products['stock'])
    available_stock = range(1, (stock_from_products - items_from_cart) +1)
    description = Product.objects.filter(id=id).values('description')[0]
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    context = {
        'cart': cart,
        'product': product,
        'products': products,
        'cart_product_form': cart_product_form,
        'available_stock': available_stock,
    }
    return render(request, 'shop/product_details.html', context)


def searchresult(request):
    cart = Cart(request)
    if request.method == 'GET':
        query = request.GET.get('q', '')

        if len(query) == 0:
            return redirect('shop:product_list')

        if query is not None:

            # lookups = Q(name__icontains=query) | Q(slug__icontains=query)
            #
            # results = Product.objects.filter(lookups).distinct()

            results = Product.objects.filter(name__icontains=query)
            search_item = Product.objects.filter(name__icontains=query).values('slug', 'brand', 'category')
            if search_item:


                search_item_cat = search_item[0]['category']
                search_item_brand = search_item[0]['brand']
                related_by_category = Product.objects.filter(category=search_item_cat)
                related_by_brand = Product.objects.filter(brand=search_item_brand)

                list1 = []
                for item in results.values_list('name', flat=True):
                    list1.append(item)
                # print(list1)

                list2 = []
                for item in related_by_category.values_list('name', flat=True):
                    list2.append(item)
                # print(list2)

                list3 = []
                for item in related_by_brand.values_list('name', flat=True):
                    list3.append(item)
                # print(list3)

                list4 = [item for item in list2 if item not in list1]
                # print(list4)

                list5 = [item for item in list4 if item not in list3]
                print(list5)

                res = Product.objects.filter(name__in=list5)

                print('.......................................')
                print(res)
                print(results)
            else:
                results = ''
                res =''
      
            context = {
                'cart': cart,
                'results': results,
                'related_by_category': res,
                # 'related_by_brand': related_by_brand,
                      }

            return render(request, 'shop/search_results.html', context)
        else:
            return render(request, 'shop/product_list.html')
    else:
        return render(request, 'shop/product_list.html')
