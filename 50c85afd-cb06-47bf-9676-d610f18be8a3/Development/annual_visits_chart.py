# 3. Visits
import plotly.express as px

# Branches to exclude (non-physical / virtual / special services)
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

# Get BranchCodes to exclude by joining with df_general_info
_exclude_codes = df_general_info.loc[
    df_general_info['BranchName'].isin(_branches_to_exclude), 'BranchCode'
].tolist()

df_visits = dataframes['df_visits']

# Filter out excluded branches
df_visits = df_visits[~df_visits['BranchCode'].isin(_exclude_codes)]

annual_visits = df_visits.groupby('Year')['Visits'].sum().reset_index()
fig_visits = px.line(
    annual_visits,
    x='Year',
    y='Visits',
    title='Annual Visits',
    labels={'Visits': 'Total Visits'}
)
fig_visits.show()