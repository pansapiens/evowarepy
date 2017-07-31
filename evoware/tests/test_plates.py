import unittest
from ..plates import PlateFormat

class Test(unittest.TestCase):
    """Test PlateFormat"""

    def test_plateformat_init(self):
        formats = {}
        for n in [6, 12, 24, 96, 384, 1536]:
            f = PlateFormat(n)
            formats[n] = f
            self.assertEqual(f.n, f.nx * f.ny, 'plate format error')

        self.assertEqual(formats[6].nx, 3, msg='6-well definition error')
        self.assertEqual(formats[12].nx, 4, msg='12-well definition error')
        self.assertEqual(formats[24].nx, 6, msg='24-well definition error')
        self.assertEqual(formats[96].nx, 12, msg='96-well definition error')
        self.assertEqual(formats[384].nx, 24, msg='384-well definition error')
        self.assertEqual(formats[1536].nx, 48, msg='1536-well definition error')

    def test_plateformat_pos2int(self):
        f = PlateFormat(96)
        self.assertEqual(f.human2int('A1'), 1)
        self.assertEqual(f.human2int('H1'), 8)
        self.assertEqual(f.human2int('b1'), 2)
        self.assertEqual(f.human2int('A2'), 9)
        self.assertEqual(f.human2int('A12'), 89)
        self.assertEqual(f.human2int('h12'), 96)

    def test_plateformat_human2int(self):
        f = PlateFormat(96)

        tests = ['A1', 'B1', 'H1', 'A2', 'B2', 'H2', 'A12', 'B12', 'H12']

        for t in tests:
            pos = f.human2int(t)
            human = f.int2human(pos)
            self.assertEqual(t, human)

    def test_plateformat_eq(self):
        f1 = PlateFormat(96)
        f2 = PlateFormat(96)
        f3 = PlateFormat(96, nx=1, ny=96)

        self.assertTrue(f1 == f2)
        self.assertFalse(f2 == f3)
        self.assertEqual(f1, f2)
