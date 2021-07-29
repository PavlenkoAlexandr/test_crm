import django_filters
from users.models import User, USER_TYPE_CHOICES


class UserFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(UserFilter, self).__init__(*args, **kwargs)
        self.queryset = User.objects.select_related('contact').all()

    is_staff = django_filters.MultipleChoiceFilter(choices=USER_TYPE_CHOICES)
    email = django_filters.CharFilter(lookup_expr='icontains')
    contact__phone = django_filters.CharFilter(label='Phone contains:', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['is_staff', 'email', 'contact__phone']
