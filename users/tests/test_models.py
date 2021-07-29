from django.test import TestCase
from users.models import User, Contact


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(email='testuser@test.org', password='12345')
        cls.test_contact = Contact.objects.create(user=cls.test_user1, city='City', house='1', phone='+9999999999')

    def test_user_str_method(self):
        expect_result = f'{self.test_user1.email}'
        self.assertEqual(expect_result, str(self.test_user1))

    def test_user_get_full_name(self):
        expect_result = f'{self.test_user1.last_name} {self.test_user1.first_name}'
        self.assertEqual(expect_result, self.test_user1.get_full_name())

    def test_user_get_absolute_url(self):
        expect = f'/user/{self.test_user1.id}'
        self.assertEqual(expect, self.test_user1.get_absolute_url())

    def test_contact_str_method(self):
        expect = self.test_contact.phone
        self.assertEqual(expect, str(self.test_contact))

    def test_contact_et_address(self):
        expect = f'{self.test_contact.city} {self.test_contact.street} {self.test_contact.house} ' \
                 f'{self.test_contact.structure} {self.test_contact.building} {self.test_contact.apartment}'
        self.assertEqual(expect, self.test_contact.get_address())
