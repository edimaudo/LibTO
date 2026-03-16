# 2. Circulation
import plotly.express as px
df_circulation = dataframes['df_circulation']
annual_circulation = df_circulation.groupby('Year')['Circulation'].sum().reset_index()
fig_circulation = px.line(
    annual_circulation,
    x='Year',
    y='Circulation',
    title='Annual Circulation',
    labels={'Circulation': 'Total Circulation'}
)
fig_circulation.show()