from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from crm import telegram_bot
from orders.filters import OrderFilter
from orders.forms import CustomerOrderForm, StaffOrderForm, OrderWorkerForm, OrderCreateForm
from orders.models import Order, OrderWorker
from users.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 10

    def get_filter(self):
        filter = OrderFilter(self.request.GET, queryset=Order.objects.all())
        return filter

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        filter = self.get_filter()
        context['filter'] = filter
        return context

    def get_queryset(self):
        if self.request.user:
            if not self.request.user.is_staff:
                id = self.request.user.id
                return Order.objects.filter(customer_id=id).order_by('updated_date')
            else:
                return super().get_queryset()


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(order_id=self.kwargs['pk'])
        if not self.request.user.is_staff and self.request.user.id != order.customer_id_id:
            return HttpResponse('<h1>403 Forbidden</h1>', status=403,)
        else:
            return super().get(self, request, *args, **kwargs)


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order

    template_name = 'orders/user_order_list.html'
    paginate_by = 10
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(UserOrderListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        filter = OrderFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        context['lookup_user'] = User.objects.get(id=pk)
        return context

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if self.request.user:
            if not self.request.user.is_staff and self.request.user.id != int(pk):
                return []
            else:
                lookup_user = User.objects.get(id=pk)
                if lookup_user.is_staff:
                    return Order.objects.filter(orderworker__worker_id=pk).order_by('updated_date')
                else:
                    return Order.objects.filter(customer_id=pk).order_by('updated_date')


class OrderCreate(LoginRequiredMixin, CreateView):

    model = Order
    fields = 'customer_id', 'order_type', 'description',

    def get_form_class(self):
        form = super().get_form_class()
        form.base_fields['customer_id'].disabled = True
        form.base_fields['customer_id'].initial = self.request.user.id
        return form


@login_required
def order_create_by_staff(request):

    if not request.user.is_staff:
        return HttpResponse('<h1>403 Forbidden</h1>', status=403, )

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)

        if order_form.is_valid():
            new_data = order_form.save()
            new_data.save()
            return HttpResponseRedirect(reverse('order-detail', args=[new_data.order_id]))

    else:
        order_form = OrderCreateForm()

    context = {'order_form': order_form}
    return render(request, 'order_staff_create.html', context)


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order

    def get_form_class(self):
        return CustomerOrderForm

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(order_id=self.kwargs['pk'])
        if not self.request.user.is_staff and self.request.user != order.customer_id:
            return HttpResponse('<h1>403 Forbidden</h1>', status=403,)
        else:
            return super().get(self, request, *args, **kwargs)


@login_required
def order_update_by_staff(request, pk):

    if not request.user.is_staff:
        return HttpResponse('<h1>403 Forbidden</h1>', status=403, )

    lookup_order = Order.objects.get(order_id=pk)
    try:
        order_worker = OrderWorker.objects.get(order_id=pk)
    except ObjectDoesNotExist:
        order_worker = OrderWorker.objects.create(order_id=lookup_order)

    if request.method == 'POST':
        order_form = StaffOrderForm(request.POST, instance=lookup_order)
        order_worker_form = OrderWorkerForm(request.POST, instance=order_worker)

        if order_form.is_valid() and order_worker_form.is_valid():
            new_data = order_form.save(commit=False)
            new_data.save()
            worker = order_worker_form.save()
            worker.save()

            if new_data.customer_id.is_sub:
                message = f'Order #{new_data.order_id} {new_data.get_order_type_display()}\n' \
                          f'Status: {new_data.get_status_display()} ' \
                          f'{new_data.updated_date.strftime("%d %b, %Y - %Hh%Mm")}'
                telegram_bot.send_message(new_data.customer_id.contact.chat_bot_id, message)

            return HttpResponseRedirect(reverse('order-detail', kwargs={'pk': pk}))

    else:
        order_form = StaffOrderForm(instance=lookup_order)
        order_worker_form = OrderWorkerForm(instance=order_worker)

    context = {'order_form': order_form, 'order_worker_form': order_worker_form, 'lookup_order': lookup_order, 'pk': pk}
    return render(request, 'order_staff_update.html', context)


class OrderDelete(LoginRequiredMixin, DeleteView):

    model = Order
    success_url = reverse_lazy('orders')
