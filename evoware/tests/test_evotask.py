import unittest
import logging
import tempfile

from ..evotask import EvoTask, osp
from .. import fileutil as F

class Test(unittest.TestCase):
    """Test Worklist"""

    def setUp(self):
        self.f_project = tempfile.mkdtemp(prefix='test_evotask_')
        self.loglevel = logging.WARNING

        logging.basicConfig(level=self.loglevel)

    def tearDown(self):
        F.tryRemove(self.f_project, tree=True)

    def test_evotask_default(self):
        t = EvoTask(projectfolder=self.f_project)

        self.assert_(osp.exists(t.f_task), 'no task folder')
        self.assert_(osp.exists(osp.join(t.f_task, t.F_LOG)), 'no log file')
