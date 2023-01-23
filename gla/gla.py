import pandas as pd
from itertools import product

from gla.ref_map import CONST_VAL, COL_NAME, N_ELEMENT, D_AGG_CALCULATION, COLS_OPT

import argparse

# produce a more compact, efficient, PEP-compliant code using the following python code?
# improve the current docstring but maintain the meaning of the old docstring
#



def save_output_excel(df, fname='result.xlsx', verbose=False):
    """
    This function saves the processed dataframe to an excel file. The location and name of the file can be specified
    by providing the 'fname' parameter. The function also has an option to remove certain columns from the dataframe
    before saving, by setting the 'verbose' parameter to False.

    Parameters:
    - df (pandas dataframe): The dataframe that needs to be saved
    - fname (str, optional): The location and name of the excel file. Default is 'result.xlsx'
    - verbose (bool, optional): A flag to indicate if certain columns should be removed from the dataframe before saving.
                                Default is False

    Returns:
    - None
    """
    columns_to_keep=['std_name',
               'research_information_gathering',
               'creative_input',
               'cooperation_within_group',
               'communication',
               'contribution_quality',
               'meeting_attendance',
               'dgroup_name',
               'nmember',
               'weightage',
               'justification_annom',
               'feedback'
               ]


    if not verbose:
        df = df.loc[:, columns_to_keep]
    # Move 'justification_annom' and 'feedback' to the last columns
    cols = df.columns.tolist()
    cols = [col for col in cols if col not in ['justification_annom', 'feedback']] + ['justification_annom', 'feedback']
    df = df[cols]
    df.to_excel(fname, index=False)


def calculate_factor(df, df_stat):
    """
    This function maps values of one dataframe column to another dataframe column based on a condition.

    Parameters:
    - df (pandas dataframe): The dataframe that needs to be processed
    - df_stat (pandas dataframe): The dataframe that will be used as a reference for the mapping

    Returns:
    - pandas dataframe: The processed dataframe
    """
    df_stat = df_stat.set_index('group_name')
    df = df.merge(df_stat, left_on='dgroup_name', right_index=True, how='left')
    df['nmember'] = df['row_const_y']
    df['group_summation'] = df['sum_percentage_all_elements_y']
    df['weightage'] = df['sum_percentage_all_elements_x'] / df['sum_percentage_all_elements_y'] * df['nmember']
    df = df.drop(columns=['sum_percentage_all_elements_x', 'sum_percentage_all_elements_y', 'row_const_y','row_const_x'])
    return df


def group_stat(df):
    """
   This function groups the dataframe by a specific column, performs aggregation and renames the column.

   Parameters:
   - df (pandas dataframe): The dataframe that needs to be processed

   Returns:
   - pandas dataframe: The processed dataframe

   """
    df_stat = df.groupby(level=0).agg({'row_const': 'sum',
                                       'sum_percentage_all_elements': 'sum'}).reset_index().rename(
        columns={'index': 'group_name'})
    return df_stat
class PeerEvaluator:
    def __init__(self, finput,scale_type=None):
        self.df = self.read_file_transform(finput)
        # self.df = df
        self.scale_type=scale_type
        self.col_name = COL_NAME
        self.n_element = N_ELEMENT
        self.d_agg_calculation = D_AGG_CALCULATION
        self.cols_opt = COLS_OPT
        self.df_agg=[]

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

    def convert_percentage_weightage(self):
        """
        Normalize the values of specific columns in the dataframe using a given scale and return the processed dataframe.
        The function has been tested for scale 5 and 7 and by default, the lowest point "Terrible (0)" will not yield any grade.
        Parameters:
        - scale_type (int): The type of scale to be used (5 or 7)
        """
        if self.scale_type not in (5, 7):
            raise ValueError('Please input a valid scale type: 5 or 7, to avoid normalization error')
        revise_max_val = 6 if self.scale_type == 7 else 4
        df=self.df
        cols = pd.Index(CONST_VAL.keys())
        mi = pd.MultiIndex.from_product([['percentage_trans'], cols])
        df[mi] = df[cols] * pd.Series(CONST_VAL) / revise_max_val
        self.df=df
        return self.df




    def aggregate_each_peers(self):
        df=self.df
        col_to_sum = list(product(['percentage_trans'], self.n_element))
        df[('sum_percentage_all_elements')] = df[col_to_sum].sum(axis=1)
        df['row_const'] = 1  # Use to calculate the number of group members

        # Assign back the student ID
        df = df.reset_index().rename(columns={'index': 'std_id', 'peer_name': 'std_name'})

        df['dgroup_name'] = df['group_name']
        df = df.set_index(['group_name', 'std_id'])

        df_stats = group_stat(df)

        df = calculate_factor(df, df_stats)
        self.df=df
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
        # df.rename(columns = {'peer_name':'name'}, inplace = True)
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

    def process_dataframe(self):
        """
        Read input file, process the dataframe and return the final processed dataframe.
        Parameters:
        - finput (str): The file name of the excel file that needs to be processed.
        - scale_type (int): The type of scale to be used (5 or 7)
        """


        self.check_missing_infomation()
        self.re_arrange_justification()
        self.convert_percentage_weightage()
        self.aggregate_each_peers()
        return self.df
def tst_fill_excel():
    fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_transform _22_23_fill.xlsx'

    peer_evaluator = PeerEvaluator(pd.read_excel(fexcel))
    peer_evaluator.check_missing_infomation()
    peer_evaluator.re_arrange_justification()
    peer_evaluator.convert_percentage_weightage(scale_type=5)


    df=peer_evaluator.aggregate_each_peers()
    save_output_excel(df, fname='2aaa023_11.xlsx', verbose=False)

fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_transform _22_23_fill.xlsx'

PE=PeerEvaluator(finput=fexcel, scale_type=5)
df=PE.process_dataframe()
save_output_excel(df, fname='other_2aaa023_11.xlsx', verbose=False)
h=1
