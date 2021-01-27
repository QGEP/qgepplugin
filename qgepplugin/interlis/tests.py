"""
python -m unittest interlis.tests
"""

import unittest
import decimal

from sqlalchemy.orm import Session

from . import main
from . import utils
from . import config


class TestQGEPUseCases(unittest.TestCase):

    def test_case_a_import_wincan_xtf(self):
        """
        # A. import Wincan-generated xtf data into QGEP

        We recieve data from a TV inspection company as a Wincan exported .xtf file. We want this data loaded into QGEP.
        """
        utils.setup_test_db('empty')
        utils.create_ili_schema(config.ABWASSER_SCHEMA, config.ABWASSER_ILI_MODEL)

        main(['--force_recreate', '--import_xtf', r'interlis\data\2021-01-21_inspectiondata\test_without_abwasserbauwerkref.xtf', 'qgep'])

        from .datamodels.qgep import Classes as QGEP

        session = Session(utils.create_engine())

        # make sure all elements got imported
        self.assertEqual(session.query(QGEP.damage_manhole).count(), 2)
        self.assertEqual(session.query(QGEP.examination).count(), 1)
        self.assertEqual(session.query(QGEP.data_media).count(), 1)
        self.assertEqual(session.query(QGEP.file).count(), 3)

        # checking some properties
        manhole = session.query(QGEP.damage_manhole).get('fk11abk6SS000002')
        self.assertEqual(manhole.distance, decimal.Decimal('2.55'))
        self.assertEqual(manhole.comments, 'wurde auch schon vor 3 Jahren festgestellt')

        data = session.query(QGEP.file).get('fk11abk6DA000002')
        self.assertEqual(data.identifier, '8486_0001.jpg')
        self.assertEqual(data.path_relative, 'inspectiondata20210120/fotos')

    @unittest.skip("seems fixed since 4.4.6 snapshot")
    def test_ili2pg_crash(self):
        """
        ili2pg crashes with --noSmartMapping with our files (see https://github.com/claeis/ili2db/issues/381)

        there's a fix incomming it seems
        """

        from .datamodels.qgep import Classes as QGEP
        main(['--force_recreate', '--import_xtf', r'interlis\data\2021-01-19_inspectiondata\testdata_vsa_kek_2019_manhole_damage_8486.xtf', 'qgep'])

