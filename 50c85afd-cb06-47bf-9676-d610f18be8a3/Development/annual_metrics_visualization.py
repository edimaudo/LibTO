import plotly.express as px

# 1. Card Registrations
df_card_registrations = dataframes['df_card_registrations']
annual_registrations = df_card_registrations.groupby('Year')['Registrations'].sum().reset_index()
fig_registrations = px.line(
    annual_registrations,
    x='Year',
    y='Registrations',
    title='Annual Card Registrations',
    labels={'Registrations': 'Total Registrations'}
)
fig_registrations.show()
