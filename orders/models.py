from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import User


class Order(models.Model):

    ORDER_TYPES = (
        ('R', 'Repair'),
        ('M', 'Maintenance'),
        ('C', 'Consultation'),
    )

    STATUS = (
        ('D', 'DONE'),
        ('P', 'IN_PROGRESS'),
        ('N', 'NEW')
    )

    order_id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    order_type = models.CharField(max_length=1, choices=ORDER_TYPES, default='C')
    status = models.CharField(max_length=1, choices=STATUS, default='N')
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.order_id)])

    def __str__(self):
        return f'Order #{self.order_id} ' \
               f'({self.get_status_display()}, {self.updated_date.strftime("%d %b, %Y - %Hh%Mm")})'


class OrderWorker(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Order #{self.order_id_id}, {self.worker_id}'
