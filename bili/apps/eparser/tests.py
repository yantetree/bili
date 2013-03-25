# -*- coding=utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client


class ParserTest(TestCase):
    def test_basic_addition(self):
        """
        Test the parser
        """
        c = Client()
        response = c.get('/search/', {'k': u'嫌疑人x的献身', 'tmall': '', 'amazon': ''})
        self.assertEqual(int(response.status_code), 200)
        print(response.content)
