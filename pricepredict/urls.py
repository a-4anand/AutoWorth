from django.urls import path
from django.urls import path
from . import views
from .views import fetch_news
urlpatterns = [
    path('', views.index, name='index'),
    path('main/index-2/', views.index2, name='index2'),
    path('main/index-3/', views.index3, name='index3'),
    path('main/index-6/', views.index6, name='index6'),
    path('main/register/', views.register, name='register'),
    path('news/', fetch_news, name='fetch_news'),
    path('predict/', views.predict_price, name='predict_price'),
    path('alternative_action/', views.alternative_action, name='alternative_action'),



]



    # path('login/', views.login_view, name='login'),  # Add your login view as well
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Add more paths as needed

    # Updated URL pattern

