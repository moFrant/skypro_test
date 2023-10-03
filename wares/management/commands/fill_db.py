import random
from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.management import BaseCommand

from wares.models import Category, Wares, Order


class Command(BaseCommand):
    help = "Наполнение базы тестовыми данными."

    def add_arguments(self, parser):
        parser.add_argument("amount_wares", type=int)
        parser.add_argument("amount_category", type=int)
        parser.add_argument("amount_orders", type=int)

    def handle(self, *args, amount_wares: int, amount_category: int, amount_orders: int, **options):
        categories = []
        wares_list = []
        today = date.today()

        for i in range(1, amount_category + 1):
            category = Category(name=f"Тестовая категория {i}")
            category.save()
            categories.append(category)

        for i in range(1, amount_wares + 1):
            category = random.choice(categories)
            wares = Wares(name=f"Тестовый товар {i}",
                          category=category,
                          price=random.randint(1, 1000))
            wares.save()
            wares_list.append(wares)

        for _ in range(amount_orders):
            wares = random.choice(wares_list)
            order = Order(create_at=today)
            order.save()
            order.wares.add(wares)
            today -= relativedelta(days=1)
