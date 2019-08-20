"""
Run Tests by calling:  `python -m unittest test_loader.py`
"""


import unittest

from program import CSVDBLoader


class TestCSVDBLoader(unittest.TestCase):

    GOOD_CSV_FILE = './data/sportwettentest-head-fixed.csv'
    BAD_CSV_FILE = './data/sportwettentest-head-broken.csv'


    def setUp(self):
        self.csv = CSVDBLoader()
        self.csv.args.input_path = self.GOOD_CSV_FILE

    def test_connection_to_sqlite_is_set(self):

        self.csv.args.run_analysis = True
        self.csv.run()
        self.assertTrue(hasattr(self.csv, 'connection'))


    # def test_table_name_contains_filename_no_ext(self):
    #     self.csv._build_table_name()
    #     print(self.csv.table_name)
    #     print(self.csv.table_name)
    #     print(self.csv.table_name)
    #     self.assertTrue(self.GOOD_CSV_FILE in self.csv.table_name)




class TestHypothesis(unittest.TestCase):


    def test_qitem(self):
        pass