"""
python -m unittest interlis.tests
"""

import unittest
import interlis
import interlis.utils
import interlis.config

class TestQGEPUseCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        interlis.utils.setup_test_db(keep_only_subset=True)

    def setUp(self):
        interlis.utils.create_ili_schema(interlis.config.ABWASSER_SCHEMA, interlis.config.ABWASSER_ILI_MODEL, force_recreate=True)

    def test_a_import_wincan_xtf(self):
        """
        # A. import Wincan-generated xtf data into QGEP

        We recieve data from a TV inspection company as a Wincan exported .xtf file. We want this data loaded into QGEP.
        """
        interlis.main(['--force_recreate', '--import_xtf', r'interlis\data\test_without_abwasserbauwerkref.xtf', 'qgep'])
