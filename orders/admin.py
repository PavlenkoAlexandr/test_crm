from django.contrib import admin
from .models import Order, OrderWorker


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderWorker)
class OrderWorkerAdmin(admin.ModelAdmin):
    pass
