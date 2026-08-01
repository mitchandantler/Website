from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path("booking/", views.BookingView.as_view(), name="booking"),
    path("order-online/", views.OrderOnlineView.as_view(), name="order_online"),
]
