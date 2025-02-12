"""
gla module for Peer Evaluation

This module includes two classes: PeerEvaluator and helper. The PeerEvaluator class allows the user to input a spreadsheet of peer evaluations and calculate scores based on the specified scale type. The helper class includes a function to save the output to an excel file.

To use the module, first import the PeerEvaluator class and the save_output_excel function from the helper class. Then, specify the input excel file path and the scale type. Create an instance of the PeerEvaluator class and run the process_dataframe method to calculate scores. Finally, use the save_output_excel function to save the scores to an output excel file.

"""
import os.path

from gla.gla import PeerEvaluator
from gla.helper import save_output_excel



# Input excel file path and scale type
fexcel = r'C:\Users\balan\IdeaProjects\pygla\basic_physic\ST00602 Basic Physic 2024_2025 1(1).xlsx'
save_path=os.path.join(os.path.split(fexcel)[0], 'output_6.xlsx')
master_list=r"C:\Users\balan\IdeaProjects\pygla\basic_physic\student_group.xlsx"
scale_type=7

# Create instance of PeerEvaluator class and process dataframe
PE = PeerEvaluator(finput=fexcel, scale_type=scale_type)
PE.process_dataframe()

# Save output to excel file
save_output_excel(PE.cal_score, fname=save_path, verbose=False)