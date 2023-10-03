from django.contrib import admin

from wares.models import Wares, Category, Order


@admin.register(Wares)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'price']


@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class AuthorAdmin(admin.ModelAdmin):
    pass
