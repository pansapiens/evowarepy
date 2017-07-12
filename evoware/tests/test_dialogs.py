import unittest
import os
from unittest import skipIf, skip
from ..dialogs import (askForFile, info, warning, error, PyDialogError,
                       lastException)

# HAS_X11 = os.environ.get('DISPLAY', None)
HAS_X11 = False


class Test(unittest.TestCase):
    """Test dialogs"""

    def setUp(self):
        pass

    @skipIf(not HAS_X11, "Skipping test, running headless")
    def test_askForFile(self):
        """fileutil.askForFile test"""
        r = askForFile(title='Test File')
        self.assertNotEqual(r, 'test.dat')

    @skipIf(not HAS_X11, "Skipping test, running headless")
    def test_info(self):
        info('testInfo', 'This is a test.')

    @skipIf(not HAS_X11, "Skipping test, running headless")
    def test_warning(self):
        warning('testWarning', 'This is a warning.')

    @skipIf(not HAS_X11, "Skipping test, running headless")
    def test_error(self):
        error('testError', 'This is an error.')

    @skipIf(not HAS_X11, "Skipping test, running headless")
    def test_exception(self):
        try:
            raise PyDialogError('testing')
        except PyDialogError as what:
            lastException()
