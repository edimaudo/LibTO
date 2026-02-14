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

## Metrics
# df = self.branch_info
#             physical = df[df['PhysicalBranch'] != 0].copy()

#             physical['SquareFootage'] = pd.to_numeric(
#                     physical['SquareFootage'].astype(str).str.replace(',', ''), 
#                     errors='coerce'
#                 )
            
#             physical['Workstations'] = pd.to_numeric(
#                     physical['Workstations'], 
#                     errors='coerce'
#                 )
        
#             # Calculate KPIs
#             num_libraries = len(physical)
#             avg_sq_ft = physical['SquareFootage'].mean()
#             avg_ws = physical['Workstations'].mean()

#             physical['PresentSiteYear'] = pd.to_numeric(physical['PresentSiteYear'], errors='coerce')
#             oldest = physical.sort_values('PresentSiteYear').iloc[0]
#             oldest_info = f"{oldest['BranchName']} ({int(oldest['PresentSiteYear'])})"
    
#             return {
#                 "count": num_libraries,
#                 "avg_sq_ft": f"{avg_sq_ft:,.0f}",
#                 "avg_ws": int(avg_ws),
#                 "oldest": oldest_info

# Graphs
# charts = {}
#             data_map = {
#                 "reg": (self.branch_registration, "Registrations", "Annual Registrations"),
#                 "circ": (self.branch_circulation, "Circulation", "Annual Circulation"),
#                 "visits": (self.branch_visits, "Visits", "Annual Visits"),
#                 "ws": (self.branch_workstation, "Sessions", "Workstation Usage")
#             }
    
#             for key, (df, col, title) in data_map.items():
#                 trend = df.groupby('Year')[col].sum().reset_index()
#                 fig = px.bar(trend, x='Year', y=col, title=title, color_discrete_sequence=['#007FA3'])
#                 fig.update_layout(template="plotly_white", title_x=0.5, height=450)

# df = self.branch_info
#         geo_df = df[df['PhysicalBranch'] != 0].copy()
        
#         fig = px.density_mapbox(
#             geo_df, lat='Lat', lon='Long', z='SquareFootage', 
#             radius=15, zoom=10, 
#             center=dict(lat=43.7, lon=-79.35),
#             mapbox_style="carto-positron",
#             title="Toronto Library Square Footage Heatmap"
#         )
#         fig.update_layout(title_font_size=20,title_x=0.5,height=500,margin=dict(l=0, r=0, t=40, b=0))
