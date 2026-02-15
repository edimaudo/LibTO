from utils import *
from data import *

st.title(APP_NAME)
st.header(OVERVIEW_HEADER)

# Calculate KPIs
num_libraries = len(physical)
avg_sq_ft = f"{physical['SquareFootage'].mean():,.0f}"
oldest_info = f"{oldest['BranchName']}" #({int(oldest['PresentSiteYear'])}
avg_ws = f"{physical['Workstations'].mean():.0f}"
kidstop = f"{physical['KidsStop'].sum():.0f}"
leading_reading = f"{physical['LeadingReading'].sum():.0f}"
teen_council = f"{physical['TeenCouncil'].sum():.0f}"
youth_hub = f"{physical['YouthHub'].sum():.0f}"
adult_literacy = f"{physical['AdultLiteracyProgram'].sum():.0f}"


top_container = st.container()
bottom_container = st.container()
with top_container:
    st.subheader("TPL Branch Information")
    col1, col2,col3 = st.columns(3)
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
    st.subheader("TPL Size & Trends")
    tab1, tab2 = st.tabs(['Size Heatmap',"Trends"])
    with tab1:
        df_merged_geo = pd.merge(
            physical,
            neighborhood,
            left_on='NBHDNo',
            right_on='AREA_ID',
            how='left'
        )

        df_map_data = df_merged_geo
        df_map_data.dropna(subset=['Lat', 'Long'], inplace=True)

        # UPDATED: Use scatter_map
        fig_heatmap = px.scatter_map(
            df_map_data,
            lat="Lat",
            lon="Long",
            size="SquareFootage",
            color="SquareFootage",
            hover_name="BranchName",
            hover_data={
                "Address": True,
                "SquareFootage": ':,.0f',
                "Lat": False,
                "Long": False
            },
            labels={"SquareFootage": "Sq. Ft"},
            color_continuous_scale=px.colors.sequential.Plasma,
            zoom=10,
            center={"lat": 43.7, "lon": -79.4},
            # UPDATED: map_style instead of mapbox_style
            map_style="carto-positron", 
            title="TPL Branches by Square Footage"
        )

        # UPDATED: margin and title layout remains the same
        fig_heatmap.update_layout(
            title_font_size=18,
            title_x=0.4,
            template='plotly_white',
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        st.plotly_chart(fig_heatmap)

    with tab2:
        # 1. Card Registrations
        df_card_registrations = registration
        annual_registrations = df_card_registrations.groupby('Year')['Registrations'].sum().reset_index()
        fig_registrations = px.line(
            annual_registrations,
            x='Year',
            y='Registrations',
            title='Card Registrations Trend',
            labels={'Registrations': 'Total Registrations'}
        )
        fig_registrations.update_layout(
            title_font_size=18,
            title_x=0.5,
            template='plotly_white',
            height=400
        )
        

        # 2. Circulation
        df_circulation = circulation
        annual_circulation = df_circulation.groupby('Year')['Circulation'].sum().reset_index()
        fig_circulation = px.line(
            annual_circulation,
            x='Year',
            y='Circulation',
            title='Circulation Trend',
            labels={'Circulation': 'Total Circulation'}
        )
        fig_circulation.update_layout(
            title_font_size=18,
            title_x=0.5,
            template='plotly_white',
            height=400
        )
        

        # 3. Visits
        df_visits = visits
        annual_visits = df_visits.groupby('Year')['Visits'].sum().reset_index()
        fig_visits = px.line(
            annual_visits,
            x='Year',
            y='Visits',
            title='Visits Trend',
            labels={'Visits': 'Total Visits'}
        )
        fig_visits.update_layout(
            title_font_size=18,
            title_x=0.5,
            template='plotly_white',
            height=400
        )
        

        # 4. Workstation Usage
        df_workstation_usage = workstation
        annual_workstation_usage = df_workstation_usage.groupby('Year')['Sessions'].sum().reset_index()
        fig_workstation_usage = px.line(
            annual_workstation_usage,
            x='Year',
            y='Sessions',
            title='Workstation Usage Trend',
            labels={'Sessions': 'Total Sessions'}
        )
        fig_workstation_usage.update_layout(
            title_font_size=18,
            title_x=0.5,
            template='plotly_white',
            height=400
        )
        #
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_registrations)
            st.plotly_chart(fig_circulation)
        with col2:
            st.plotly_chart(fig_visits)
            st.plotly_chart( fig_workstation_usage)

    