import pandas as pd
from itertools import product

from gla.ref_map import CONST_VAL, COL_NAME, N_ELEMENT, D_AGG_CALCULATION, DROP_COLS_OPT

import argparse

# produce a more compact, efficient, PEP-compliant code using the following python code?
# improve the current docstring but maintain the meaning of the old docstring
def extract_each_peers(df, dcols, std_col):
    """
    This function extracts specific columns from a given dataframe and renames the columns.

    Parameters:
    - df (pandas dataframe): The dataframe that needs to be processed
    - dcols (list): A list of column indices that need to be extracted from the dataframe
    - std_col (list): A list of column indices that will be included in the extracted dataframe along with dcols

    Returns:
    - pandas dataframe: The extracted dataframe with renamed columns.

    """
    expanded_col = std_col + dcols
    return df.iloc[:, expanded_col].rename(columns=COL_NAME)


def collapse_cols_representation(df, cols):
    """
    This function extracts specific columns from a given dataframe, concatenates them, and extracts digits
     from the concatenated column.

    Parameters:
    - df (pandas dataframe): The dataframe that needs to be processed
    - cols (list): A list of column names in the dataframe

    Returns:
    - pandas dataframe: The processed dataframe

    """
    indices_s = [i for i, s in enumerate(cols) if 'Peer Name' in s]
    indices_e = [i for i, s in enumerate(cols) if 'Justification for Peer' in s]
    indices_e = [x + 1 for x in indices_e]
    col_int = [range(start, end) for start, end in zip(indices_s, indices_e)]
    std_col = range(0, indices_s[0])
    all_df = [extract_each_peers(df, dcols, std_col) for dcols in col_int]
    df1 = pd.concat(all_df).reset_index(drop=True)
    for delement in N_ELEMENT:
        df1[delement] = df1[delement].str.extract('\((\d+)\)')
    return df1


def read_file_transform(finput=None):
    """

    Parameters:
    - finput (str): The file name of the excel file that needs to be processed.

    Returns:
    - pandas dataframe: The processed dataframe.

    Note:
    - The input dataframe should have the columns: name, group_name, peer_name, peer_student_id, research_information_gathering, creative_input, coperation_within_group, communication, contribution_quality, meeting_attendance, justification.
    - If the input dataframe is less than 13 columns, it is assumed that it is in the correct format for further processing.



    """
    df = pd.read_excel(finput)
    cols = df.columns.tolist()
    return collapse_cols_representation(df, cols) if len(cols) > 13 else df


def convert_percentage_weightage(df, scale_type=None):
    """
        Normalizes the values of specific columns in a given dataframe using a given scale.
        The function has been tested for scale 5 and 7 and by default, the lowest point "Terrible (0)" will not yield any grade.
        The scale type can be either 5 or 7.

        Parameters:
        - df (pandas dataframe): The dataframe that needs to be processed
        - scale_type (int): The type of scale to be used (5 or 7)

        Returns:
        - pandas dataframe: The processed dataframe
        """

    if scale_type not in (5, 7):
        raise ValueError('Please input a valid scale type: 5 or 7, to avoid normalization error')
    revise_max_val = 6 if scale_type == 7 else 4
    cols = pd.Index(CONST_VAL.keys())
    mi = pd.MultiIndex.from_product([['percentage_trans'], cols])
    df[mi] = df[cols] * pd.Series(CONST_VAL) / revise_max_val
    return df


def re_arrange_justification(df, n_element):

    """
 This function processes the dataframe by creating a new column 'feedback', modifying the 'justification' column,
 setting the index, and converting the specific column to integer.

 Parameters:
 - df (pandas dataframe): The dataframe that needs to be processed
 - n_element (str): The name of the column that needs to be converted to integer

 Returns:
 - pandas dataframe: The processed dataframe

 """

    df["feedback"] = df["name"].str.cat(df["justification"], sep="-->")
    df["justification"] = "'" + df["justification"].astype(str) + "'"
    df = df.set_index(["peer_student_id", "assessor_student_id"])
    df = df.sort_index(ascending=True)
    df.index = pd.MultiIndex.from_tuples(df.index.tolist())
    df[n_element] = df[n_element].astype(int)
    df["justification_annom"] = df["justification"].astype(str)
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


