# import pandas as pd
# df = pd.DataFrame(data=[[1,2,4,5,1,2]], index=['a','b'])
# df.columns = pd.MultiIndex.from_product([['x', 'y', 'z'], list('ab')])
# df[('t','jj')]=4
# df[('xx','')]=400
# print(df)
# # df1=df.T
# # A=df1.groupby(level=[1],axis=0).sum()
# # df['ss']=df.groupby(level=0, axis=1).sum()
# g=1
ggg=list('ab')
import pandas as pd
import numpy as np
np.random.seed(0)

arr=np.random.randint(5, size=(6, 3))

df = pd.DataFrame(data=arr, index=[('s1','s2'),('s1','s3'),('s2','s3'),('s2','s4'),('s3','s1'),('s3','s4')],
                  columns=['a','fe','gg'])
df['new_text']='t'
print(df.dtypes)
# df2=df.groupby(level=0).agg(['mean'])
# print(df2)

# df[('t','')]=400
# df[('ts','text')]='a'
# h=df.groupby(level=0, axis=1).sum()
# g=1