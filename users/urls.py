from django.conf.urls import url
from django.urls import path
from users import views


urlpatterns = [
    url(r'^users/$', views.UserListView.as_view(), name='users'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^user/(?P<pk>\d+)/update$', views.user_detail_update, name='user-detail-update'),
    url(r'^accounts/register$', views.register, name='register'),
    url(r'^user/confirm_subscribe$', views.subscribe_to_updates, name='confirm-subscribe'),
]
