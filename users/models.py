import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse

USER_TYPE_CHOICES = (
    (True, 'worker'),
    (False, 'customer'),

)


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField('email', unique=True, blank=False, null=False)
    first_name = models.CharField('first name', max_length=20)
    last_name = models.CharField('last name', max_length=25)
    is_sub = models.BooleanField('mail subscribe status', default=False)
    is_staff = models.BooleanField('staff status', default=False, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Contact(models.Model):

    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='City')
    street = models.CharField(max_length=100, verbose_name='Street', default='')
    house = models.CharField(max_length=15, verbose_name='House', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Structure', blank=True, default='')
    building = models.CharField(max_length=15, verbose_name='Building', blank=True, default='')
    apartment = models.CharField(max_length=15, verbose_name='Apartment', blank=True, default='')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    telegram = models.CharField(max_length=150, verbose_name='Telegram', null=True)
    chat_bot_id = models.TextField(verbose_name='chat_bot_id', null=True)

    def __str__(self):
        return f'{self.phone}'

    def get_address(self):
        return f'{self.city} {self.street} {self.house} {self.structure} {self.building} {self.apartment}'
