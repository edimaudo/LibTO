import pandas as pd
import os
import json
import plotly.express as px
import plotly.utils

class DataProcessor:
    def __init__(self):
        base_path = os.path.join(os.path.dirname(__file__), 'data')
        
        self.branch_info = pd.read_csv(os.path.join(base_path, 'tpl-branch-general-information-2023.csv'))
        self.branch_visits = pd.read_csv(os.path.join(base_path, 'tpl-visits-annual-by-branch.csv'))
        self.branch_space_rental = pd.read_csv(os.path.join(base_path, 'tpl-branch-space-rentals-2024.csv'))
        self.branch_registration = pd.read_csv(os.path.join(base_path, 'tpl-card-registrations-annual-by-branch.csv'))
        self.branch_circulation = pd.read_csv(os.path.join(base_path, 'tpl-circulation-annual-by-branch.csv'))
        self.branch_workstation = pd.read_csv(os.path.join(base_path, 'tpl-workstation-usage-annual-by-branch.csv'))
        self.neighbourhoods = pd.read_csv(os.path.join(base_path, 'Neighbourhoods.csv'))

        
    def get_branch_list(self):
        # Returns alphabetical list of branches for the dropdown
        return sorted(self.branch_info['BranchName'].unique().tolist())

    def get_branch_data(self, branch_name):
        # Filters all dataframes for a specific branch
        branch_details = self.branch_info[self.branch_info['BranchName'] == branch_name].to_dict('records')[0]
        return branch_details

    def get_overview_kpis(self):
            df = self.branch_info
            physical = df[df['PhysicalBranch'] != 0].copy()

            physical['SquareFootage'] = pd.to_numeric(
                    physical['SquareFootage'].astype(str).str.replace(',', ''), 
                    errors='coerce'
                )
            
            physical['Workstations'] = pd.to_numeric(
                    physical['Workstations'], 
                    errors='coerce'
                )
        
            # Calculate KPIs
            num_libraries = len(physical)
            avg_sq_ft = physical['SquareFootage'].mean()
            avg_ws = physical['Workstations'].mean()

            physical['PresentSiteYear'] = pd.to_numeric(physical['PresentSiteYear'], errors='coerce')
            oldest = physical.sort_values('PresentSiteYear').iloc[0]
            oldest_info = f"{oldest['BranchName']} ({int(oldest['PresentSiteYear'])})"
    
            return {
                "count": num_libraries,
                "avg_sq_ft": f"{avg_sq_ft:,.0f}",
                "avg_ws": round(avg_ws, 0),
                "oldest": oldest_info
            }

    def get_trend_charts(self):
        # Load trend datasets
        df_reg = self.branch_registration
        df_circ = self.branch_circulation
        df_visits = self.branch_visits
        df_ws = self.branch_workstation

        # Grouping logic from your .ipynb
        charts = {}
        data_map = {
            "reg": (df_reg, "Registrations", "Annual Registrations"),
            "circ": (df_circ, "Circulation", "Annual Circulation"),
            "visits": (df_visits, "Visits", "Annual Visits"),
            "ws": (df_ws, "Sessions", "Workstation Usage")
        }

        for key, (df, col, title) in data_map.items():
            trend = df.groupby('Year')[col].sum().reset_index()
            fig = px.bar(trend, x='Year', y=col, title=title, color_discrete_sequence=['#007FA3'])
            fig.update_layout(template="plotly_white", title_font_size=20,title_x=0.5,height=500, margin=dict(l=20, r=20, t=40, b=20))
            charts[key] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return charts

    def get_heatmap(self):
        df = self.branch_info
        geo_df = df[df['PhysicalBranch'] != 0].copy()
        
        fig = px.density_mapbox(
            geo_df, lat='Lat', lon='Long', z='SquareFootage', 
            radius=15, zoom=10, 
            center=dict(lat=43.7, lon=-79.35),
            mapbox_style="carto-positron",
            title="Toronto Library Square Footage Heatmap"
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
