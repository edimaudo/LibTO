from utils import *
from data import *

st.title(APP_NAME)
st.header(OVERVIEW_HEADER)
st.write("LibTO is a civic intelligence app designed for Toronto denizens to get insights into the Toronto Public Library (TPL) Network")

# Calculate KPIs
# KPIs
num_libraries = len(physical)
avg_sq_ft = f"{physical['SquareFootage'].mean():,.0f}"
oldest_info = f"{oldest['BranchName']}"
avg_ws = f"{physical['Workstations'].mean():.0f}"
kidstop = f"{physical['KidsStop'].sum():.0f}"
leading_reading = f"{physical['LeadingReading'].sum():.0f}"
teen_council = f"{physical['TeenCouncil'].sum():.0f}"
youth_hub = f"{physical['YouthHub'].sum():.0f}"
adult_literacy = f"{physical['AdultLiteracyProgram'].sum():.0f}"

top_container = st.container()
bottom_container = st.container()

with top_container:
    st.subheader("Toronto Public Library Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="No. of Branches", value=num_libraries)
        st.metric(label="Oldest Branch", value=oldest_info)
        st.metric(label="Avg. Branch Sq. Footage", value=avg_sq_ft) 
    with col2:
        st.metric(label="Youth Hubs Branches", value=youth_hub)
        st.metric(label="Teen Council Branches", value=teen_council)
        st.metric(label="Leading Reading Branches", value=leading_reading )
    with col3:
        st.metric(label="Avg. Branch Workstations", value=int(avg_ws))
        st.metric(label="Kid Stop Branches", value=kidstop)
        st.metric(label="Adult Literacy Branches", value=adult_literacy)

with bottom_container:
    st.subheader("Toronto Public Library Insights")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Size Map', "Rankings", "Size vs Performance", "Correlations", "Trends"])
    with tab1:
        map_clean = df_map_data.dropna(subset=['Lat', 'Long']).copy()
        map_clean['SquareFootage'] = pd.to_numeric(map_clean['SquareFootage'], errors='coerce')
        map_clean.dropna(subset=['SquareFootage'], inplace=True)
        fig_heatmap = px.scatter_map(
                map_clean, lat="Lat", lon="Long", size="SquareFootage", color="SquareFootage",
                hover_name="BranchName", hover_data={"Address": True, "SquareFootage": ':,.0f'},
                labels={"SquareFootage": "Sq. Ft"}, color_continuous_scale=px.colors.sequential.Plasma,
                zoom=10, center={"lat": 43.7, "lon": -79.4}, map_style="carto-positron"
            )
        fig_heatmap.update_layout(template='plotly_white', height=400,title_text="Square Footage Heatmap", title_x=0.5)
        st.plotly_chart(fig_heatmap, width='stretch')
        
        with tab2: st.plotly_chart(fig_rankings, width='stretch')
        with tab3: st.plotly_chart(fig_bubble, width='stretch')
        with tab4: st.plotly_chart(fig_correlation)
        with tab5: 
            col_a, col_b = st.columns(2)
            for i, m in enumerate(METRIC_MAP):
                annual = m['df'].groupby('Year')[m['id']].sum().reset_index()
                fig_t = px.line(annual, x='Year', y=m['id'], title=f'{m["label"]} Trend',hover_data={m['id']: ':.0f'})
                fig_t.update_layout(template='plotly_white', height=400, title_x=0.5)
                if i % 2 == 0: col_a.plotly_chart(fig_t)
                else: col_b.plotly_chart(fig_t)

