import os
import pandas as pd
from fuzzywuzzy import fuzz
import re

def extract_group_number(group_value):
    """
    Extracts the numeric part of a group name (e.g., 'Group 16' → 16).

    Parameters:
        group_value (str): The group value as a string.

    Returns:
        int or None: The extracted group number or None if not found.
    """
    if pd.isna(group_value) or not isinstance(group_value, str):
        return None
    match = re.search(r'\d+', group_value)  # Extract the first numeric value found
    return int(match.group()) if match else None

def find_column(df, target):
    """
    Searches for a column in df whose normalized name matches the target string.

    Parameters:
        df (pd.DataFrame): DataFrame in which to search for the column.
        target (str): The target column name to find.

    Returns:
        str or None: The original column name if found, else None.
    """
    for col in df.columns:
        normalized = col.strip().strip('"').strip().lower()
        if normalized == target.lower():
            return col
    return None

def find_id_columns(df):
    """
    Identify all columns in df that might contain student IDs (peer assessment columns).

    Parameters:
        df (pd.DataFrame): The log file DataFrame.

    Returns:
        list: List of column names that contain student IDs.
    """
    return [col for col in df.columns if "peer student id" in col.lower()]

def check_discrepancies_with_nlp(output_path, master_path, log_path, threshold=50, consider_group=True):
    """
    Check discrepancies between the output file (with std_id) and the master list (with student_id).
    Then find the mistake maker from the log file (ST00602 file) by dynamically searching for
    which column contains the incorrect ID.

    Uses fuzzy matching to suggest the correct ID and retrieve the corresponding student name.
    If `consider_group` is True, it ensures the proposed student is from the same group as the mistake maker.

    Returns:
        pd.DataFrame: DataFrame with mistake maker, incorrect std_id, suggested correct ID,
                      real student name, and confidence level.
    """
    # Read the files
    df_output = pd.read_excel(output_path)
    df_master = pd.read_excel(master_path)
    df_log = pd.read_excel(log_path)

    # Extract group columns
    group_master_col = find_column(df_master, "group")
    group_log_col = find_column(df_log, "group name")

    if group_master_col and group_log_col:
        df_master[group_master_col] = df_master[group_master_col].astype(str).apply(extract_group_number)
        df_log[group_log_col] = df_log[group_log_col].astype(str).apply(extract_group_number)

    # -----------------------------------
    # Step 1. Identify incorrect std_id
    # -----------------------------------
    # Find IDs in output_6.xlsx that are NOT in student_group.xlsx
    incorrect_df = df_output[~df_output['std_id'].isin(df_master['student_id'])].copy()
    incorrect_df.rename(columns={'std_id': 'Incorrect_std_id'}, inplace=True)

    # If there are no incorrect std_ids, return an empty DataFrame
    if incorrect_df.empty:
        return pd.DataFrame(columns=['Mistake_Maker', 'Incorrect_std_id', 'Proposed_Correct_id', 'Proposed_Student_Name', 'Confidence_Level'])

    # -----------------------------------
    # Step 2. Locate the mistake maker dynamically
    # -----------------------------------
    id_columns = find_id_columns(df_log)
    mistake_maker_col = find_column(df_log, 'name')

    mistake_makers = []

    if mistake_maker_col:
        for _, row in incorrect_df.iterrows():
            incorrect_id = str(row['Incorrect_std_id'])
            mistake_maker = "Unknown"
            mistake_maker_group = None

            for id_col in id_columns:
                matching_rows = df_log[df_log[id_col].astype(str) == incorrect_id]

                if not matching_rows.empty:
                    mistake_maker = matching_rows[mistake_maker_col].values[0]
                    if group_log_col:
                        mistake_maker_group = matching_rows[group_log_col].values[0]  # Extract group number
                    break  # Stop searching once we find the first match

            mistake_makers.append({'Incorrect_std_id': incorrect_id, 'Mistake_Maker': mistake_maker, 'Group_Number': mistake_maker_group})

    mistake_maker_df = pd.DataFrame(mistake_makers)

    # -----------------------------------
    # Step 3. Suggest correct IDs using NLP (Fuzzy Matching)
    # -----------------------------------
    suggestions = []
    df_master['student_id'] = df_master['student_id'].astype(str)

    for _, row in mistake_maker_df.iterrows():
        incorrect_id = row['Incorrect_std_id']
        mistake_maker_group = row['Group_Number']
        best_match = None
        best_score = -1

        if consider_group and group_master_col:
            # Filter master list to only students in the same group
            group_filtered_master = df_master[df_master[group_master_col] == mistake_maker_group]
        else:
            # Use the full master list if group-based filtering is disabled
            group_filtered_master = df_master

        for _, master_row in group_filtered_master.iterrows():
            master_id = master_row['student_id']
            score = fuzz.ratio(incorrect_id, master_id)
            if score > best_score:
                best_score = score
                best_match = master_row

        # Only accept the suggestion if the score meets the threshold; otherwise, no suggestion.
        if best_score < threshold:
            proposed_id = "No suggestion"
            proposed_name = "No suggestion"
        else:
            proposed_id = best_match['student_id']
            proposed_name = best_match['student_name']

        suggestions.append({
            'Incorrect_std_id': incorrect_id,
            'Proposed_Correct_id': proposed_id,
            'Proposed_Student_Name': proposed_name,
            'Confidence_Level': best_score
        })

    suggestions_df = pd.DataFrame(suggestions)

    # -----------------------------------
    # Step 4. Merge mistake maker with suggestions
    # -----------------------------------
    final_df = pd.merge(mistake_maker_df, suggestions_df, on='Incorrect_std_id', how='left').drop(columns=['Group_Number'])

    return final_df

if __name__ == '__main__':
    # Define file paths
    fexcel = r'C:\Users\balan\IdeaProjects\pygla\basic_physic\ST00602 Basic Physic 2024_2025 1(1).xlsx'
    master_list = r'C:\Users\balan\IdeaProjects\pygla\basic_physic\student_group.xlsx'
    save_path = os.path.join(os.path.split(fexcel)[0], 'output_6.xlsx')

    # Run the discrepancy check with NLP (fuzzy matching)
    final_discrepancies_df = check_discrepancies_with_nlp(save_path, master_list, fexcel, threshold=50, consider_group=True)

    # Display the results
    print("Final Suggestions for Incorrect IDs:")
    print(final_discrepancies_df)

    # Save the results to an Excel file
    output_suggestions_file = os.path.join(os.path.split(fexcel)[0], 'final_suggestions.xlsx')
    final_discrepancies_df.to_excel(output_suggestions_file, index=False)
