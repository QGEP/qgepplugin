"""
python -m unittest interlis.tests
"""

import unittest

from sqlalchemy.orm import Session

from . import main
from . import utils
from . import config


class TestQGEPUseCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        utils.setup_test_db(with_data=True, keep_only_subset=False)

    def setUp(self):
        utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL, force_recreate=True)

    def test_case_a_import_wincan_xtf(self):
        """
        # A. import Wincan-generated xtf data into QGEP

        We recieve data from a TV inspection company as a Wincan exported .xtf file. We want this data loaded into QGEP.
        """
        main(['--force_recreate', '--import_xtf', r'interlis\data\2021-01-21_inspectiondata\test_without_abwasserbauwerkref.xtf', 'qgep'])

        from .datamodels.qgep import Classes as QGEP

        session = Session(utils.create_engine())

        # make sure all elements got imported
        self.assertEqual(session.query(QGEP.damage_manhole).count(), 2)
        self.assertEqual(session.query(QGEP.examination).count(), 1)
        self.assertEqual(session.query(QGEP.data_media).count(), 1)
        self.assertEqual(session.query(QGEP.file).count(), 3)

        # TODO : also check some properties

