# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from django.utils import timezone

from money.tool import get_current_minute, cycle_need_push


class FuckTestCase(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        self.assertTrue(cycle_need_push(600, 60))
        self.assertTrue(cycle_need_push(100, 20))
        self.assertFalse(cycle_need_push(100, 30))
