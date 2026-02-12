import pandas as pd
import os

class DataProcessor:
    def __init__(self):
        # Use absolute paths to avoid issues during deployment
        base_path = os.path.join(os.path.dirname(__file__), 'data')
        
        self.branch_info = pd.read_csv(os.path.join(base_path, 'tpl-branch-general-information-2023.csv'))
        self.visits = pd.read_csv(os.path.join(base_path, 'tpl-visits-annual-by-branch.csv'))
        self.space_rental = pd.read_csv(os.path.join(base_path, 'tpl-branch-space-rentals-2024.csv'))
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
