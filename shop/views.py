from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, SignUpForm
from .models import Category, Order, OrderItem, Product
from .services.telegram import send_order_to_telegram


def index(request):
    featured = Product.objects.filter(is_active=True).select_related("category")[:4]
    return render(
        request,
        "shop/index.html",
        {"categories": Category.objects.all(), "featured": featured},
    )


def catalog(request, slug=None):
    qs = Product.objects.filter(is_active=True).select_related("category")
    if slug:
        current = get_object_or_404(Category, slug=slug)
        items = qs.filter(category=current)
    else:
        items = qs
        current = None
    return render(
        request,
        "shop/catalog.html",
        {
            "products": items,
            "categories": Category.objects.all(),
            "current": current,
            "slug": slug,
        },
    )


def product_detail(request, pid):
    item = get_object_or_404(Product.objects.select_related("category"), pk=pid, is_active=True)
    related = (
        Product.objects.filter(is_active=True, category=item.category)
        .exclude(pk=item.pk)
        .select_related("category")[:3]
    )
    return render(
        request,
        "shop/product.html",
        {"product": item, "related": related},
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def checkout(request, pid: int):
    product = get_object_or_404(Product, pk=pid, is_active=True)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                customer_name=form.cleaned_data["customer_name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )
            qty = form.cleaned_data["qty"]
            OrderItem.objects.create(order=order, product=product, qty=qty, price=product.price)

            lines = [
                f"Новый заказ #{order.pk}",
                f"Пользователь: {request.user.username} ({request.user.email})",
                f"Имя: {order.customer_name}",
                f"Телефон: {order.phone}",
                f"Адрес: {order.address}",
                "",
                f"Товар: {product.name}",
                f"Количество: {qty}",
                f"Сумма: {order.total} ₽",
            ]
            send_order_to_telegram("\n".join(lines))

            return redirect("order_success", oid=order.pk)
    else:
        initial = {"customer_name": request.user.get_full_name().strip() or request.user.username}
        form = CheckoutForm(initial=initial)

    return render(request, "shop/checkout.html", {"product": product, "form": form})


@login_required
def order_success(request, oid: int):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=oid, user=request.user)
    return render(request, "shop/order_success.html", {"order": order})


def about(request):
    return render(request, "shop/about.html")


def contacts(request):
    return render(request, "shop/contacts.html")


def page_not_found(request, exception):
    return render(request, "shop/404.html", status=404)
