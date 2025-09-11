from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Comment, ProductImage

# 📸 Додаткові зображення (inline)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# 📦 Товари
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'author', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
    inlines = [ProductImageInline]

# 📂 Категорії
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 💬 Коментарі
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)

# 🧾 Елементи замовлення (вкладені в замовлення)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# 🛒 Замовлення
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'created_at', 'total_price', 'user', 'status')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'total_price')
    fields = ('full_name', 'address', 'phone', 'user', 'status', 'created_at', 'total_price')

# 🔓 Додаткові зображення напряму (не обов’язково)
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')





