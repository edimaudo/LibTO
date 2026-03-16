# 4. Workstation Usage
import plotly.express as px
df_workstation_usage = dataframes['df_workstation_usage']
annual_workstation_usage = df_workstation_usage.groupby('Year')['Sessions'].sum().reset_index()
fig_workstation_usage = px.line(
    annual_workstation_usage,
    x='Year',
    y='Sessions',
    title='Annual Workstation Usage',
    labels={'Sessions': 'Total Sessions'}
)
fig_workstation_usage.show()