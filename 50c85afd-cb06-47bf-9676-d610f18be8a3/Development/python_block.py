## Branch Health 

df_visits = dataframes['df_visits']
df_total_visits = df_visits.groupby('BranchCode')['Visits'].sum().reset_index()
df_total_visits.rename(columns={'Visits': 'TotalVisits'}, inplace=True)

df_workstation_usage = dataframes['df_workstation_usage']
df_total_workstation_usage = df_workstation_usage.groupby('BranchCode')['Sessions'].sum().reset_index()
df_total_workstation_usage.rename(columns={'Sessions': 'TotalWorkstationUsage'}, inplace=True)

df_map_data = dataframes['df_map_data']
df_total_visits = df_total_visits # Already created in previous steps
df_total_workstation_usage = df_total_workstation_usage # Already created in previous steps

# Merge df_map_data with df_total_visits
df_health_index_data = pd.merge(
    df_map_data,
    df_total_visits,
    on='BranchCode',
    how='left'
)

# Merge the result with df_total_workstation_usage
df_health_index_data = pd.merge(
    df_health_index_data,
    df_total_workstation_usage,
    on='BranchCode',
    how='left'
)

# Fill NaN values in TotalVisits and TotalWorkstationUsage with 0
# This assumes that if a branch does not appear in the visits/workstation usage data,
# it means it had 0 visits/sessions for those metrics.
df_health_index_data['TotalVisits'].fillna(0, inplace=True)
df_health_index_data['TotalWorkstationUsage'].fillna(0, inplace=True)

# Display head and info of the merged DataFrame
print("--- Merged DataFrame for Health Index Calculation ---")
print("\ndf_health_index_data.head():")
print(df_health_index_data.head())

print("\ndf_health_index_data.info():")
df_health_index_data.info()

# Calculate the 'Library Health Index'
# Ensure SquareFootage is not zero to avoid division by zero errors.
# If SquareFootage is 0 or NaN, the index will be NaN.
df_health_index_data['LibraryHealthIndex'] = (
    df_health_index_data['TotalVisits'] + df_health_index_data['TotalWorkstationUsage']
) / df_health_index_data['SquareFootage']

# Display head and info of the DataFrame with the new index
print("--- DataFrame with Library Health Index ---")
print("\ndf_health_index_data.head():")
print(df_health_index_data.head())

print("\ndf_health_index_data.info():")
df_health_index_data.info()

# Add the updated DataFrame back to the dataframes dictionary
#dataframes['df_health_index_data'] = df_health_index_data