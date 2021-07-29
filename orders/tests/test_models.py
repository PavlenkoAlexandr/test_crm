from django.test import TestCase
from orders.models import Order, OrderWorker
from users.models import User


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_order = Order.objects.create(customer_id=cls.test_user1, )
        cls.test_order_worker = OrderWorker.objects.create(order_id=cls.test_order, worker_id=cls.test_user1)

    def test_order_str_method(self):
        expected_result = f'Order #{self.test_order.order_id} ' \
                          f'({self.test_order.get_status_display()}, ' \
                          f'{self.test_order.updated_date.strftime("%d %b, %Y - %Hh%Mm")})'
        self.assertEqual(expected_result, str(self.test_order))

    def test_order_get_absolute_url(self):
        self.assertEqual(self.test_order.get_absolute_url(), f'/order/{self.test_order.order_id}')

    def test_orderworker_str_method(self):
        expected_result = f'Order #{self.test_order_worker.order_id_id}, {self.test_order_worker.worker_id}'
        self.assertEqual(expected_result, str(self.test_order_worker))
