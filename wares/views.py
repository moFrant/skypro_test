from django.views.generic import ListView

from wares.models import Wares


class WareListView(ListView):
    """Список товаров"""

    model = Wares
    template_name = 'main.htm'
