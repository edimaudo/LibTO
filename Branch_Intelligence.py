from utils import *
from data import *

st.title(APP_NAME)
st.header(BRANCH_INTELLIGENCE_HEADER)

# setup data
branch_option = st.sidebar.selectbox("Branch",branch_list)
branch_df = physical[(physical['BranchName'] == branch_option)].reset_index()
print(branch_df)
df_events_with_branch_info = pd.merge(
    df_events,
    branch_df,
    left_on='LocationName',
    right_on='BranchName',
    how='inner' 
)
columns_to_filter = [
    'Title',
    'StartTime',
    'EndTime',
    'StartDateLocal',
    'LocationName',
    'Audiences',
    'Languages',
    'EventTypes'
]

df_filtered_events = df_events_with_branch_info[columns_to_filter].drop_duplicates()

df_filtered_events.rename(columns={
    'Title': 'Event title',
    'StartTime': 'Start Time',
    'EndTime': 'End Time',
    'StartDateLocal': 'Event Date',
    'LocationName': 'Location',
    'Audiences': 'Audience',
    'Languages': 'Language',
    'EventTypes': 'Event Types'
}, inplace=True)

# clean up date and time
# Convert 'Start Time' and 'End Time' to datetime objects and then format them
df_filtered_events['Start Time'] = pd.to_datetime(df_filtered_events['Start Time']).dt.strftime('%I:%M%p')
df_filtered_events['End Time'] = pd.to_datetime(df_filtered_events['End Time']).dt.strftime('%I:%M%p')

# Convert 'Event Date' to datetime objects and then format it to show only the date
df_filtered_events['Event Date'] = pd.to_datetime(df_filtered_events['Event Date']).dt.strftime('%Y-%m-%d')

# setup containers
top_container = st.container()
middle_container = st.container()
bottom_container = st.container()

with top_container:
    st.subheader("Branch Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Branch Name" + " : " + str(branch_df['BranchName'][0]))
        st.write("Branch Code"+ " : " +branch_df['BranchCode'][0])
        st.write("Address" + " : " + branch_df['Address'][0])
        st.write("Postal Code"+ " : " +branch_df['PostalCode'][0])
    with col2:
        st.write("Telephone"+ " : " +branch_df['Telephone'][0])
        st.write("Website"+ " : " +branch_df['Website'][0])
        st.write("Ward Name" + " : " + branch_df['WardName'][0])
        st.write("Site Year" + " : " + str(int(branch_df['PresentSiteYear'][0])))  

with middle_container:
    st.subheader("Branch Features")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Square Footage" + " : " + str(branch_df['SquareFootage'][0]) )
        st.write("No of workstations"+ " : " + str(int(branch_df['Workstations'][0])))
        st.write("Public Parking Available" + " : " + str(branch_df['PublicParking'][0]))
        st.write("KidStop Program Available" + " : " + str("Yes" if branch_df['KidsStop'][0] == 1 else "No"))
        st.write("Teen Council Program Available" + " : " + str("Yes" if branch_df['TeenCouncil'][0] == 1 else "No"))
    with col2:
        st.write("Adult literacy Program Avilable" + " : " + str("Yes" if branch_df['AdultLiteracyProgram'][0] == 1 else "No"))
        st.write("Computer learning centre Avilable" + " : " + str("Yes" if branch_df['CLC'][0] == 1 else "No"))
        st.write("Digital Innovation Hub Avilable" + " : " + str("Yes" if branch_df['DIH'][0] == 1 else "No"))
        st.write("Youth Hub Avilable" + " : " + str("Yes" if branch_df['YouthHub'][0] == 1 else "No"))
        st.write("Leading Reading Avilable" + " : " + str("Yes" if branch_df['LeadingReading'][0] == 1 else "No"))

