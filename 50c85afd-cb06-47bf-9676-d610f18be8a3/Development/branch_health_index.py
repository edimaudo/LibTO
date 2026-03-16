## Branch Health 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

df_visits = dataframes['df_visits']
df_total_visits = df_visits.groupby('BranchCode')['Visits'].sum().reset_index()
df_total_visits.rename(columns={'Visits': 'TotalVisits'}, inplace=True)

df_workstation_usage = dataframes['df_workstation_usage']
df_total_workstation_usage = df_workstation_usage.groupby('BranchCode')['Sessions'].sum().reset_index()
df_total_workstation_usage.rename(columns={'Sessions': 'TotalWorkstationUsage'}, inplace=True)

df_map_data = dataframes['df_map_data']
df_total_visits = df_total_visits 
df_total_workstation_usage = df_total_workstation_usage 

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

# Filter out non-physical / administrative / special branches
branches_to_exclude = [
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
df_health_index_data = df_health_index_data[
    ~df_health_index_data['BranchName'].isin(branches_to_exclude)
].reset_index(drop=True)

print(f"Branches after filtering: {len(df_health_index_data)}")

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

# ── Top 10 / Bottom 10 Library Health Index Bar Chart ──────────────────────────
_lhi = (
    df_health_index_data[['BranchName', 'LibraryHealthIndex']]
    .dropna(subset=['LibraryHealthIndex'])
    .sort_values('LibraryHealthIndex', ascending=False)
    .reset_index(drop=True)
)

# Top 10 descending (highest performers first)
_top10 = _lhi.head(10).copy()

# Bottom 10 ascending (lowest performers first, worst at the bottom of its chart)
_bot10 = _lhi.tail(10).sort_values('LibraryHealthIndex', ascending=True).copy()

_COLOR_TOP = '#2196F3'   # blue
_COLOR_BOT = '#FF5722'   # deep orange

fig_health_ranking = make_subplots(
    rows=1, cols=2,
    subplot_titles=('🏆 Top 10 Branches', '⚠️ Bottom 10 Branches'),
    horizontal_spacing=0.18,
)

# Top 10 — descending (highest at top of horizontal bar)
fig_health_ranking.add_trace(
    go.Bar(
        x=_top10['LibraryHealthIndex'],
        y=_top10['BranchName'],
        orientation='h',
        marker_color=_COLOR_TOP,
        text=_top10['LibraryHealthIndex'].round(2),
        textposition='outside',
        name='Top 10',
        showlegend=False,
    ),
    row=1, col=1,
)

# Bottom 10 — ascending (lowest at bottom of horizontal bar)
fig_health_ranking.add_trace(
    go.Bar(
        x=_bot10['LibraryHealthIndex'],
        y=_bot10['BranchName'],
        orientation='h',
        marker_color=_COLOR_BOT,
        text=_bot10['LibraryHealthIndex'].round(2),
        textposition='outside',
        name='Bottom 10',
        showlegend=False,
    ),
    row=1, col=2,
)

fig_health_ranking.update_layout(
    title={
        'text': 'Library Health Index — Top 10 & Bottom 10 Branches',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18},
    },
    height=520,
    width=1200,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=20, r=120, t=80, b=40),
    font=dict(size=12),
)

# Axis styling — top panel
fig_health_ranking.update_xaxes(
    title_text='Health Index',
    showgrid=True,
    gridcolor='#eeeeee',
    row=1, col=1,
)
fig_health_ranking.update_yaxes(
    autorange='reversed',   # highest value at the top
    tickfont=dict(size=11),
    row=1, col=1,
)

# Axis styling — bottom panel
fig_health_ranking.update_xaxes(
    title_text='Health Index',
    showgrid=True,
    gridcolor='#eeeeee',
    row=1, col=2,
)
fig_health_ranking.update_yaxes(
    tickfont=dict(size=11),
    row=1, col=2,
)

fig_health_ranking.show()
print("Health Index ranking chart rendered.")