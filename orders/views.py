from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct, Payment
from store.models import Product
# Create your views here.

def payments(request):

        # cart_item = CartItem.objects.get(id=item.id)
        # product_variation = cart_item.variations.all()
        # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        # orderproduct.save()


    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or euqal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')


    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        #if 1 == 1:
        # to use cleaned_data you should use is_valid() before!
        # try with make migrations!!
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            #data.address_line_2 = form.cleaned_data['address_line_2']
            #data.country = form.cleaned_data['country']
            #data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                	'order': order,
                    'cart_items': cart_items,
                    'total': total,
            }

            # Move the cart items to Order Product table
            cart_items_2 = CartItem.objects.filter(user=request.user)

            for item in cart_items_2:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                #orderproduct.payment = payment
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()

                # Reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            # Clear cart
            CartItem.objects.filter(user=request.user).delete()





            return render(request, 'orders/payments.html', context)
        else:
            #print(form.errors)
            return redirect('store')


def order_complete(request):
    return render(request, 'orders/order_complete.html')
