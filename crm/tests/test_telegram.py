from django.test import TestCase
from crm import telegram_bot

class TelegreamTest(TestCase):

    def test_create_url(self):
        method = 'method'
        token = 'token'
        expect = f'https://api.telegram.org/bot{token}/{method}'
        self.assertEqual(expect, telegram_bot.create_url(token, method))

    def test_get_update(self):
        self.assertTrue(telegram_bot.get_update().json()['ok'])

    def test_get_chat_id(self):
        id = ''
        self.assertTrue(telegram_bot.get_chat_id(id)['ok'])

    def test_send_message(self):
        to = '1'
        text = '1'
        self.assertEqual(telegram_bot.send_message(to, text)['description'], 'Bad Request: chat not found')

