import pandas as pd
from itertools import product

def read_file_transform():
    fexcel=r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_assessment.xlsx'
    df=pd.read_excel(fexcel)
    cols=df.columns.tolist()

    col_int=[range(6,15),
             range(16,25),
             range(26,35)]
    std_col=range(0,6)
    col_name=['id','start_time','completion_time','email','name','group_name','peer_name',
              'peer_student_id','research_information_gathering','creative_input',
              'coperation_within_group','communication','contribution_quality',
              'meeting_attendance','justification']
    all_df=[]
    for dcols in col_int:
        expanded_col=list(std_col)+list(dcols)
        dd=df.iloc[:,expanded_col]
        dd.columns=col_name
        all_df.append(dd)

    df1 = pd.concat(all_df).reset_index(drop=True)

    remap_values = {"Option 1" : '0',
                    "Option 2" : '1',
                    "Option 3" : '2',
                    "Option 4" : '3',
                    "Option 5" : '4',
                    "Option 6" : '5',
                    "Option 7" : '6', }
    # df1.replace(remap_values,value='--',inplace=True)
    df1.replace(remap_values, inplace=True)

    return  df1
def transform_representation(df1):
    n_name=['std1','std2','std3','std4']
    n_element=['research_information_gathering',
               'creative_input',
               'coperation_within_group',
               'communication',
               'contribution_quality',
               'meeting_attendance',
               'justification']


    col_n=list(product(n_element,n_name))
    # col_n=[f"{x}__{y}" for x,y in product(n_name, n_element)]
    col_a=[('name','rr'),('name_id','qqq')]+col_n

    df_n = pd.DataFrame(columns=col_a,
                        index=n_name)

    for ele,main_p in col_n:
        # main_p,ele=ydex.split('__')
        for xdex in n_name:
            if main_p!= xdex:

                try:
                    dval=df1.loc[(df1['name'] == main_p) & (df1['peer_name'] ==xdex),ele].values[0]
                    df_n.at[xdex, (ele,main_p )] = dval
                    gg=1
                except IndexError:
                    pass



    return  df_n




df1=read_file_transform()
df_n=transform_representation(df1)


ls_cols_to_average=df_n.columns.tolist()
kw_p=['justification','name','name_id']
ele_average=[]
for dpair_peers in ls_cols_to_average:

    if dpair_peers[0] not in kw_p:
        ele_average.append(dpair_peers)


# https://stackoverflow.com/questions/48272452/sum-columns-by-level-in-a-pandas-multiindex-dataframe
df_n[ele_average] = df_n[ele_average].apply(lambda x: pd.to_numeric(x, errors='coerce'))
# df_n[('summation_typical','ce')] = df_n[ele_average].sum(axis=1)

n_name=['std1','std2','std3','std4']
a=list(product(['research_information_gathering'],n_name))
n_element_f=['research_information_gathering',
             'creative_input',
             'coperation_within_group',
             'communication',
             'contribution_quality',
             'meeting_attendance']

# for delemnt in n_element_f:
#     a=list(product([delemnt],n_name))
#     df_n[('comb',delemnt)] = df_n[a].sum(axis=1)

for delemnt in n_element_f:
    a=list(product([delemnt],n_name))
    df_n[('average',delemnt)] = df_n[a].mean(axis=1)


const_val=dict(research_information_gathering=15,
               creative_input=20,
               coperation_within_group=15,
               communication=15,
               contribution_quality=20,
               meeting_attendance=15)

# There can be 5 points scale or 7 points scale. Therefore, the value max_val can be either 5 or 7
max_val=6

# minus 1 since we dont want to assign any mark to the lowest point
revise_max_val=max_val-1
# Convert into percentage
for dpair in const_val:
    ttt=const_val[dpair]
    con_t=ttt/revise_max_val
    df_n[('percentage_trans',dpair)]=df_n[('average',dpair)]*con_t

aeee=list(product(['percentage_trans'],n_element_f))
df_n[('sum_percentage_all_elements','')] = df_n[aeee].sum(axis=1)
nsbj=len(df_n)

ntotal= df_n[('sum_percentage_all_elements','')].sum(axis=0)
df_n[('factor','')]=df_n[('sum_percentage_all_elements','')]*nsbj/ntotal
# df_n[('factor','')]=df_n[('sum_t_group','')]/ntotal
nweight= df_n[('factor','')].sum(axis=0)
df_n.to_excel('result_v.xlsx')
g=1