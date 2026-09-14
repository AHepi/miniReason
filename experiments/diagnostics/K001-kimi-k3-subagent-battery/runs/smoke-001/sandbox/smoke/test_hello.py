import unittest

from smoke.hello import hello, twice


class TestHello(unittest.TestCase):
    def test_twice_positive(self):
        self.assertEqual(twice(3), 6)

    def test_twice_zero(self):
        self.assertEqual(twice(0), 0)

    def test_twice_negative(self):
        self.assertEqual(twice(-4), -8)

    def test_hello_kimi(self):
        self.assertEqual(hello("kimi"), "hello, kimi")


if __name__ == "__main__":
    unittest.main()
