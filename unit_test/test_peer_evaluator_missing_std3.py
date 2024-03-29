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
        data_bench = {'std_name': ['std21', 'std22', 'std23'],
                      'research_information_gathering': [2, 6, 1.5],
                      'creative_input': [2, 6, 3],
                      'cooperation_within_group': [2, 6, 3],
                      'communication': [2, 6, 3],
                      'contribution_quality': [2, 6, 3],
                      'meeting_attendance': [2, 6, 3],
                      'group_summation': [179.58, 179.58, 179.58],
                      'weightage': [0.56, 1.67, 0.77]
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

        self.rcols=['research_information_gathering',
               'creative_input',
               'cooperation_within_group',
               'communication',
               'contribution_quality',
               'meeting_attendance',
               'group_summation',
               'weightage',
               ]
        data = [['std21', 21, 99, 'std22', 22, 7, 7, 7, 7, 7, 7, 'STD21 comment to std22'],
                ['std21', 21, 99, 'std23', 23, 4, 4, 4, 4, 4, 4, 'STD21 comment to std23'],
                ['std22', 22, 99, 'std21', 21, 3, 3, 3, 3, 3, 3, 'STD22 comment to std21'],
                ['std22', 22, 99, 'std23', 23, 1, 4, 4, 4, 4, 4, 'STD22 comment to std23'],
                ]
        self.df = pd.DataFrame(data, columns=['name', 'assessor_student_id', 'group_name', 'peer_name', 'peer_student_id',
                                         'research_information_gathering', 'creative_input', 'cooperation_within_group',
                                         'communication', 'contribution_quality', 'meeting_attendance', 'justification'])


        self.fpath_excel = self.df
        self.scale_type = 7
        self.data_bench = DataBenchmark()

    def test_equals(self):
        PE = PeerEvaluator(finput=self.fpath_excel, scale_type=self.scale_type)
        PE.process_dataframe()
        df_n = PE.cal_score

        df_n = df_n.loc[:, self.columns_to_keep].reset_index(drop=True)



        # Round due to floating error
        df_n=df_n[self.rcols].apply(lambda x: pd.Series.round(x, 2))
        self.data_bench.df_bench=self.data_bench.df_bench[self.rcols].apply(lambda x: pd.Series.round(x, 2))

        self.assertTrue(df_n.equals(self.data_bench.df_bench), "The two dataframes are not equal")


if __name__ == '__main__':
    unittest.main()
