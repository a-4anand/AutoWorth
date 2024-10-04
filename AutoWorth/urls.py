"""
URL configuration for AutoWorth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# root urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # path('auth/', include('auth_app.urls', namespace='auth_app')),  # Example namespace
    # path('', lambda request: redirect('auth_app:register')),  # Redirect root URL to register page
    path('', include('pricepredict.urls')),  # Include
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='/accounts/register/')),  # Redirect to the registration page
    # path('accounts/', include('accounts.urls')),  # Include URLs from the accounts app
    # path('index/',include('pricepredict.urls')),  # Add this line

]

