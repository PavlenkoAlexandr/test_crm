from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    url(r'^order/(?P<pk>\d+)$', views.OrderDetailView.as_view(), name='order-detail'),
    url(r'^user/(?P<pk>\d+)/orders/$', views.UserOrderListView.as_view(), name='user-orders'),
]

urlpatterns += [
    url(r'^order/create/$', views.OrderCreate.as_view(), name='order-create'),
    url(r'^order/(?P<pk>\d+)/update/$', views.OrderUpdate.as_view(), name='order-update'),
    url(r'^order/(?P<pk>\d+)/delete/$', views.OrderDelete.as_view(), name='order-delete'),
    url(r'^order/(?P<pk>\d+)/staff_update/$', views.order_update_by_staff, name='order-staff-update'),
    url(r'^order/staff_create/$', views.order_create_by_staff, name='order-staff-create')
]
