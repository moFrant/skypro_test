"""Тестирование автонаполнение БД."""
import random

import pytest
from django.core.management import call_command
from freezegun import freeze_time

from wares.models import Category, Wares


@pytest.mark.django_db
@pytest.mark.parametrize("wares, categories, orders, today, stat_month, stat_current", (
        (1, 1, 1, "2023-10-03", 1, 1),
        (1, 1, 10, "2023-10-03", 10, 3),
        (30, 17, 100, "2023-10-31", 31, 61)
))
def test_auto_fill(wares: int, categories: int, orders: int, today: str, stat_month: int, stat_current: int):
    """Вызов команды автонаполнения БД."""

    with freeze_time(today):
        call_command("fill_db", wares, categories, orders)

        assert Category.objects.count() == categories
        assert Wares.objects.count() == wares

        category = Category.objects.first()
        wares_category = category.wares.all()
        one_wares_category = random.choice(wares_category)

        assert one_wares_category.monthly_statistics <= stat_month
        assert one_wares_category.statistics_for_current_month <= stat_current
