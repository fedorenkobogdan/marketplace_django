from django.urls import path, include

from .views import (
    product_list, product_detail, product_create, product_update, product_delete,
    register, profile, profile_edit,
    add_to_cart, view_cart, cart_remove, cart_decrease, cart_clear,
    checkout, order_success, my_orders, cancel_order,
    product_image_delete, cart_add, cart_detail,
)
from django.contrib.auth import views as auth_views
from .views import test_email
from django.conf.urls.i18n import set_language
urlpatterns = [
    # 📦 Продукти
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<int:pk>/edit/', product_update, name='product_update'),
    path('<int:pk>/delete/', product_delete, name='product_delete'),
    path('product-image/<int:pk>/delete/', product_image_delete, name='product_image_delete'),

    # 👤 Профіль
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(
        template_name='products/password_change.html',
        success_url='/profile/'
    ), name='password_change'),

    # 🛒 Кошик
    path('<int:pk>/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart/decrease/<int:pk>/', cart_decrease, name='cart_decrease'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('checkout/', checkout, name='checkout'),

    # 🧾 Замовлення
    path('order/success/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:order_id>/cancel/', cancel_order, name='cancel_order'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('test-email/', test_email, name='test_email'),
    path('i18n/', include('django.conf.urls.i18n')),
    

]










