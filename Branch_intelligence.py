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
    if option == "Trends":
        pass
    elif option == "Forecast":
        pass
    else:
        pass

    