"""
gla module for Peer Evaluation

This module includes two classes: PeerEvaluator and helper. The PeerEvaluator class allows the user to input a spreadsheet of peer evaluations and calculate scores based on the specified scale type. The helper class includes a function to save the output to an excel file.

To use the module, first import the PeerEvaluator class and the save_output_excel function from the helper class. Then, specify the input excel file path and the scale type. Create an instance of the PeerEvaluator class and run the process_dataframe method to calculate scores. Finally, use the save_output_excel function to save the scores to an output excel file.

"""

# Usage

from gla.gla import PeerEvaluator
from gla.helper import save_output_excel

# Input excel file path and scale type
fexcel = r'C:\Users\balandongiv\IdeaProjects\pygla\unit_test\peer_assessment.xlsx'
scale_type=5

# Create instance of PeerEvaluator class and process dataframe
PE = PeerEvaluator(finput=fexcel, scale_type=scale_type)
PE.process_dataframe()

# Save output to excel file
save_output_excel(PE.cal_score, fname='_11.xlsx', verbose=False)