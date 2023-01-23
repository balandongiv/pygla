
import pandas as pd
from itertools import product
def read_file(finput=None):
    df=pd.read_excel(finput)
    cols=df.columns.tolist()
    indices_s = [i for i, s in enumerate(cols) if 'Peers Student' in s]
    all_df=[]
    for dcols in indices_s :
        expanded_col=[dcols-1,dcols]
        dd=df.iloc[:,expanded_col]
        dd.columns=['peer_name','std_id']
        all_df.append(dd)

    df1 = pd.concat(all_df).reset_index(drop=True)
    df1=df1.dropna()
    newdf1 = df1.groupby(['peer_name','std_id']).first()
    newdf1=newdf1.reset_index()
    df1.drop_duplicates( "std_id" , keep='first')

    h=1

fexcel=r'C:\Users\balandongiv\IdeaProjects\krr\peer_assessment\peer_assessment.xlsx'
df=read_file(fexcel)