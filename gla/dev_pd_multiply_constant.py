import pandas as pd
import numpy as np
np.random.seed(0)

const_val=dict(a_b_c=15,
               dd_ee=20,
               ff_ff=15,
               abc=15,
               devb=20,)

df = pd.DataFrame(data=np.random.randint(5, size=(3, 6)),
                  columns=['id','a_b_c','dd_ee','ff_ff','abc','devb'])

reval=6

for dpair in const_val:
    df[('per_a',dpair)]=df[dpair]*const_val[dpair]/reval

print(df)
# cols = pd.Index(const_val.keys())
# # df[cols + '_per_a'] = df[cols] * pd.Series(const_val) / reval
# df[('_per_a',cols)] = df[cols] * pd.Series(const_val) / reval
# hh=1
