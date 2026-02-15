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


        



