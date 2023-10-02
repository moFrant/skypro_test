"""Тестирование моделей для работы с товарами."""
from datetime import date

import pytest

from wares.models import Category, Wares, Order


@pytest.mark.django_db
def test_create_models():
    """Тест создания записей."""

    assert Category.objects.count() == 0
    category = Category(name="Тестовая категория")
    category.save()

    assert Category.objects.count() == 1
    category = Category.objects.first()
    assert category.name == "Тестовая категория"

    assert Wares.objects.count() == 0
    wares = Wares(name="Тестовый товар",
                  category=category,
                  price=100.00)
    wares.save()

    assert Wares.objects.count() == 1
    wares = Wares.objects.first()
    assert wares.name == "Тестовый товар"
    assert wares.category == category

    assert Order.objects.count() == 0
    order = Order()
    order.save()
    order.wares.add(wares)
    order.save()

    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order.create_at == date.today()
    assert order.wares.count() == 1
    wares = order.wares.first()
    assert wares.name == 'Тестовый товар'


@pytest.mark.django_db
def test_back_related():
    """Проверка обратных связей."""

    category = Category(name="Тестовая категория")
    category.save()
    wares = Wares(name="Тестовый товар",
                  category=category,
                  price=100.00)
    wares.save()
    order = Order()
    order.save()
    order.wares.add(wares)
    order.save()

    # Получение товаров по категории
    category = Category.objects.filter(name="Тестовая категория").first()
    wares = category.wares.all()
    assert wares.count() == 1
    assert wares.first().name == 'Тестовый товар'

    # Получение заказов по товару
    wares = Wares.objects.filter(name="Тестовый товар").first()
    orders = wares.orders.all()
    assert orders.count() == 1
    order = orders.first()
    assert order.create_at == date.today()
