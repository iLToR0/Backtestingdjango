# backtestapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('ejecutar', views.ejecutar_backtest, name='ejecutar_backtest'),
    path('home', views.home, name='inicio'),
]
