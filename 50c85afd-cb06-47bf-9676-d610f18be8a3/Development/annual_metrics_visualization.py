import plotly.express as px

# Branches to exclude (non-physical / virtual / special services)
BRANCHES_TO_EXCLUDE = [
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

# 1. Card Registrations
df_card_registrations = dataframes['df_card_registrations']

# Filter out non-physical/virtual branches by joining with general info on BranchCode
_branch_filter = df_general_info[~df_general_info['BranchName'].isin(BRANCHES_TO_EXCLUDE)][['BranchCode']]
df_card_registrations = df_card_registrations[df_card_registrations['BranchCode'].isin(_branch_filter['BranchCode'])]

annual_registrations = df_card_registrations.groupby('Year')['Registrations'].sum().reset_index()
fig_registrations = px.line(
    annual_registrations,
    x='Year',
    y='Registrations',
    title='Annual Card Registrations',
    labels={'Registrations': 'Total Registrations'}
)
fig_registrations.show()