# -*- coding=utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from eparser import TmallParser()
from amazon_parser = AmazonParser()


class ParserTest(TestCase):
    def test_mul_parser(self):
        """
        Test the parser
        """
        c = Client()
        response = c.get('/search/', 
                {'k': u'嫌疑人x的献身', 'tmall': '', 'amazon': ''})
        self.assertEqual(int(response.status_code), 200)
        print(response.content)
    def test_parsers(self):
        tmall_parser = TmallParser()
        amazon_parser = AmazonParser()
        print tmall_parser.parse(u'嫌疑人x的獻身')
        print amazon_parser.parse(u'嫌疑人x的獻身')
