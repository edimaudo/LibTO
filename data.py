from utils import *

# Load data
@st.cache_data
def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    #for col in ['GIFT_DATE', 'CRM_INTERACTION_DATE', 'SENT_DATE']:
    #    if col in data.columns:
    #        data[col] = pd.to_datetime(data[col])
    return data

path = "data/"
branch_info = load_data(path + "tpl-branch-general-information-2023.csv")
visits = load_data(path + "tpl-visits-annual-by-branch.csv")
registration = load_data(path + "tpl-card-registrations-annual-by-branch.csv")
circulation = load_data(path + "tpl-circulation-annual-by-branch.csv")
workstation = load_data(path + "tpl-workstation-usage-annual-by-branch.csv")
space_rental = load_data(path + "tpl-branch-space-rentals-2024.csv")
neighborhood = load_data(path + "Neighbourhoods.csv")


# physical branches        
physical = branch_info[branch_info['PhysicalBranch'] != 0]
physical['SquareFootage'] = pd.to_numeric(physical['SquareFootage'].astype(str).str.replace(',', ''), errors='coerce')      
physical['Workstations'] = pd.to_numeric(physical['Workstations'], errors='coerce')
physical['KidsStop'] = pd.to_numeric(physical['KidsStop'], errors='coerce')
physical['LeadingReading'] = pd.to_numeric(physical['LeadingReading'], errors='coerce')
physical['TeenCouncil'] = pd.to_numeric(physical['TeenCouncil'], errors='coerce')
physical['YouthHub'] = pd.to_numeric(physical['YouthHub'], errors='coerce')
physical['AdultLiteracyProgram'] = pd.to_numeric(physical['AdultLiteracyProgram'], errors='coerce')
physical['PresentSiteYear'] = pd.to_numeric(physical['PresentSiteYear'], errors='coerce')
oldest = physical.sort_values('PresentSiteYear').iloc[0]

branch_list = physical['BranchName'].unique()
branch_list = branch_list.astype('str')
branch_list.sort()

