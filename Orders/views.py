from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from Carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from Store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from Store.models import *


from jjcollection.settings import RAZORPAY_KEY_ID
from django.views.decorators.csrf import csrf_exempt
import razorpay

@csrf_exempt
def razorpay_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })
        except:
            return JsonResponse({"status": "failure"}, status=400)

        # Get order object using order_number from frontend
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=data["order_number"])

        # Save payment details
        payment = Payment.objects.create(
            user=request.user,
            payment_id=data["razorpay_payment_id"],
            payment_method="Razorpay",
            amount_paid=order.order_total,
            status="COMPLETED",
        )

        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move cart items to OrderProduct
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Variations
          
            orderproduct.save()

            # Decrease stock
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send confirmation email
        mail_subject = "Thank you for your order!"
        message = render_to_string("order_recieved_email.html", {
            "user": request.user,
            "order": order,
        })
        EmailMessage(mail_subject, message, to=[request.user.email]).send()

        return JsonResponse({
            "status": "success",
            "order_number": order.order_number,
            "payment_id": payment.payment_id
        })
def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (5 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate unique order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            # ---------- Razorpay Order Creation ----------
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                "amount": int(grand_total * 100),  # in paise
                "currency": "INR",
                "payment_capture": 1
            })
            razorpay_order_id = razorpay_order["id"]

            # Save Razorpay order ID in Order model (optional but recommended)
            order.razorpay_order_id = razorpay_order_id
            order.save()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
                'currency': 'INR',
            }
            return render(request, 'payments.html', context)
        else:
            return redirect('checkout')
        

@csrf_exempt
def razorpay_success(request):
    if request.method == "POST":
        data = json.loads(request.body)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature(data)
            # save payment to your database
            return JsonResponse({"status": "success", "order_number": "12345", "payment_id": data["razorpay_payment_id"]})
        except:
            return JsonResponse({"status": "failure"})        


def payments(request):
    # Suppose you have grand_total already calculated
    grand_total = 500  # example ₹500

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        "amount": int(grand_total * 100),  # in paise
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,   # ✅ send this to template
        "razorpay_order_id": razorpay_order["id"],
        "grand_total": grand_total,
    }
    return render(request, "payments.html", context)

def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    try:
        order = get_object_or_404(Order, order_number=order_number, is_ordered=True)
        payment = get_object_or_404(Payment, payment_id=payment_id)
        ordered_products = OrderProduct.objects.filter(order=order)

        subtotal = 0
        # ✅ Calculate total_price for each item
        for item in ordered_products:
            item.total_price = item.product_price * item.quantity  # calculate total for each product
            subtotal += item.total_price

        context = {
            'order': order,
            'payment': payment,
            'ordered_products': ordered_products,
            'subtotal': subtotal,
            'order_number': order_number,
            'payment_id': payment_id,
        }
        return render(request, 'order_complete.html', context)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')
