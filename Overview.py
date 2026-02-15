from utils import *
from data import *

st.title(APP_NAME)
st.header(OVERVIEW_HEADER)

## Data setup
df = branch_info
physical = df[df['PhysicalBranch'] != 0]
physical['SquareFootage'] = pd.to_numeric(physical['SquareFootage'].astype(str).str.replace(',', ''), errors='coerce')      
physical['Workstations'] = pd.to_numeric(physical['Workstations'], errors='coerce')
physical['KidsStop'] = pd.to_numeric(physical['KidsStop'], errors='coerce')
physical['LeadingReading'] = pd.to_numeric(physical['LeadingReading'], errors='coerce')
physical['TeenCouncil'] = pd.to_numeric(physical['TeenCouncil'], errors='coerce')
physical['YouthHub'] = pd.to_numeric(physical['YouthHub'], errors='coerce')
physical['AdultLiteracyProgram'] = pd.to_numeric(physical['AdultLiteracyProgram'], errors='coerce')
physical['PresentSiteYear'] = pd.to_numeric(physical['PresentSiteYear'], errors='coerce')
oldest = physical.sort_values('PresentSiteYear').iloc[0]

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
    st.subheader("TPL Branch Overview")
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
    st.subheader("TPL Trends")
    tab1, tab2 = st.tabs(["Trends",'Size Heatmap'])
    with tab1:
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

    with tab2:
        pass