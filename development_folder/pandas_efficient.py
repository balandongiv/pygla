import pandas as pd
from itertools import product

drop_cols_opt = ['dgroup_name',
                 ('percentage_trans', 'research_information_gathering'),
                 ('percentage_trans', 'creative_input'),
                 ('percentage_trans', 'coperation_within_group'),
                 ('percentage_trans', 'creative_input'),
                 ('percentage_trans', 'coperation_within_group'),
                 ('percentage_trans', 'communication'),
                 ('percentage_trans', 'contribution_quality'),
                 ('percentage_trans', 'meeting_attendance'),
                 ('percentage_trans', 'creative_input'),
                 'sum_percentage_all_elements',
                 'row_const',
                 'group_summation',
                 'nmember']

d_agg_calculation = {'peer_name': 'first',
                     # 'name': 'first',
                     'group_name': 'first',
                     'research_information_gathering': 'mean',
                     'creative_input': 'mean',
                     'coperation_within_group': 'mean',
                     'communication': 'mean',
                     'contribution_quality': 'mean',
                     'meeting_attendance': 'mean',
                     'feedback': '\n'.join,
                     'justification_annom': '\n'.join}
remap_values = {"Terrible (0)": '0',
                "Very Poor (1)": '1',
                "Poor (2)": '2',
                "Adequate (3)": '3',
                "Good (4)": '4',
                "Very Good (5)": '5',
                "Excellent (6)": '6'}

col_name = ['id', 'start_time', 'completion_time', 'email', 'name', 'assessor_student_id', 'group_name',
            'peer_name', 'peer_student_id', 'research_information_gathering', 'creative_input',
            'coperation_within_group', 'communication', 'contribution_quality',
            'meeting_attendance', 'justification']

n_element = ['research_information_gathering',
             'creative_input',
             'coperation_within_group',
             'communication',
             'contribution_quality',
             'meeting_attendance']

const_val = dict(research_information_gathering=15,
                 creative_input=20,
                 coperation_within_group=15,
                 communication=15,
                 contribution_quality=20,
                 meeting_attendance=15)


def extract_each_peers(df, dcols, std_col):
    expanded_col = list(std_col) + list(dcols)
    dd = df.iloc[:, expanded_col]
    dd.columns = col_name
    return dd


def collapse_cols_representation(df, cols):
    indices_s = [i for i, s in enumerate(cols) if 'Peer Name' in s]

    indices_e = [i for i, s in enumerate(cols) if 'Justification for Peer' in s]

    indices_e = [x.__add__(1) for x in indices_e]

    col_int = [range(x, y) for x, y in zip(indices_s, indices_e)]
    std_col = range(0, indices_s[0])

    all_df = [extract_each_peers(df, dcols, std_col) for dcols in col_int]

    df1 = pd.concat(all_df).reset_index(drop=True)


    for delement in n_element:
        df1[delement] = df1[delement].str.extract('\((\d+)\)')

    # df1.replace(remap_values, inplace=True)

    return df1


def read_file_transform(finput=None):
    df = pd.read_excel(finput)
    cols = df.columns.tolist()

    if len(cols) > 13:  # Typically, the number of cols from a MForm is more than 50
        return collapse_cols_representation(df, cols)
    else:
        '''
        manually data entry into the required cols format
        name	group_name	peer_name	peer_student_id	research_information_gathering	creative_input	coperation_within_group	communication	contribution_quality	meeting_attendance	justification

        '''
        g=1
        return df


def convert_percentage_weightage(df, scale_type=None):
    """
    Currently, the code only has been tested for scale 5 and 7
    As per previous practice, Terrible (0) would not yield any grade
    :param df:
    :param scale_type:
    :return:
    """
    if scale_type is None:
        # Or to enforce infer?
        raise 'Please input the scale type to avoid normalization error'
    elif scale_type == 7:
        # minus 1 since we dont want to assign any mark to the lowest point
        # There can be 5 points scale or 7 points scale. Therefore, the value revise_max_val can be either 5 or 4
        revise_max_val = 6
    elif scale_type == 5:
        revise_max_val = 4

    cols = pd.Index(const_val.keys())
    mi = pd.MultiIndex.from_product([['percentage_trans'], cols])
    df[mi] = df[cols] * pd.Series(const_val) / revise_max_val
    return df


