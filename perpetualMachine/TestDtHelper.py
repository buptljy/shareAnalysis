import unittest


import DtHelper as dthp


class TestDtHelper(unittest.TestCase):

    def test_getDayStr(self):
        day = "2018-04-16"
        self.assertEquals("2018-04-13", dthp.getDayStr(-1, day))
        day = "2018-02-14"
        self.assertEquals("2018-02-22", dthp.getDayStr(1, day))


if __name__ == "__main__":
    unittest.main()