from django.http import Http404
from django.shortcuts import render

from .data import CATEGORIES, PRODUCTS


def index(request):
    featured = PRODUCTS[:4]
    return render(
        request,
        "shop/index.html",
        {"categories": CATEGORIES, "featured": featured},
    )


def catalog(request, slug=None):
    if slug:
        items = [p for p in PRODUCTS if p["category"] == slug]
        current = next((c for c in CATEGORIES if c["slug"] == slug), None)
        if current is None:
            raise Http404("Категория не найдена")
    else:
        items = PRODUCTS
        current = None
    return render(
        request,
        "shop/catalog.html",
        {
            "products": items,
            "categories": CATEGORIES,
            "current": current,
            "slug": slug,
        },
    )


def product_detail(request, pid):
    item = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not item:
        raise Http404("Товар не найден")
    related = [p for p in PRODUCTS if p["category"] == item["category"] and p["id"] != pid][:3]
    return render(
        request,
        "shop/product.html",
        {"product": item, "related": related},
    )


def about(request):
    return render(request, "shop/about.html")


def contacts(request):
    return render(request, "shop/contacts.html")


def page_not_found(request, exception):
    return render(request, "shop/404.html", status=404)
