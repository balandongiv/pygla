
from gla.gla import PeerEvaluator
from gla.helper import save_output_excel

fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_transform _22_23_fill.xlsx'
peer_evaluator = PeerEvaluator(pd.read_excel(fexcel))
peer_evaluator.check_missing_infomation()
peer_evaluator.re_arrange_justification()
peer_evaluator.convert_percentage_weightage(scale_type=5)


df=peer_evaluator.aggregate_each_peers()
save_output_excel(df, fname='2aaa023_11.xlsx', verbose=False)