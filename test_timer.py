#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
from timer import Timer

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()

    def test_timer_is_running_if_it_is_started(self):
        self.timer.start()
        self.assertTrue(self.timer.running)

    def test_timer_is_not_running_if_it_is_paused(self):
        self.timer.pause()
        self.assertFalse(self.timer.running)

    def test_time_left_is_decremented_one_second_if_timer_is_running(self):
        self.time_left = 300
        self.timer.start()
        self.timer.update()
        self.assertEqual(self.timer.time_left, 299)

if __name__ == '__main__':
    unittest.main()
