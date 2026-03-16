# 3. Visits
import plotly.express as px
df_visits = dataframes['df_visits']
annual_visits = df_visits.groupby('Year')['Visits'].sum().reset_index()
fig_visits = px.line(
    annual_visits,
    x='Year',
    y='Visits',
    title='Annual Visits',
    labels={'Visits': 'Total Visits'}
)
fig_visits.show()