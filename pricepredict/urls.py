from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('main/index-2/', views.index2, name='index2'),
    path('main/index-3/', views.index3, name='index3'),
    path('main/index-6/', views.index6, name='index6'),
    path('main/register/', views.register, name='register'),
    path('predict/', views.predict, name='predict'),

    # path('login/', views.login_view, name='login'),  # Add your login view as well
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Add more paths as needed

    # Updated URL pattern
]