def calculate_factor(df, df_stat):
    """


 This function maps values of one dataframe column to another dataframe column based on a condition.

    Parameters:
    - df (pandas dataframe): The dataframe that needs to be processed
    - df_stat (pandas dataframe): The dataframe that will be used as a reference for the mapping

    Returns:
    - pandas dataframe: The processed dataframe
    """
    # https://stackoverflow.com/questions/70004051/assign-values-of-one-dataframe-column-to-another-dataframe-column-based-on-condi?rq=1
    mapping = df_stat.set_index('group_name').to_dict()
    df['group_summation'] = df['dgroup_name'].map(mapping['sum_percentage_all_elements']).fillna(0)
    df['nmember'] = df['dgroup_name'].map(mapping['row_const']).fillna(0)
    df['weightage'] = (df['nmember'] / df['group_summation']) * df[('sum_percentage_all_elements')]
    return df


def save_output_excel(df, fname=None, verbose=False):

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

    # Move the feedback section at the last column for readability
    df.insert(len(df.columns) - 1, 'feedback', df.pop('feedback'))
    df.insert(len(df.columns) - 1, 'justification_annom', df.pop('justification_annom'))

    if fname is None:
        fname = 'result.xlsx'

    if not verbose:
        df.drop(DROP_COLS_OPT, axis=1, inplace=True)
    df.reset_index(drop=False, inplace=True)
    ncols = tuple(df.columns.tolist())
    # df.columns = pd.MultiIndex.from_product(
    #     [("Complete Data Backup\n test",), ncols])
    # dgroup_name

    df.to_excel(fname, index=0)


def check_missing_infomation(df):
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
    df = df.dropna()
    return df


def calculate_factors(df_raw, scale_type):
    """

    TODO
    1) Check for duplicate entries
    2) To check existence of compulsory columns

    :param df_raw:
    :param scale_type:
    :return:
    """

    df_raw = re_arrange_justification(df_raw, N_ELEMENT)
    df = df_raw.groupby(level=0).agg(D_AGG_CALCULATION)

    df = convert_percentage_weightage(df, scale_type=scale_type)

    col_to_sum = list(product(['percentage_trans'], N_ELEMENT))
    df[('sum_percentage_all_elements')] = df[col_to_sum].sum(axis=1)
    df['row_const'] = 1  # Use to calculate the number of group members

    # Assign back the student ID
    df = df.reset_index().rename(columns={'index': 'std_id', 'peer_name': 'std_name'})

    df['dgroup_name'] = df['group_name']
    df = df.set_index(['group_name', 'std_id'])

    df_stats = group_stat(df)

    df = calculate_factor(df, df_stats)

    return df

def create_parser():
    parser = argparse.ArgumentParser(description='Process peer assessment data')
    parser.add_argument('finput', type=str, help='file name of the excel file to be processed')
    parser.add_argument('-v', '--verbose', action='store_true', help='include additional information in the output file')
    parser.add_argument('-f', '--fname', type=str, default='result.xlsx', help='output file name')
    parser.add_argument('-s', '--scale_type', type=int, default=5, choices=[5,7], help='scale type for normalization')
    return parser

# if __name__ == '__main__':
#
#     """
#     This script reads an excel file, processes the dataframe using the read_file_transform function, checks for missing information using the check_missing_infomation function, normalizes the values using the calculate_factors function, and saves the output in an excel file.
#     """
#
#     parser = create_parser()
#     args = parser.parse_args()
#     df = read_file_transform(args.finput)
#     df = check_missing_infomation(df)
#     df1 = calculate_factors(df, scale_type=args.scale_type)
#
#     save_output_excel(df1, fname=args.fname, verbose=args.verbose)

if __name__ == '__main__':

    # fexcel=r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_assessment.xlsx'
    # fexcel = r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_assessment_7_scale.xlsx'
    # fexcel = r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_transform.xlsx'
    fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_transform _22_23_fill.xlsx'
    df = read_file_transform(fexcel)
    df = check_missing_infomation(df)
    df1 = calculate_factors(df, scale_type=5)

    save_output_excel(df1, fname='baseline_2023_11.xlsx', verbose=False)
