from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("reviews/", views.ReviewsView.as_view(), name="reviews"),
    path("faq/", views.FAQView.as_view(), name="faq"),
]
