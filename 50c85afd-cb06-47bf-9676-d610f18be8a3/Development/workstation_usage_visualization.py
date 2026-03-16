# 4. Workstation Usage
import plotly.express as px
df_workstation_usage = dataframes['df_workstation_usage']

# BranchNames to exclude (non-physical/virtual/special services)
_branches_to_exclude = [
    'Answerline',
    'Bookmobile One',
    'Bookmobile Two',
    'Departmental Staff',
    'Home Library Service',
    'Interloan',
    'Literacy Deposits',
    'Merril Collection',
    'Osborne Collection',
    'Automated Phone System',
    'Sunnybrook Hospital',
    'Virtual Library',
]

# Filter out excluded branches by joining with branch general info
_branch_codes_to_exclude = df_general_info.loc[
    df_general_info['BranchName'].isin(_branches_to_exclude), 'BranchCode'
].tolist()
df_workstation_usage = df_workstation_usage[~df_workstation_usage['BranchCode'].isin(_branch_codes_to_exclude)]

annual_workstation_usage = df_workstation_usage.groupby('Year')['Sessions'].sum().reset_index()
fig_workstation_usage = px.line(
    annual_workstation_usage,
    x='Year',
    y='Sessions',
    title='Annual Workstation Usage',
    labels={'Sessions': 'Total Sessions'}
)
fig_workstation_usage.show()