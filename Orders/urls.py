
from django.urls import path
from . import views
from .views import*

urlpatterns = [
    path('place_order/',place_order, name='place_order'),
    path('payments/', payments, name='payments'),
    path("razorpay-payment/", views.razorpay_payment, name="razorpay_payment"),
    path("razorpay/success/", views.razorpay_success, name="razorpay_success"),
    path("order_complete/", order_complete, name='order_complete')

]
