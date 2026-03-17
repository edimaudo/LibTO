# Setup Libraries
import pandas as pd
import plotly.express as px

# Load Data
files_to_load = {
    'df_neighbourhoods': 'Neighbourhoods.csv',
    'df_general_info': 'tpl-branch-general-information-2023.csv',
    'df_space_rentals': 'tpl-branch-space-rentals-2024.csv',
    'df_card_registrations': 'tpl-card-registrations-annual-by-branch.csv',
    'df_circulation': 'tpl-circulation-annual-by-branch.csv',
    'df_visits': 'tpl-visits-annual-by-branch.csv',
    'df_workstation_usage': 'tpl-workstation-usage-annual-by-branch.csv'
}

# Dictionary to store DataFrames
dataframes = {}

# Load each file, display head, info, missing values, and duplicates
for df_name, file_path in files_to_load.items():
    print(f"\n--- Processing {df_name} from {file_path} ---")
    try:
        df = pd.read_csv(file_path)
        dataframes[df_name] = df

        print(f"\n{df_name}.head():")
        print(df.head())

        print(f"\n{df_name}.info():")
        df.info()

        print(f"\nMissing values in {df_name}:")
        print(df.isnull().sum())

        print(f"\nDuplicate rows in {df_name}:")
        print(df.duplicated().sum())

    except Exception as e:
        print(f"Error loading or processing {file_path}: {e}")

# Overview
df_general_info = dataframes['df_general_info']
df_space_rentals = dataframes['df_space_rentals']

# Create a new column 'Extracted_BranchName' by extracting the first word from the 'Name' column
df_space_rentals['Extracted_BranchName'] = df_space_rentals['Name'].apply(lambda x: x.split(' ')[0])

# Perform a left merge using 'BranchName' from df_general_info and 'Extracted_BranchName' from df_space_rentals
df_branch_info_with_rentals = pd.merge(
    df_general_info,
    df_space_rentals,
    left_on='BranchName',
    right_on='Extracted_BranchName',
    how='left'  # Use a left merge to keep all general branch info
)

# Add the new DataFrame to the dataframes dictionary
dataframes['df_branch_info_with_rentals'] = df_branch_info_with_rentals

print("\n--- Merged DataFrame: df_branch_info_with_rentals ---")
print("\ndf_branch_info_with_rentals.head():")
print(df_branch_info_with_rentals.head())

print("\ndf_branch_info_with_rentals.info():")
df_branch_info_with_rentals.info()

df_general_info = dataframes['df_general_info']
df_neighbourhoods = dataframes['df_neighbourhoods']

# Merge df_general_info and df_neighbourhoods
df_merged_geo = pd.merge(
    df_general_info,
    df_neighbourhoods,
    left_on='NBHDNo',
    right_on='AREA_ID',
    how='left'
)

# Add the new DataFrame to the dataframes dictionary
dataframes['df_merged_geo'] = df_merged_geo

print("--- Merged DataFrame: df_merged_geo ---")
print("\ndf_merged_geo.head():")
print(df_merged_geo.head())

print("\ndf_merged_geo.info():")
df_merged_geo.info()
