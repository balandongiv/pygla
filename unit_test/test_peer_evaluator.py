'''
This code is a Python unit test that tests the functionality of the PeerEvaluator class from
the gla module. It uses the unittest library to create a test case named TestPeerEvaluator,
which performs various tests on the PeerEvaluator class. The DataBenchmark class is defined as
an auxiliary class to hold some data for the tests.
The setUp method of the TestPeerEvaluator class creates an instance of the DataBenchmark class
and sets up some required data.


The code checks whether the output generated by the function PE.cal_score is equal to a
benchmark dataframe.
The equality between the two is confirmed using the assert statement,
which will raise an error if the two objects are not equal.

'''

import os
import unittest

import pandas as pd

from gla.gla import PeerEvaluator


class DataBenchmark:
    def __init__(self):
        data_bench = {
            'std_name': ['std1', 'std2', 'std3', 'std5', 'std6', 'std7', 'std8', 'std9', 'std10'],
            'research_information_gathering': [0, 6, 3, 6, 6, 6, 3, 3, 3],
            'creative_input': [0, 6, 3, 6, 6, 6, 3, 3, 3],
            'cooperation_within_group': [0, 6, 3, 6, 6, 6, 3, 3, 3],
            'communication': [0, 6, 3, 6, 6, 6, 3, 3, 3],
            'contribution_quality': [0, 6, 3, 6, 6, 6, 3, 3, 3],
            'meeting_attendance': [0, 6, 3, 6, 6, 6, 3, 3, 3],
            'group_summation': [150, 150, 150, 300, 300, 300, 150, 150, 150],
            'weightage': [0, 2, 1, 1, 1, 1, 1, 1, 1]
        }
        self.df_bench = pd.DataFrame(data_bench)
        convert_dict = {'research_information_gathering': float,
                        'creative_input': float,
                        'cooperation_within_group': float,
                        'communication': float,
                        'contribution_quality': float,
                        'meeting_attendance': float,
                        'group_summation': float,
                        'weightage': float}
        self.df_bench = self.df_bench.astype(convert_dict)


class TestPeerEvaluator(unittest.TestCase):
    def setUp(self):
        self.columns_to_keep = ['std_name',
                                'research_information_gathering',
                                'creative_input',
                                'cooperation_within_group',
                                'communication',
                                'contribution_quality',
                                'meeting_attendance',
                                'group_summation',
                                'weightage',
                                ]
        self.data_all = {
            'name': ['std1', 'std1', 'std2', 'std2', 'std3', 'std3', 'std5', 'std5', 'std6', 'std6', 'std7', 'std7',
                     'std8', 'std8', 'std9', 'std9', 'std10', 'std10'],
            'assessor_student_id': [1, 1, 2, 2, 3, 3, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10],
            'group_name': [10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 15, 15, 15, 15, 15, 15],
            'peer_name': ['std2', 'std3', 'std1', 'std3', 'std1', 'std2', 'std6', 'std7', 'std5', 'std7', 'std5',
                          'std6', 'std9', 'std10', 'std8', 'std10', 'std8', 'std9'],
            'peer_student_id': [2, 3, 1, 3, 1, 2, 6, 7, 5, 7, 5, 6, 9, 10, 8, 10, 8, 9],
            'research_information_gathering': [7, 4, 1, 4, 1, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4],
            'creative_input': [7, 4, 1, 4, 1, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4],
            'cooperation_within_group': [7, 4, 1, 4, 1, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4],
            'communication': [7, 4, 1, 4, 1, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4],
            'contribution_quality': [7, 4, 1, 4, 1, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4],
            'meeting_attendance': [7, 4, 1, 4, 1, 7, 7, 7, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4],
            'justification': ['STD1 comment to std2', 'STD1 comment to std3', 'STD2 comment to std3',
                              'STD2 comment to std3', 'STD3 comment to std1', 'STD3 comment to std2',
                              'STD5 comment to std6', 'STD5 comment to std7', 'STD6 comment to std5',
                              'STD6 comment to std7', 'STD7 comment to std5', 'STD7 comment to std6',
                              'STD8 comment to std9', 'STD8 comment to std10', 'STD9 comment to std8',
                              'STD9 comment to std10', 'STD10 comment to std8', 'STD10 comment to std9']
        }

        self.fpath_excel = 'case_all.xlsx'
        self.df = pd.DataFrame(self.data_all)
        self.df.to_excel(self.fpath_excel)
        self.scale_type = 7
        self.data_bench = DataBenchmark()


    def test_equals(self):
        PE = PeerEvaluator(finput=self.fpath_excel, scale_type=self.scale_type)
        PE.process_dataframe()
        df_n = PE.cal_score

        df_n = df_n.loc[:, self.columns_to_keep].reset_index(drop=True)

        self.assertTrue(df_n.equals(self.data_bench.df_bench), "The two dataframes are not equal")

        os.remove(self.fpath_excel)

if __name__ == '__main__':
    unittest.main()
