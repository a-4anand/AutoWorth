from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('main/index-2/', views.index2, name='index2'),  # Updated URL pattern
]