# 2. Circulation
import plotly.express as px
df_circulation = dataframes['df_circulation']

# Filter out non-physical/virtual branch names
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
df_circulation = df_circulation[~df_circulation['BranchName'].isin(_branches_to_exclude)]

annual_circulation = df_circulation.groupby('Year')['Circulation'].sum().reset_index()
fig_circulation = px.line(
    annual_circulation,
    x='Year',
    y='Circulation',
    title='Annual Circulation',
    labels={'Circulation': 'Total Circulation'}
)
fig_circulation.show()