import plotly.express as px

# Load circulation data from the dataframes dictionary (loaded in data_loading_preparation)
# df_circulation has columns: _id, Year, BranchCode, Circulation — NO BranchName column
_df_circ_raw = dataframes['df_circulation']

# Filter out non-physical/virtual branches by joining with df_general_info on BranchCode
# (BRANCHES_TO_EXCLUDE is available from upstream annual_metrics_visualization block)
_branch_codes_to_keep = df_general_info[~df_general_info['BranchName'].isin(BRANCHES_TO_EXCLUDE)][['BranchCode']]
_df_circ_filtered = _df_circ_raw[_df_circ_raw['BranchCode'].isin(_branch_codes_to_keep['BranchCode'])]

annual_circulation = _df_circ_filtered.groupby('Year')['Circulation'].sum().reset_index()

fig_circulation = px.line(
    annual_circulation,
    x='Year',
    y='Circulation',
    title='Annual Circulation',
    labels={'Circulation': 'Total Circulation'}
)
fig_circulation.show()
