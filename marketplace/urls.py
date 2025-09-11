from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Основний додаток (усі шляхи з products.urls)
    path('', include('products.urls')),

    # Аутентифікація
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    # 🛒 Кошик (додаткові маршрути — якщо ще не в products.urls)
    path('<int:pk>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]

# Для медіафайлів у режимі DEBUG (зображення товарів, тощо)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







