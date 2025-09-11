from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Comment
from .forms import (
    ProductForm,
    CustomUserCreationForm,
    UserUpdateForm,
    CommentForm
)
from django.views.decorators.http import require_POST
from .forms import CheckoutForm
from .models import Order, OrderItem
from .models import ProductImage
from django.http import HttpResponseForbidden

# 🏠 Головна сторінка зі списком товарів + пошук
def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category_id and category_id.isdigit():
        products = products.filter(category__id=category_id)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None
    })


# 📦 Детальна інформація про товар + коментарі
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product).order_by('-created_at')
    images = ProductImage.objects.filter(product=product)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.product = product
            comment.save()
            return redirect('product_detail', pk=product.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'products/product_detail.html', {
    'product': product,
    'comments': comments,
    'comment_form': comment_form,
    'images': images  # не обов’язково, бо в шаблоні можна через product.productimage_set.all
})

# ➕ Створення товару
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()

            # Обробка додаткових зображень
            for image_file in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image_file)

            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})


# ✏️ Редагування товару
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Заборона редагування чужого товару
    if request.user != product.author:
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Додаткові зображення
            for image_file in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image_file)

            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
    })


# 🗑 Видалення товару
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.author:
        return HttpResponseForbidden("⛔ Ви не маєте доступу до видалення цього товару.")

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# 👤 Реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# 👤 Перегляд профілю
@login_required
def profile(request):
    user = request.user
    products = Product.objects.filter(author=user)
    return render(request, 'products/profile.html', {'user': user, 'products': products})


# ⚙️ Редагування профілю
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})


# 📝 Альтернативне редагування профілю
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'products/profile_edit.html', {'form': form})


# 🛒 Додати товар у кошик
@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    cart[str(product.pk)] = cart.get(str(product.pk), 0) + 1
    request.session['cart'] = cart

    return redirect('view_cart') 


# 🧾 Перегляд кошика
def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.pk)]
        subtotal = quantity * product.price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })
def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart_detail')
def cart_decrease(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        if cart[str(pk)] > 1:
            cart[str(pk)] -= 1
        else:
            cart.pop(str(pk))
        request.session['cart'] = cart
    return redirect('cart_detail')
def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart_detail')
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys())
    
    if not products:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                total_price=0  # тимчасово, перерахуємо нижче
            )

            total = 0
            for product in products:
                quantity = cart[str(product.pk)]
                price = product.price
                subtotal = price * quantity
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += subtotal

            order.total_price = total
            order.save()

            # Очистити кошик
            request.session['cart'] = {}

            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(request, 'products/checkout.html', {
        'form': form,
        'cart': cart,
        'products': products
    })


def order_success(request):
    return render(request, 'products/order_success.html')
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/my_orders.html', {'orders': orders})
@login_required
def product_image_delete(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    
    if image.product.author != request.user:
        return HttpResponseForbidden("Ви не маєте доступу до цього зображення.")
    
    product_pk = image.product.pk
    image.delete()
    return redirect('product_update', pk=product_pk)
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'products/cart.html', {'cart': cart})








