import pandas as pd
from gla.gla import PeerEvaluator
'''
Test if std33 did not provide any assessment
'''
data = [['std21', 21, 99, 'std22', 22, 7, 7, 7, 7, 7, 7, 'STD21 comment to std22'],
        ['std21', 21, 99, 'std23', 23, 4, 4, 4, 4, 4, 4, 'STD21 comment to std23'],
        ['std22', 22, 99, 'std21', 21, 3, 3, 3, 3, 3, 3, 'STD22 comment to std21'],
        ['std22', 22, 99, 'std23', 23, 1, 4, 4, 4, 4, 4, 'STD22 comment to std23'],
        ]
columns_to_keep = ['std_name',
                   'research_information_gathering',
                   'creative_input',
                   'cooperation_within_group',
                   'communication',
                   'contribution_quality',
                   'meeting_attendance',
                   'group_summation',
                   'weightage',
                   ]
df = pd.DataFrame(data, columns=['name', 'assessor_student_id', 'group_name', 'peer_name', 'peer_student_id',
                                 'research_information_gathering', 'creative_input', 'cooperation_within_group',
                                 'communication', 'contribution_quality', 'meeting_attendance', 'justification'])

print(df)

fpath_excel = 'ttcase_all.xlsx'

df.to_excel(fpath_excel)

scale_type = 7

PE = PeerEvaluator(finput=fpath_excel, scale_type=scale_type)
PE.process_dataframe()
df_n = PE.cal_score

df_n = df_n.loc[:, columns_to_keep].reset_index(drop=True)
'''
0.556844548
1.670533643
0.77262181

'''
