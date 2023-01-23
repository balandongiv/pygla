
import pandas as pd
import numpy as np
np.random.seed(0)


cosl_ori=['ID', 'St ti', 'Comp time', 'Email', 'Name', 'Gr Name\n',
   'As Na (P1)\n', 'Fr ID (P1)\n', '        Role   & royce ', 'Cradle insigt', 'Co-exist network', 'Ample Tree (P1)\n',
   'As Na (P2)\n', 'Fr ID (P2)\n', '        Role   & royce 2', 'Cradle insigt2', 'Co-exist network2', 'Ample Tree (P2)\n',
   'As Na (P3)\n', 'Fr ID (P3)\n', '        Role   & royce 3', 'Cradle insigt3', 'Co-exist network3', 'Ample Tree (P3)\n']

df = pd.DataFrame(data=np.random.randint(5, size=(3, 24)),
                  columns=cosl_ori)
cols=df.columns.tolist()
indices_s = [i for i, s in enumerate(cols) if 'As Na' in s]

indices_e = [i for i, s in enumerate(cols) if 'Ample Tree' in s]

indices_e=[x.__add__(1) for x in indices_e]

col_int=[range(x,y) for x,y in zip(indices_s,indices_e)]
std_col=range(0,6)

col_name=['id','st_ti','comp_ti','email','name','gr_na','as_na',
          'fr_id','role_royce','cradle_insight',
          'coexist_net','ample_tree']
all_df=[]
for dcols in col_int:
    expanded_col=list(std_col)+list(dcols)
    dd=df.iloc[:,expanded_col]
    dd.columns=col_name
    all_df.append(dd)

df_expected_output = pd.concat(all_df).reset_index(drop=True)
