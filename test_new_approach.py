import pandas as pd

# Define file paths
input_path = r'C:\Users\balan\IdeaProjects\pygla\tutorial\ST00602 Basic Physic 2024_2025 1.xlsx'
output_path = r'C:\Users\balan\IdeaProjects\pygla\tutorial\Transformed_Peer_Evaluation1.xlsx'

# Load the Excel file
df = pd.read_excel(input_path)

# Prepare a list to store transformed data
transformed_data = []

# Define assessment components
assessment_components = [
    "Research & Information Gathering",
    "Creative Input",
    "Co-Operation Within Group",
    "Communication Withing Group",
    "Quality of Individual Contribution",
    "Attendance At Meeting"
]

# Iterate over each row in the original dataframe
for _, row in df.iterrows():
    for i in range(1, 8):  # Assuming up to 7 peers can be evaluated
        peer_name_col = f'Peer Name (P{i})\n'
        peer_id_col = f'Peer Student ID (P{i})\n'

        if peer_name_col in df.columns and pd.notna(row[peer_name_col]):
            # Extract peer-related data
            peer_data = {
                'Id': row['Id'],
                'Start time': row['Start time'],
                'Completion time': row['Completion time'],
                'Email': row['Email'],
                'Name': row['Name\n'],
                'Group Name': row['Group Name\n'],
                'Assessor Student ID': row['assessor student id\n'],
                'Peer Name': row[peer_name_col],
                'Peer Student ID': row[peer_id_col],
            }

            # Extract assessment components
            for comp in assessment_components:
                possible_cols = [
                    f'Assessment Component\n.{comp}{"" if i == 1 else i-1}',
                    f'Assessment Component\n.{comp}{i-1}',
                    f'Assessment Component\n.{comp}{i-1}\n'
                ]

                for col in possible_cols:
                    if col in df.columns and pd.notna(row[col]):
                        peer_data[comp] = row[col]
                        break
                else:
                    peer_data[comp] = None  # Ensure column presence even if missing

            # Extract justification and evaluation choice
            justification_col = f'Justification for Peer (P{i})\n'
            eval_col = f'Do you want to Evaluate Peer (P{i+1})\n' if i < 7 else None

            peer_data['Justification'] = row.get(justification_col, None)
            if eval_col and eval_col in df.columns:
                peer_data['Do you want to Evaluate Next Peer'] = row.get(eval_col, None)

            # Append to transformed data list
            transformed_data.append(peer_data)

# Convert to DataFrame and save
df_transformed = pd.DataFrame(transformed_data)
df_transformed.to_excel(output_path, index=False)

print(f"Transformed data saved to {output_path}")
