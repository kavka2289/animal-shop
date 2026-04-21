from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    desc = models.TextField(blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=200)
    short = models.CharField(max_length=300, blank=True)
    price = models.PositiveIntegerField()
    image_key = models.SlugField(
        max_length=64,
        blank=True,
        help_text="Ключ для CSS-класса превью (например dog-food). Файлы лежат в static/shop/img/products/.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PAID = "paid", "Оплачен"
        CANCELLED = "cancelled", "Отменён"

    user = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)

    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Заказ #{self.pk}"

    @property
    def total(self) -> int:
        return sum(i.total for i in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(help_text="Цена за единицу на момент заказа")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    @property
    def total(self) -> int:
        return self.qty * self.price
