import pandas as pd
from itertools import product
name=['ali',
      'ali',
      'abu',
      'abu',
      'bobi',
      'bobi',
      ]

name_id=['1a',
         '1a',
         '1b',
         '1b',
         '1c',
         '1c',
         ]

is_pair=['abu',
         'bobi',
         'ali',
         'bobi',
         'ali',
         'abu',
         ]

group=['this_ga',
       'this_ga',
       'this_ga',
       'this_ga',
       'this_ga',
       'this_ga',
       ]

element_a=[1,
           4,
           7,
           10,
           13,
           30,
           ]

element_b=[2,
           5,
           8,
           11,
           15,
           35,
           ]
comment=['a',
        'b',
        'c',
        'ee',
        'tr',
        'zz',
        ]

df=pd.DataFrame(list(zip(name,name_id,is_pair,group,element_a,element_b,comment)),
                columns=['name','name_id','is_pair','group','elem_a','elem_b','elem_comm'])

n_name=['ali','abu','bobi']
n_element=['elem_aa','elem_2','elem_comm']



col_n=[f"{x}__{y}" for x,y in product(n_name, n_element)]
B = ['comm', 'BBB']
ele_average=[word for word in col_n if not any(bad in word for bad in B)]
col_a=['name','name_id']+col_n

df_n = pd.DataFrame(columns=col_a,
                  index=n_name)
# df_n=df_n.reset_index()
for ydex in col_n:
    main_p,ele=ydex.split('__')
    for xdex in n_name:
        if main_p!= xdex:

            for delement in ['elem_a','elem_b','elem_comm']:
                dval=df.loc[(df['name'] == main_p) & (df['is_pair'] ==xdex),ele].values[0]
                df_n.at[xdex, ydex] = dval
                hh=1

df_n['e'] = df_n[ele_average].sum(axis=1)
g=1