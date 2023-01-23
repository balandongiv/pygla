

# Overview
This script includes several functions and a class for performing peer evaluations. The main function, PeerEvaluator, reads in a file, performs some data transformations, and allows for calculation of factors and grouping of data. The script also includes a function save_output_excel that saves the processed dataframe to an excel file, and a function calculate_factor that maps values of one dataframe column to another dataframe column based on a condition.

# Dependencies
pandas
itertools
gla.ref_map
argparse

# Usage
Initialize a PeerEvaluator object by passing in the input file and an optional scale type.


evaluator = PeerEvaluator(finput, scale_type)
Use the calculate_factor method to map values and calculate a factor.


evaluator.calculate_factor(df_stat)
Use the group_stat method to group the data and perform aggregation.


evaluator.group_stat()
Use the save_output_excel function to save the processed dataframe to an excel file.

save_output_excel(evaluator.df, fname='result.xlsx', verbose=False)


# Note
save_output_excel function has an option to remove certain columns from the dataframe before saving, by setting the 'verbose' parameter to False.
calculate_factor function maps values of one dataframe column to another dataframe column based on a condition.
group_stat function groups the dataframe by a specific column, performs aggregation and renames the column.
PeerEvaluator class uses read_file_transform method to read in a file and perform data transformations.