def re_arrange_justification(df, n_element):
    df["feedback"] = df["name"].str.cat(df["justification"], sep="-->")
    df['justification'] = df['justification'].apply(lambda x: "'" + str(x) + "'")
    # df = df.set_index(['peer_name', 'peer_student_id'])
    df = df.set_index(['peer_student_id', 'assessor_student_id'])
    df = df.sort_index(ascending=True)
    df.index = pd.MultiIndex.from_tuples(df.index.tolist())
    df[n_element] = df[n_element].astype(int)
    df['justification_annom'] = df['justification'].astype(str)
    # print(df1.dtypes)
    return df


def group_stat(df):
    df_stat = df.groupby(level=0).agg({'row_const': 'sum',
                                       'sum_percentage_all_elements': 'sum'})

    df_stat = df_stat.reset_index().rename(columns={'index': 'group_name'})
    return df_stat


def calculate_factor(df, df_stat):
    # https://stackoverflow.com/questions/70004051/assign-values-of-one-dataframe-column-to-another-dataframe-column-based-on-condi?rq=1
    df['group_summation'] = df['dgroup_name'].map(
        dict(zip(df_stat['group_name'], df_stat['sum_percentage_all_elements']))).fillna(0)
    df['nmember'] = df['dgroup_name'].map(dict(zip(df_stat['group_name'], df_stat['row_const']))).fillna(0)

    df['weightage'] = (df['nmember'] / df['group_summation']) * df[('sum_percentage_all_elements')]
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

    df_raw = re_arrange_justification(df_raw, n_element)
    df = df_raw.groupby(level=0).agg(d_agg_calculation)

    df = convert_percentage_weightage(df, scale_type=scale_type)

    col_to_sum = list(product(['percentage_trans'], n_element))
    df[('sum_percentage_all_elements')] = df[col_to_sum].sum(axis=1)
    df['row_const'] = 1  # Use to calculate the number of group members

    # Assign back the student ID
    df = df.reset_index().rename(columns={'index': 'std_id', 'peer_name': 'std_name'})

    df['dgroup_name'] = df['group_name']
    df = df.set_index(['group_name', 'std_id'])

    df_stats = group_stat(df)

    df = calculate_factor(df, df_stats)

    return df


def save_output_excel(df, fname=None, verbose=False):
    # Move the feedback section at the last column for readability
    df.insert(len(df.columns) - 1, 'feedback', df.pop('feedback'))
    df.insert(len(df.columns) - 1, 'justification_annom', df.pop('justification_annom'))

    if fname is None:
        fname = 'result.xlsx'

    if not verbose:
        df.drop(drop_cols_opt, axis=1, inplace=True)
    df.reset_index(drop=False, inplace=True)
    ncols = tuple(df.columns.tolist())
    # df.columns = pd.MultiIndex.from_product(
    #     [("Complete Data Backup\n test",), ncols])
    # dgroup_name

    df.to_excel(fname, index=0)
def check_missing_infomation(df):
    '''
    TODO:
    Sometime, for manual data entry, the student ID and peer ID is missing,
    for the time being, we drop student/peer with ID.

    However, we should raise warning for this serious issue

    :param df:
    :return:
    '''
    df = df.dropna()
    return df


if __name__ == '__main__':
    # fexcel=r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_assessment.xlsx'
    # fexcel = r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_assessment_7_scale.xlsx'
    # fexcel = r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_transform.xlsx'
    fexcel=r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_transform _22_23_fill.xlsx'
    df = read_file_transform(fexcel)
    df=check_missing_infomation(df)
    df1 = calculate_factors(df, scale_type=5)

    save_output_excel(df1, fname='2023_11.xlsx', verbose=False)
