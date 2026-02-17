from utils import *
from data import *

st.title(APP_NAME)
st.header(BRANCH_INTELLIGENCE_HEADER)



branch_option = st.sidebar.selectbox("Branches",branch_list)
branch_df = physical[(physical['BranchName'] == branch_option)].reset_index()
top_container = st.container()
middle_container = st.container()

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
        st.write("Square Footage")
        st.write("No of workstations")
        st.write("Public Parking Available")
        st.write("Service Tier")
    with col2:
        st.write("Adult literacy Program Avilable")
        st.write("Computer learning centre Avilable")
        st.write("Digital Innovation Hub Avilable")
        st.write("Youth Hub Avilable")