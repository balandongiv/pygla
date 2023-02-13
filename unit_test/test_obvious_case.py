"""
gla module for Peer Evaluation

This module includes two classes: PeerEvaluator and helper. The PeerEvaluator class allows the user to input a spreadsheet of peer evaluations and calculate scores based on the specified scale type. The helper class includes a function to save the output to an excel file.

To use the module, first import the PeerEvaluator class and the save_output_excel function from the helper class. Then, specify the input excel file path and the scale type. Create an instance of the PeerEvaluator class and run the process_dataframe method to calculate scores. Finally, use the save_output_excel function to save the scores to an output excel file.


The input used in this test is similar with the peer input in the `test_peer_evaluator.py`.
The only diffrent is we load from the excel file.
"""

# Usage
import os

import pandas as pd

from gla.gla import PeerEvaluator
from gla.helper import save_output_excel

fpath_excel = r'C:\Users\balandongiv\IdeaProjects\pygla\doc\understanding_concept_excel_formula.xlsx'

fexcel='understand_concept.xlsx'
df = pd.read_excel(fpath_excel, sheet_name="input_data_scale_7")
df.to_excel(fexcel, index=0)


scale_type=7

# Create instance of PeerEvaluator class and process dataframe
PE = PeerEvaluator(finput=fexcel, scale_type=scale_type)
PE.process_dataframe()

# Save output to excel file
save_output_excel(PE.cal_score, fname='aunderstand_concept.xlsx', verbose=True)
os.remove(fexcel)