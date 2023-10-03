from datetime import date

from dateutil.relativedelta import relativedelta
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

    def _statistics(self, begin_period: date, end_period: date) -> int:
        """Вспомогательный метод для получения статистики заказов по товару."""

        orders = self.orders.filter(create_at__gte=begin_period, create_at__lte=end_period)
        return orders.count()

    @property
    def monthly_statistics(self) -> int:
        """Статистика за месяц."""

        end_period = date.today()
        begin_period = end_period - relativedelta(months=1)
        return self._statistics(begin_period, end_period)

    @property
    def statistics_for_current_month(self) -> int:
        """Статистика за текущий месяц."""

        end_period = date.today()
        begin_period = end_period - relativedelta(day=1)
        return self._statistics(begin_period, end_period)


class Order(models.Model):
    """Заказы."""

    wares = models.ManyToManyField(Wares, related_name='orders', verbose_name="товары")
    create_at = models.DateField(verbose_name="дата заказа", auto_created=True, default=date.today)

    def __str__(self):
        return f'Заказ {self.pk}'
