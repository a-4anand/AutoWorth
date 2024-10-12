from django.urls import path
from django.urls import path
from . import views

urlpatterns = [

    path('', views.register_view, name='register'),  # User registration form
    path('index/', views.index, name='index'),  # Home/index view
    path('login/', views.login_view, name='login'),  # Login form
    path('index/main/logout_view/',views.logout_view,name='logout'),
    # path('index/main/index-2/', views.index2, name='index2'),  # View for index-2
    path('index/main/index-3/', views.index3, name='index3'),  # View for index-3
    path('index/main/index-6/', views.index6, name='index6'),  # View for index-6
    path('predict/', views.predict_price, name='predict_price'),  # Prediction of car price
    path('express-interest/<int:listing_id>/', views.express_interest, name='express_interest'),#for marketplace
    path('listings/<int:listing_id>/express_interest/', views.express_interest, name='express_interest'),
    path('index/main/listings/', views.view_listings, name='view_listings'),
    path('index/main/listings/create/', views.create_listing, name='create_listing'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),

    # You need to create this view for listing all vehicles



]






