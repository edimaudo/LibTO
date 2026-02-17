from utils import *
from data import *

st.title(APP_NAME)
st.header(BRANCH_INTELLIGENCE_HEADER)

branch_option = st.sidebar.selectbox("Branches",branch_list)
branch_df = physical[(physical['BranchName'] == branch_option)].reset_index()

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
    option = st.selectbox("Options",("Trends", "Forecasts", "Branch Agent"),)
    branch_code = branch_df['BranchCode'][0]

    if option == "Trends":
        if len(branch_code) > 0:
            col1, col2 = st.columns(2)
            
            branch_registrations = registration[registration['BranchCode'] == branch_code]            
            fig_registrations_branch = create_branch_bar_chart(
                branch_registrations,
                x_col='Year',
                y_col='Registrations',
                title=f'Annual Card Registrations for {branch_option}',
                y_label='Total Card Registrations'
            )

            branch_circulation = circulation[circulation['BranchCode'] == branch_code]
            fig_circulation_branch = create_branch_bar_chart(
                branch_circulation,
                x_col='Year',
                y_col='Circulation',
                title=f'Annual Circulation for {branch_option}',
                y_label='Total Circulations'
            )

            branch_visits = visits[visits['BranchCode'] == branch_code]
            fig_visits_branch = create_branch_bar_chart(
                branch_visits,
                x_col='Year',
                y_col='Visits',
                title=f'Annual Visits for {branch_option}',
                y_label='Total Visits'
            )

            branch_workstation_usage = workstation[workstation['BranchCode'] == branch_code]
            fig_workstation_usage_branch = create_branch_bar_chart(
                branch_workstation_usage,
                x_col='Year',
                y_col='Sessions',
                title=f'Annual Workstation Usage for {branch_option}',
                y_label='Total Sessions'
            )

            with col1:
                st.plotly_chart(fig_registrations_branch)
                st.plotly_chart(fig_circulation_branch)
            with col2:
                st.plotly_chart(fig_visits_branch)
                st.plotly_chart(fig_workstation_usage_branch)
        else:
            print(f"Branch '{branch_df['BranchName'][0]}' not found.")
    elif option == "Forecast":
        col1, col2 = st.columns(2)
        with col1:
            pass
        with col2:
            pass
    else:
        pass

    