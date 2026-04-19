from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog/", views.catalog, name="catalog"),
    path("catalog/<slug:slug>/", views.catalog, name="catalog_category"),
    path("product/<int:pid>/", views.product_detail, name="product"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
]
