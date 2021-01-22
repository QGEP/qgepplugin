"""
python -m unittest interlis.tests
"""

import unittest
import interlis
import interlis.utils
import interlis.config

class TestQgep2Ili(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        interlis.utils.setup_test_db(keep_only_subset=True)

    def setUp(self):
        interlis.utils.create_ili_schema(interlis.config.ABWASSER_SCHEMA, interlis.config.ABWASSER_ILI_MODEL, force_recreate=True)

    def test_export(self):
        interlis.main(['qgep', 'export', 'test.xtf'])

    def test_import(self):
        interlis.main(['qgep', 'import', 'test.xtf'])

class TestQwat2Ili(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        interlis.utils.setup_test_db(keep_only_subset=True)

    def setUp(self):
        interlis.utils.create_ili_schema(interlis.config.WASSER_SCHEMA, interlis.config.WASSER_ILI_MODEL, force_recreate=True)

    def test_export(self):
        interlis.main(['qwat', 'export', 'test.xtf'])

    def test_import(self):
        interlis.main(['qwat', 'import', 'test.xtf'])
