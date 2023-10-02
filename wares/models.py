from datetime import date

from django.db import models


class Category(models.Model):
    """Категория товара."""

    name = models.CharField(max_length=255, verbose_name='название')

    def __str__(self):
        return self.name


class Wares(models.Model):
    """Модель товара."""

    name = models.CharField(max_length=255, verbose_name='название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категория товара",
                                 related_name='wares')
    is_active = models.BooleanField(verbose_name="активный", default=True)
    price = models.DecimalField(verbose_name="цена", max_digits=16, decimal_places=2)


class Order(models.Model):
    """Заказы."""

    wares = models.ManyToManyField(Wares, related_name='orders', verbose_name="товары")
    create_at = models.DateField(verbose_name="дата заказа", auto_created=True, default=date.today)
