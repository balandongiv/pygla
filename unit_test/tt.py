from gla.gla import PeerEvaluator
from gla.helper import save_output_excel

# Create instance of PeerEvaluator class and process dataframe
PE = PeerEvaluator(finput='peer.xlsx', scale_type=7)
PE.process_dataframe()

save_output_excel(PE.cal_score, fname='output.xlsx', verbose=False)