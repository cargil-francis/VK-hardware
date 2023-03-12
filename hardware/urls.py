from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'hardware'

urlpatterns = [  
    path('', views.index, name = 'index'),

    path('product/<slug:slug>/', views.detail, name ='product'),
    path('category/',views.all_categories, name ='categories'),
    path('category/<slug:slug>/',views.category_products, name ='categories_product'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('cart/', views.cart, name='cart'),
    path('success/', views.success, name='success'),

    path('user_profile/', views.profile, name="profile"),
    path('add-address/', views.AddressView.as_view(), name="add-address"),
    path('remove-address/<int:id>/', views.remove_address, name="remove-address"),
    
  
   



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)