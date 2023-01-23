import pandas as pd
from itertools import product

from gla.ref_map import CONST_VAL, COL_NAME, N_ELEMENT, D_AGG_CALCULATION, DROP_COLS_OPT

import argparse

# produce a more compact, efficient, PEP-compliant code using the following python code?
# improve the current docstring but maintain the meaning of the old docstring
#

### not working

class PeerEvaluator:
    def __init__(self, df):
        self.df = df
        self.col_name = COL_NAME
        self.n_element = N_ELEMENT
        self.d_agg_calculation = D_AGG_CALCULATION
        self.drop_cols_opt = DROP_COLS_OPT

    def extract_each_peers(self, dcols, std_col):
        """
        Extract specific columns from the dataframe, rename the columns and return the extracted dataframe.
        Parameters:
        - dcols (list): A list of column indices that need to be extracted from the dataframe
        - std_col (list): A list of column indices that will be included in the extracted dataframe along with dcols
        """
        expanded_col = std_col + dcols
        return self.df.iloc[:, expanded_col].rename(columns=self.col_name)

    def collapse_cols_representation(self, cols):
        """
        Extract specific columns from the dataframe, concatenate them, extract digits from the concatenated column and return the processed dataframe.
        Parameters:
        - cols (list): A list of column names in the dataframe
        """
        indices_s = [i for i, s in enumerate(cols) if 'Peer Name' in s]
        indices_e = [i for i, s in enumerate(cols) if 'Justification for Peer' in s]
        indices_e = [x + 1 for x in indices_e]
        col_int = [range(start, end) for start, end in zip(indices_s, indices_e)]
        std_col = range(0, indices_s[0])
        all_df = [self.extract_each_peers(dcols, std_col) for dcols in col_int]
        df1 = pd.concat(all_df).reset_index(drop=True)
        for delement in self.n_element:
            df1[delement] = df1[delement].str.extract('\((\d+)\)')
        return df1

    def read_file_transform(self, finput=None):
        """
        Read input file, process the dataframe and return the processed dataframe
        Parameters:
        - finput (str): The file name of the excel file that needs to be processed.

            Note:
    - The input dataframe should have the columns: name, group_name, peer_name, peer_student_id, research_information_gathering, creative_input, coperation_within_group, communication, contribution_quality, meeting_attendance, justification.
    - If the input dataframe is less than 13 columns, it is assumed that it is in the correct format for further processing.


        """
        df = pd.read_excel(finput)
        cols = df.columns.tolist()
        return self.collapse_cols_representation(cols) if len(cols) > 13 else df

    def convert_percentage_weightage(self, scale_type=None):
        """
        Normalize the values of specific columns in the dataframe using a given scale and return the processed dataframe.
        The function has been tested for scale 5 and 7 and by default, the lowest point "Terrible (0)" will not yield any grade.
        Parameters:
        - scale_type (int): The type of scale to be used (5 or 7)
        """
        if scale_type not in (5, 7):
            raise ValueError('Please input a valid scale type: 5 or 7, to avoid normalization error')
        revise_max_val = 6 if scale_type == 7 else 4
        for delement in self.n_element:
            self.df[delement] = self.df[delement].apply(lambda x: (x - 1) / revise_max_val * 100 if x != 0 else 0)
        return self.df




    def aggregate_each_peers(self):
        """
        Aggregate the dataframe based on the specific columns and return the processed dataframe.
        """
        df_agg = self.df.groupby(['name', 'group_name']).agg(self.d_agg_calculation)
        df_agg.reset_index(inplace=True,drop=True)
        return df_agg

    def drop_cols_opt_func(self):
        """
        Drop specific columns from the dataframe and return the processed dataframe.
        """
        return self.df.drop(columns=self.drop_cols_opt)

    def process_dataframe(self, finput=None, scale_type=None):
        """
        Read input file, process the dataframe and return the final processed dataframe.
        Parameters:
        - finput (str): The file name of the excel file that needs to be processed.
        - scale_type (int): The type of scale to be used (5 or 7)
        """
        self.df = self.read_file_transform(finput)

        # df_raw = re_arrange_justification(self.df, self.n_element)
        # df = df_raw.groupby(level=0).agg(D_AGG_CALCULATION)


        self.df = self.convert_percentage_weightage(scale_type)
        self.df = self.aggregate_each_peers()
        self.df = self.drop_cols_opt_func()
        return self.df

    def re_arrange_justification(self):

        """
     This function processes the dataframe by creating a new column 'feedback', modifying the 'justification' column,
     setting the index, and converting the specific column to integer.

     Parameters:
     - df (pandas dataframe): The dataframe that needs to be processed
     - n_element (str): The name of the column that needs to be converted to integer

     Returns:
     - pandas dataframe: The processed dataframe

     """
        df=self.df
        n_element=self.n_element
        df["feedback"] = df["name"].str.cat(df["justification"], sep="-->")
        df["justification"] = "'" + df["justification"].astype(str) + "'"
        df = df.set_index(["peer_student_id", "assessor_student_id"])
        df = df.sort_index(ascending=True)
        df.index = pd.MultiIndex.from_tuples(df.index.tolist())
        df[n_element] = df[n_element].astype(int)
        df["justification_annom"] = df["justification"].astype(str)

        df = df.groupby(level=0).agg(D_AGG_CALCULATION)
        df.rename(columns = {'peer_name':'name'}, inplace = True)
        self.df=df
        return self.df

    def check_missing_infomation(self):
        """
            TODO:

            This function checks for missing information in the dataframe, specifically the student ID and peer ID. If any
            missing values are found, they will be dropped from the dataframe. This function also raises a warning for
            this serious issue.

            Parameters:
            - df (pandas dataframe): The dataframe to be checked for missing information

            Returns:
            - df (pandas dataframe): The dataframe with missing information removed
            """
        self.df = self.df.dropna()
        return self.df

fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_transform _22_23_fill.xlsx'
# peer_evaluator = PeerEvaluator(pd.read_excel(fexcel))
# peer_evaluator.convert_percentage_weightage(scale_type=5)
# peer_evaluator.check_missing_infomation()
# peer_evaluator.re_arrange_justification()
# df=peer_evaluator.aggregate_each_peers()
# peer_evaluator.drop_cols_opt_func()
# final_df = peer_evaluator.df
PeerEvaluator.process_dataframe(finput=None, scale_type=None)