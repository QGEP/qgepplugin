"""
python -m unittest interlis.tests
"""

import os
import unittest
import decimal
import tempfile

from sqlalchemy.orm import Session

from . import main
from . import utils


class TestQGEPUseCases(unittest.TestCase):

    # @unittest.skip("...")
    def test_case_a_import_wincan_xtf(self):
        """
        # A. import Wincan-generated xtf data into QGEP

        We recieve data from a TV inspection company as a Wincan exported .xtf file. We want this data loaded into QGEP.
        """
        utils.various.setup_test_db("full")

        from .qgep.model_qgep import QGEP
        session = Session(utils.sqlalchemy.create_engine())

        self.assertEqual(session.query(QGEP.damage_manhole).count(), 0)
        self.assertEqual(session.query(QGEP.examination).count(), 0)
        self.assertEqual(session.query(QGEP.data_media).count(), 0)
        self.assertEqual(session.query(QGEP.file).count(), 0)
        self.assertEqual(session.query(QGEP.organisation).count(), 15)

        path = os.path.join(os.path.dirname(__file__), 'data', 'test_data', 'case_a_import_from_wincan.xtf')
        main(["io", "--import_xtf", path, "qgep", "--recreate_schema"])

        # make sure all elements got imported
        self.assertEqual(session.query(QGEP.damage_manhole).count(), 2)
        self.assertEqual(session.query(QGEP.examination).count(), 1)
        self.assertEqual(session.query(QGEP.data_media).count(), 1)
        self.assertEqual(session.query(QGEP.file).count(), 3)
        self.assertEqual(session.query(QGEP.organisation).count(), 18)

        # checking some properties
        manhole = session.query(QGEP.damage_manhole).get("fk11abk6SS000002")
        self.assertEqual(manhole.distance, decimal.Decimal("2.55"))
        self.assertEqual(manhole.comments, "wurde auch schon vor 3 Jahren festgestellt")

        data = session.query(QGEP.file).get("fk11abk6DA000002")
        self.assertEqual(data.identifier, "8486_0001.jpg")
        self.assertEqual(data.path_relative, "inspectiondata20210120/fotos")

    # @unittest.skip("...")
    def test_case_b_export_complete_qgep_to_xtf(self):
        """
        # B. export the whole QGEP model to interlis
        """
        utils.various.setup_test_db("subset")  # we use a subset for now as full export can take time

        path = os.path.join(tempfile.mkdtemp(), "export.xtf")
        main(["io", "--export_xtf", path, "qgep", "--recreate_schema"])

        print(f"Saved to {path}")
        utils.ili2db.validate_xtf_data(path)

    # @unittest.skip("...")
    def test_case_c_import_complete_xtf_to_qgep(self):
        """
        # C. import a whole interlis transfer file into QGEP
        """

        utils.various.setup_test_db("empty")

        from .qgep.model_qgep import QGEP
        session = Session(utils.sqlalchemy.create_engine())

        self.assertEqual(session.query(QGEP.channel).count(), 0)
        self.assertEqual(session.query(QGEP.manhole).count(), 0)

        path = os.path.join(os.path.dirname(__file__), 'data', 'test_data', 'case_c_import_all.xtf')
        main(["io", "--import_xtf", path, "qgep", "--recreate_schema"])

        # make sure all elements got imported
        self.assertEqual(session.query(QGEP.channel).count(), 102)
        self.assertEqual(session.query(QGEP.manhole).count(), 49)

        # checking some properties  # TODO : add some more...
        manhole = session.query(QGEP.manhole).get("ch080qwzNS000113")
        self.assertEqual(manhole.year_of_construction, 1950)


class TestRegressions(unittest.TestCase):

    # FIXME
    # @unittest.skip("...")
    @unittest.expectedFailure
    def test_regression_001_self_referencing_organisation(self):
        """
        Due to current logic of the import script, organisations may be created multiple times.
        """

        utils.various.setup_test_db("empty")

        from .qgep.model_qgep import QGEP
        session = Session(utils.sqlalchemy.create_engine())

        self.assertEqual(session.query(QGEP.organisation).count(), 0)

        main(
            [
                "--recreate_schema",
                "--import_xtf",
                r"interlis\data\test_data\regression_001_self_referencing_organisation.xtf",
                "qgep",
            ]
        )

        self.assertEqual(session.query(QGEP.organisation).count(), 1)

    # @unittest.skip("...")
    @unittest.expectedFailure
    def test_ili2pg_crash(self):
        """
        ili2pg crashes with --noSmartMapping with our files (see https://github.com/claeis/ili2db/issues/381)

        this should be fixed with ili2pg 4.4.6
        """

        main(
            [
                "--recreate_schema",
                "--import_xtf",
                r"interlis\data\2021-01-19_inspectiondata\testdata_vsa_kek_2019_manhole_damage_8486.xtf",
                "qgep",
            ]
        )
