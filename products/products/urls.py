from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import order_success
from .views import my_orders

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),

    # 👤 Профіль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(
        template_name='products/password_change.html',
        success_url='/profile/'
    ), name='password_change'),

    # 🛒 Кошик
    path('<int:pk>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/decrease/<int:pk>/', views.cart_decrease, name='cart_decrease'),
    path('cart/', views.view_cart, name='cart_detail'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('my-orders/', my_orders, name='my_orders'),
    path('product-image/<int:pk>/delete/', views.product_image_delete, name='product_image_delete'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]








