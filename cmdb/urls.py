from django.urls import path
from . import views

urlpatterns = [
    path('', views.assets_list, name="assets_list"),
    path('add_host/', views.add_host, name="add_host"),
]
