from django.urls import path
from django.urls import path

from .views import index, index2, index3, index6, register, predict

urlpatterns = [
    path('', index, name='index'),
    path('main/index-2/', index2, name='index2'),
    path('main/index-3/', index3, name='index3'),
    path('main/index-6/', index6, name='index6'),
    path('main/register/', register, name='register'),
    path('main/predict/', predict, name='predict'),
]



    # path('login/', views.login_view, name='login'),  # Add your login view as well
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Add more paths as needed

    # Updated URL pattern

