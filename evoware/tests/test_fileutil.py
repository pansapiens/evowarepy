import unittest
from ..fileutil import *

class Test(unittest.TestCase):
    """Test MyModule"""

    def setUp(self):
        self.fname1 = '~/nonexistent/../subfolder/file.txt'

    def test_stripFilename(self):
        """fileutil.stripFilename test"""
        r = stripFilename(self.fname1)
        self.assertEqual(r, 'file', '%r != %r' % (r, 'file'))

    def test_absfilename(self):
        """fileutil.absfilename test"""
        r = absfile(self.fname1)
        self.assertEqual(r,
                         osp.join(osp.expanduser('~'), 'subfolder/file.txt'))
