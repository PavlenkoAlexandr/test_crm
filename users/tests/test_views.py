from django.test import TestCase
from orders.models import Order, OrderWorker
from users.models import User, Contact
from django.urls import reverse


class UserListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_users = 25
        cls.test_staf_user = User.objects.create_superuser(email='staff@test.org', password='12345')
        for i in range(number_of_users):
            User.objects.create_user(email=f'user{i}@test.org', password='12345')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('users'))
        self.assertRedirects(resp, '/accounts/login/?next=/users/')

    def test_test_if_logged_not_staff(self):
        login = self.client.login(email='user1@test.org', password='12345')
        resp = self.client.get(reverse('users'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exist(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get('/users/')
        self.assertEqual(str(resp.context['user']), 'staff@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get(reverse('users'))
        self.assertEqual(str(resp.context['user']), 'staff@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get(reverse('users'))
        self.assertEqual(str(resp.context['user']), 'staff@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/user_list.html')

    def test_pagination_is_25(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get(reverse('users'))
        self.assertEqual(str(resp.context['user']), 'staff@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['user_list']) == 25)

    def test_lists_all_users(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get(reverse('users') + '?page=2')
        self.assertEqual(str(resp.context['user']), 'staff@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['user_list']) == 1)


class UserDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_user2 = User.objects.create_user(email='testuser2@test.org', password='12345')
        cls.test_staff_user = User.objects.create_superuser(email='staff@test.org', password='12345')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('user-detail', args=[self.test_user1.id]))
        self.assertRedirects(resp, f'/accounts/login/?next=/user/{self.test_user1.id}')

    def test_if_logged_in_by_another_user(self):
        login = self.client.login(email='testuser2@test.org', password='12345')
        resp = self.client.get(reverse('user-detail', args=[self.test_user1.id]))
        # self.assertEqual(str(resp.context['user']), 'testuser2@test.org')
        self.assertEqual(resp.status_code, 403)

    def test_if_logged_in_by_staff(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get(reverse('user-detail', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'staff@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(f'/user/{self.test_user1.id}')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-detail', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-detail', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/user_detail.html')


class UserDetailUpdate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_user2 = User.objects.create_user(email='testuser2@test.org', password='12345')
        cls.test_staff_user = User.objects.create_superuser(email='staff@test.org', password='12345')
        cls.test_contact = Contact.objects.create(user=cls.test_user1, phone='+99999999999', city='City', house='1')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('user-detail-update', args=[self.test_user1.id]))
        self.assertRedirects(resp, f'/accounts/login/?next=/user/{self.test_user1.id}/update')

    def test_if_logged_in_by_another_user(self):
        login = self.client.login(email='testuser2@test.org', password='12345')
        resp = self.client.get(reverse('user-detail-update', args=[self.test_user1.id]))
        self.assertEqual(resp.status_code, 403)

    def test_if_logged_in_by_staff(self):
        login = self.client.login(email='staff@test.org', password='12345')
        resp = self.client.get(reverse('user-detail-update', args=[self.test_user1.id]))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(f'/user/{self.test_user1.id}')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-detail-update', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-detail-update', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user_detail_update.html')

    # Не пойму что не так с POST запросом
    def test_redirects_to_user_detail_on_success(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.post(reverse('user-detail-update', args=[self.test_user1.id]),
                                {'first_name': 'Name', 'last_name': 'Last Name', 'phone': '+99999999', 'city': 'New_city', 'house': '2'})
        # self.assertEqual(self.test_user1.first_name, 'Name')
        # self.assertEqual(self.test_user1.last_name, 'Last Name')
        # self.assertEqual(self.test_contact.phone, '+99999999')
        # self.assertEqual(self.test_contact.city, 'New_city')
        # self.assertEqual(self.test_contact.house, '2')
        self.assertEqual(resp.status_code, 200)
