from django import forms
from orders.models import Order, OrderWorker
from users.models import User


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type', 'description']


class StaffOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status', 'order_type', 'description', ]


class OrderWorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderWorkerForm, self).__init__(*args, **kwargs)
        self.fields['worker_id'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = OrderWorker
        fields = ['worker_id']


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['customer_id'].queryset = User.objects.filter(is_staff=False)

    class Meta:
        model = Order
        fields = ['customer_id', 'order_type', 'description', ]
