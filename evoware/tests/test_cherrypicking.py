import unittest
from os import path
import tempfile
from .. import fileutil as F
from ..cherrypicking import TargetIndex, PartIndex, CherryWorklist
from .. import plates


class Test(unittest.TestCase):
    """Test PlateFormat"""

    def setUp(self):
        """Called once"""
        testdata_dir = path.join(path.dirname(__file__), 'testdata')
        self.f_parts = path.join(testdata_dir, 'partslist.xls')
        self.f_primers = path.join(testdata_dir, 'primers.xls')
        self.f_simple = path.join(testdata_dir, 'targetlist.xls')
        self.f_pcr = path.join(testdata_dir, 'targetlist_PCR.xls')

        self.f_worklist = tempfile.mktemp(suffix=".gwl",
                                          prefix="test_cherrypicking_")

    def tearDown(self):
        """Called after all tests"""
        F.tryRemove(self.f_worklist)

    def test_partIndex(self):
        self.p = PartIndex()
        self.p.readExcel(self.f_parts)

        self.assertEqual(self.p['sb0101', 2], self.p['sb0101#2'])
        self.assertEqual(len(self.p['sb0111']), 2)

        self.assertEqual(len(self.p), 27)

        self.assertEqual(self.p.position('sb0102', '2'), (u'SB10', u'A5'))

        self.assertEqual(self.p.position('sb0102#2', plate='SB10'),
                         self.p.position('sb0102', '2'))

        self.assertEqual(self.p._plates['SB11'], plates.PlateFormat(384))

    def test_targetIndex_simple(self):
        t = TargetIndex(srccolumns=[('construct', 'clone')])
        t.readExcel(self.f_simple)

    def test_targetIndex_multiple(self):
        t = TargetIndex(srccolumns=['template', 'primer1', 'primer2'])
        t.readExcel(self.f_pcr)

        self.assertTrue(t._volume['template'] == 2)
        self.assertEqual(t._volume['primer1'], 5)
        self.assertEqual(t._volume['primer2'], 5)

    def test_generate_worklist(self):
        parts = PartIndex()
        parts.readExcel(self.f_parts)
        parts.readExcel(self.f_primers)

        t = TargetIndex(srccolumns=['template', 'primer1', 'primer2'])
        t.readExcel(self.f_pcr)

        cwl = CherryWorklist(self.f_worklist, t, parts)

        cwl.toWorklist(byLabel=True, volume=10)

        cwl.close()