with bottom_container:
    option = st.selectbox("Options",("Trends", "Forecasts","Events" ,"Branch Q&A"))
    branch_code = branch_df['BranchCode'][0]
    # Clean columns of trend dataframes for matching
    df_card_registration.columns = df_card_registration.columns.str.strip()
    df_circulation.columns = df_circulation.columns.str.strip()
    df_visits.columns = df_visits.columns.str.strip()
    df_workstation_usage.columns = df_workstation_usage.columns.str.strip()
    branch_registrations = df_card_registration[df_card_registration['BranchCode'] == branch_code] 
    branch_circulation = df_circulation[df_circulation['BranchCode'] == branch_code]
    branch_visits = df_visits[df_visits['BranchCode'] == branch_code]
    branch_workstation_usage = df_workstation_usage[df_workstation_usage['BranchCode'] == branch_code]
    if option == "Trends":
        st.subheader("Branch Trends")
        if len(branch_code) > 0:
            col1, col2 = st.columns(2)

            fig_registrations_branch = create_branch_bar_chart(
                branch_registrations,
                x_col='Year',
                y_col='Registrations',
                title=f'Annual Card Registrations for {branch_option}',
                y_label='Total Card Registrations'
            )
            fig_circulation_branch = create_branch_bar_chart(
                branch_circulation,
                x_col='Year',
                y_col='Circulation',
                title=f'Annual Circulation for {branch_option}',
                y_label='Total Circulations'
            )
            fig_visits_branch = create_branch_bar_chart(
                branch_visits,
                x_col='Year',
                y_col='Visits',
                title=f'Annual Visits for {branch_option}',
                y_label='Total Visits'
            )
            fig_workstation_usage_branch = create_branch_bar_chart(
                branch_workstation_usage,
                x_col='Year',
                y_col='Sessions',
                title=f'Annual Workstation Usage for {branch_option}',
                y_label='Total Sessions'
            )
            with col1:
                st.plotly_chart(fig_registrations_branch,width='stretch')
                st.plotly_chart(fig_circulation_branch,width='stretch')
            with col2:
                st.plotly_chart(fig_visits_branch,width='stretch')
                st.plotly_chart(fig_workstation_usage_branch,width='stretch')
        else:
            print(f"Branch '{branch_df['BranchName'][0]}' not found.")
    
    elif option == "Forecasts":
        forecast_horizon = st.sidebar.slider("Forecast Horizon (Years)",1,5)
        col1, col2 = st.columns(2)
        
        # --- Registrations ---
        reg_df = prepare_time_series(branch_registrations, 'Registrations')
        reg_forecast_index, reg_forecast_values, _ = forecast_series(reg_df['Registrations'],forecast_horizon)
        registration_forecast = plot_forecast(
        reg_df,
        'Registrations',
        reg_forecast_index,
        reg_forecast_values,
        title=f'Annual Card Registrations Forecast for {branch_option}',
        y_label='Registrations'
        )
        
        # --- Visits ---
        visits_df = prepare_time_series(branch_visits, 'Visits')
        visits_forecast_index, visits_forecast_values, _ = forecast_series(visits_df['Visits'],forecast_horizon)
        visits_forecast = plot_forecast(
        visits_df,
        'Visits',
        visits_forecast_index,
        visits_forecast_values,
        title=f'Annual Card Visits Forecast for {branch_option}',
        y_label='Visits'
        )

        # --- Circulations ---
        circ_df = prepare_time_series(branch_circulation, 'Circulation')
        circ_forecast_index, circ_forecast_values, _ = forecast_series(circ_df['Circulation'],forecast_horizon)
        circulation_forecast = plot_forecast(
        circ_df,
        'Circulation',
        circ_forecast_index,
        circ_forecast_values,
        title=f'Annual Circulation Forecast for {branch_option}',
        y_label='Circulation'
        )
        
        # --- Workstation Usage ---
        ws_df = prepare_time_series(branch_workstation_usage, 'Sessions')
        ws_forecast_index, ws_forecast_values, _ = forecast_series(ws_df['Sessions'],forecast_horizon)
        workstation_forecast = plot_forecast(
        ws_df,
        'Sessions',
        ws_forecast_index,
        ws_forecast_values,
        title=f'Annual Workstation Usage Forecast for {branch_option}',
        y_label='Sessions'
        )

        with col1:
            st.plotly_chart(registration_forecast)
            st.plotly_chart(circulation_forecast)
        with col2:
            st.plotly_chart(visits_forecast)
            st.plotly_chart(workstation_forecast)
    elif option == "Events":
        st.dataframe(df_filtered_events)
    elif option == "Branch Q&A":
        st.write("Ask a question about " + str(branch_df['BranchName'][0]))
        branch_question_txt = st.text_area(label="",value="",placeholder=None,key=1)
        branch_question_button = st.button("Get Inisghts", type="primary")
        instruction="""
                Return your entire response in professional Markdown format:
                1. Use ## for Section Headers.
                2. Use **bold** for key insights and numbers.
                3. Use Markdown tables if comparing multiple data points.
                4. If there is a clear trend, provide a 'Key Takeaway' section at the end.
            """
        if branch_question_button:
            st.html("<p> </p>")
            if branch_question_txt.strip():    
                st.subheader("Insights")
                with st.spinner("Analyzing data..."):
                    analysis = analyze_dataframe(df_master, branch_question_txt,instruction)
                    st.markdown(analysis)
            else:
                st.warning("Please enter a question in the text area above.")

    