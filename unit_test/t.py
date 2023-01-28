from gla.gla import PeerEvaluator
from gla.helper import save_output_excel

fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_assessment.xlsx'
scale_type=5
PE = PeerEvaluator(finput=fexcel, scale_type=scale_type)
PE.process_dataframe()
save_output_excel(PE.cal_score, fname='_11.xlsx', verbose=False)