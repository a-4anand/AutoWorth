from django.urls import path
from django.urls import path
from . import views

urlpatterns = [

    path('', views.register_view, name='register'),  # User registration form
    path('index/', views.index, name='index'),  # Home/index view
    path('login/', views.login_view, name='login'),  # Login form
    path('index/main/logout_view/',views.logout_view,name='logout'),
    path('index/main/index-2/', views.index2, name='index2'),  # View for index-2
    path('index/main/index-3/', views.index3, name='index3'),  # View for index-3
    path('index/main/index-6/', views.index6, name='index6'),  # View for index-6
    path('index/main/news/', views.fetch_news, name='fetch_news'),  # Fetch Indian automobile news
    path('predict/', views.predict_price, name='predict_price'),  # Prediction of car price



]



    # path('login/', views.login_view, name='login'),  # Add your login view as well
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Add more paths as needed

    # Updated URL pattern

