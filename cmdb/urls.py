from django.urls import path
from . import views

urlpatterns = [
    path('', views.assets_list, name="assets_list"),
]
