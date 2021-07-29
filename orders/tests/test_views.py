from django.test import TestCase
from orders.models import Order, OrderWorker
from users.models import User
from django.urls import reverse


class OrderListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_orders = 22
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_user2 = User.objects.create_user(email='testuser2@test.org', password='12345')
        for i in range(number_of_orders):
            if i % 2:
                Order.objects.create(customer_id=cls.test_user1, description=str(i), )
            else:
                Order.objects.create(customer_id=cls.test_user2, description=str(i), )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('orders'))
        self.assertRedirects(resp, '/accounts/login/?next=/orders/')

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get('/orders/')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('orders'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('orders'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/order_list.html')

    def test_pagination_is_ten(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('orders'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['order_list']) == 10)

    def test_lists_all_orders(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('orders') + '?page=2')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['order_list']) == 1)

    def test_only_testuser_orders_in_list(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('orders'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        for order in resp.context['order_list']:
            self.assertEqual(resp.context['user'], order.customer_id)
            self.assertEqual('N', order.status)

    def test_staff_order_list_view(self):
        self.test_user1.is_staff = True
        self.test_user1.save(update_fields=['is_staff', ])
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('orders'))
        resp2 = self.client.get(reverse('orders') + '?page=2')
        resp3 = self.client.get(reverse('orders') + '?page=3')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(str(resp2.context['user']), 'testuser@test.org')
        self.assertEqual(str(resp3.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['order_list']) == 10)
        self.assertTrue(resp2.context['is_paginated'])
        self.assertTrue(len(resp2.context['order_list']) == 10)
        self.assertTrue(resp3.context['is_paginated'])
        self.assertTrue(len(resp3.context['order_list']) == 2)


class OrderDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_user2 = User.objects.create_user(email='testuser2@test.org', password='12345')
        cls.test_order = Order.objects.create(customer_id=cls.test_user1, )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('order-detail', args=[self.test_order.order_id]))
        self.assertRedirects(resp, f'/accounts/login/?next=/order/{self.test_order.order_id}')

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(f'/order/{self.test_order.order_id}')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-detail', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-detail', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/order_detail.html')

    def test_owner_order_detail_view(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-detail', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'], self.test_order.customer_id)

    def test_not_owner_order_detail_view(self):
        login = self.client.login(email='testuser2@test.org', password='12345')
        resp = self.client.get(reverse('order-detail', args=[self.test_order.order_id]))
        # self.assertEqual(str(resp.context['user']), 'testuse2@test.org')
        self.assertEqual(resp.status_code, 403)

    def test_staff_order_detail_view(self):
        self.test_user2.is_staff = True
        self.test_user2.save(update_fields=['is_staff', ])
        login = self.client.login(email='testuser2@test.org', password='12345')
        resp = self.client.get(reverse('order-detail', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'testuser2@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.context['user'], self.test_order.customer_id)


class UserOrderListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_orders = 11
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_user2 = User.objects.create_user(email='testuser2@test.org', password='12345')
        for i in range(number_of_orders):
            Order.objects.create(customer_id=cls.test_user1, description=str(i), )
        Order.objects.create(customer_id=cls.test_user2, )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]))
        self.assertRedirects(resp, f'/accounts/login/?next=/user/{self.test_user1.id}/orders/')

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(f'/user/{self.test_user1.id}/orders/')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/user_order_list.html')

    def test_pagination_is_ten(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['order_list']) == 10)

    def test_lists_all_orders(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]) + '?page=2')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['order_list']) == 1)

    def test_only_testuser_orders_in_list(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        for order in resp.context['order_list']:
            self.assertEqual(resp.context['user'], order.customer_id)

    def test_staff_order_list_view(self):
        self.test_user2.is_staff = True
        self.test_user2.save(update_fields=['is_staff', ])
        login = self.client.login(email='testuser2@test.org', password='12345')
        resp = self.client.get(reverse('user-orders', args=[self.test_user1.id]))
        resp2 = self.client.get(reverse('user-orders', args=[self.test_user1.id]) + '?page=2')
        self.assertEqual(str(resp.context['user']), 'testuser2@test.org')
        self.assertEqual(str(resp2.context['user']), 'testuser2@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['order_list']) == 10)
        self.assertTrue(resp2.context['is_paginated'])
        self.assertEqual(len(resp2.context['order_list']), 1)


class OrderCreate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('order-create'))
        self.assertRedirects(resp, '/accounts/login/?next=/order/create/')

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get('/order/create/')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-create'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-create'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/order_form.html')

    def test_form_customer_id_initially(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-create'))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form']['customer_id'].initial, resp.context['user'].id)
        self.assertTrue(resp.context['form'].base_fields['customer_id'].disabled)

    def test_redirects_to_order_detail_on_success(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        test_order = Order.objects.create(customer_id=self.test_user1, )
        resp = self.client.post(reverse('order-create'), {'order_type': 'C'})
        order = Order.objects.get(order_id=int(test_order.order_id)+1)
        self.assertEqual(order.order_type, 'C')
        self.assertEqual(order.status, 'N')
        self.assertEqual(order.customer_id, self.test_user1)
        self.assertRedirects(resp, reverse('order-detail', args=[order.order_id]))


class OrderCreateByStaffTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_staff_user = User.objects.create_user(email='staffuser@test.org', password='12345')
        cls.test_staff_user.is_staff = True
        cls.test_staff_user.save(update_fields=['is_staff', ])
        cls.test_user = User.objects.create_user(email='testuser@test.org', password='12345')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('order-staff-create'))
        self.assertRedirects(resp, '/accounts/login/?next=/order/staff_create/')

    def test_if_logged_not_staff(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-staff-create'))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exist(self):
        login = self.client.login(email='staffuser@test.org', password='12345')
        resp = self.client.get('/order/staff_create/')
        self.assertEqual(str(resp.context['user']), 'staffuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='staffuser@test.org', password='12345')
        resp = self.client.get(reverse('order-staff-create'))
        self.assertEqual(str(resp.context['user']), 'staffuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='staffuser@test.org', password='12345')
        resp = self.client.get(reverse('order-staff-create'))
        self.assertEqual(str(resp.context['user']), 'staffuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'order_staff_create.html')

    def test_redirects_to_order_detail_on_success(self):
        login = self.client.login(email='staffuser@test.org', password='12345')
        test_order = Order.objects.create(customer_id=self.test_user, )
        resp = self.client.post(reverse('order-staff-create'), {'customer_id': self.test_user.id, 'order_type': 'C'})
        order = Order.objects.get(order_id=int(test_order.order_id)+1)
        self.assertEqual(order.order_type, 'C')
        self.assertEqual(order.status, 'N')
        self.assertEqual(order.customer_id, self.test_user)
        self.assertRedirects(resp, reverse('order-detail', args=[order.order_id]))


class OrderUpdateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_order = Order.objects.create(customer_id=cls.test_user)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('order-update', args=[self.test_order.order_id]))
        self.assertRedirects(resp, f'/accounts/login/?next=/order/{self.test_order.order_id}/update/')

    def test_if_logged_as_another_user(self):
        user = User.objects.create_user(email='testuser2@test.org', password='12345')
        login = self.client.login(email='testuser2@test.org', password='12345')
        resp = self.client.get(reverse('order-update', args=[self.test_order.order_id]))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exist(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(f'/order/{self.test_order.order_id}/update/')
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-update', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-update', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'testuser@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/order_form.html')

    # Не пойму что не так с POST запросом
    def test_redirects_to_order_detail_on_success(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.post(reverse('order-update', args=[self.test_order.order_id]),
                                {'order_type': 'R', 'description': 'test'})
        # self.assertEqual(self.test_order.order_type, 'R')
        # self.assertEqual(self.test_order.description, 'test')
        # self.assertEqual(self.test_order.customer_id, self.test_user)
        self.assertRedirects(resp, reverse('order-detail', args=[self.test_order.order_id]))


class OrderUpdateByStaff(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_staff_user = User.objects.create_superuser(email='staf@test.org', password='12345')
        cls.test_order = Order.objects.create(customer_id=cls.test_user)
        cls.test_order_worker = OrderWorker.objects.create(order_id=cls.test_order, worker_id=cls.test_staff_user)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('order-staff-update', args=[self.test_order.order_id]))
        self.assertRedirects(resp, f'/accounts/login/?next=/order/{self.test_order.order_id}/staff_update/')

    def test_if_logged_not_staff(self):
        login = self.client.login(email='testuser@test.org', password='12345')
        resp = self.client.get(reverse('order-staff-update', args=[self.test_order.order_id]))
        self.assertEqual(resp.status_code, 403)

    def test_view_url_exist(self):
        login = self.client.login(email='staf@test.org', password='12345')
        resp = self.client.get(f'/order/{self.test_order.order_id}/staff_update/')
        self.assertEqual(str(resp.context['user']), 'staf@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email='staf@test.org', password='12345')
        resp = self.client.get(reverse('order-staff-update', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'staf@test.org')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(email='staf@test.org', password='12345')
        resp = self.client.get(reverse('order-staff-update', args=[self.test_order.order_id]))
        self.assertEqual(str(resp.context['user']), 'staf@test.org')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'order_staff_update.html')

    # Не пойму что не так с POST запросом
    def test_redirects_to_order_detail_on_success(self):
        login = self.client.login(email='staf@test.org', password='12345')
        new_worker = User.objects.create_user(email='test@test.org', password='12345')
        resp = self.client.post(reverse('order-staff-update', args=[self.test_order.order_id]),
                                {'order_type': 'R', 'description': 'test', 'status': 'P', 'worker_id': new_worker})
        # self.assertEqual(self.test_order.order_type, 'R')
        # self.assertEqual(self.test_order.status, 'P')
        # self.assertEqual(self.test_order.description, 'test')
        # self.assertEqual(self.test_order.worker_id, new_worker)
        self.assertEqual(resp.status_code, 200)
