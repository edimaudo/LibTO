## Load Libraries
import streamlit as st
import pandas as pd
import numpy as np
import os, os.path
import warnings
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Setup
APP_NAME = 'LibTO'
OVERVIEW_HEADER = 'Library Insights'
BRANCH_INTELLIGENCE_HEADER = "Branch Intelligence"

warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

def create_branch_bar_chart(df, x_col, y_col, title, y_label):
    fig = px.bar(
        df, x=x_col, y=y_col, title=title,
        labels={y_col: y_label},
        hover_data={x_col: True, y_col: ':.0f'}
    )
    fig.update_layout(
        template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400
    )
    return fig

## Load Data
from zerve import variable
branch_info = variable("dataframe_assignments","df_general_info")
df_map_data = variable("dataframe_assignments","df_merged_geo")
df_card_registration = variable("annual_metrics_visualization","df_card_registrations")
df_circulation = variable("annual_circulation_plot","annual_circulation")
df_visits = variable("annual_visits_chart","df_visits")
df_workstation_usage = variable("workstation_usage_visualization","df_workstation_usage")

## Data setup       
physical = branch_info[branch_info['PhysicalBranch'] != 0].copy()
# Clean columns for physical base to avoid hidden spaces
physical.columns = physical.columns.str.strip()

physical['SquareFootage'] = pd.to_numeric(physical['SquareFootage'].astype(str).str.replace(',', ''), errors='coerce')      
physical['Workstations'] = pd.to_numeric(physical['Workstations'], errors='coerce')
physical['KidsStop'] = pd.to_numeric(physical['KidsStop'], errors='coerce')
physical['LeadingReading'] = pd.to_numeric(physical['LeadingReading'], errors='coerce')
physical['TeenCouncil'] = pd.to_numeric(physical['TeenCouncil'], errors='coerce')
physical['YouthHub'] = pd.to_numeric(physical['YouthHub'], errors='coerce')
physical['AdultLiteracyProgram'] = pd.to_numeric(physical['AdultLiteracyProgram'], errors='coerce')
physical['PresentSiteYear'] = pd.to_numeric(physical['PresentSiteYear'], errors='coerce')
oldest = physical.sort_values('PresentSiteYear').iloc[0]

## Branch List
branch_list = physical['BranchName'].unique().astype('str')
branch_list.sort()

## Metric data clean up & Advanced Visuals
# --- Configuration ---
BRANCHES_TO_EXCLUDE = {
    "Answerline", "Bookmobile One", "Bookmobile Two", "Departmental Staff",
    "Home Library Service", "Interloan", "Literacy Deposits", "Merril Collection",
    "Osborne Collection", "Automated Phone System", "Sunnybrook Hospital", "Virtual Library"
}

TIER_CONFIG = {
    'NL': {'label': 'Neighborhood Library (NL)', 'color': '#00CC96'},
    'DL': {'label': 'District Library (DL)', 'color': '#636EFA'},
    'RR': {'label': 'Research & Reference Library (RR)', 'color': '#EF553B'},
}

# Source references for the pipeline
METRIC_MAP = [
    {'id': 'Registrations', 'label': 'Card Registrations', 'df': df_card_registration},
    {'id': 'Visits',         'label': 'Visits',             'df': df_visits},
    {'id': 'Circulation',    'label': 'Circulation',        'df': df_circulation},
    {'id': 'Sessions',       'label': 'Workstation Usage',  'df': df_workstation_usage},
]

# --- Processing Pipeline ---
def prepare_analysis_df(physical_df, metrics):
    # Filter physical branches by name exclusion and presence of Square Footage
    df_base = physical_df[
        ~physical_df['BranchName'].isin(BRANCHES_TO_EXCLUDE) & 
        physical_df['SquareFootage'].notna()
    ].copy()
    
    # Normalize ServiceTier naming
    if 'ServiceTier' in df_base.columns:
        df_base['ServiceTier'] = df_base['ServiceTier'].replace({'RL': 'RR'})
    
    # Get set of codes to exclude
    excluded_codes = set(physical_df[physical_df['BranchName'].isin(BRANCHES_TO_EXCLUDE)]['BranchCode'])
    
    for m in metrics:
        m_df = m['df'].copy()
        # FIX: Strip whitespace from columns to prevent KeyError
        m_df.columns = m_df.columns.str.strip()
        
        # Detect Branch identifier
        code_col = next((c for c in ['BranchCode', 'Branch Code', 'Branch'] if c in m_df.columns), None)
        
        if code_col:
            m_df = m_df.rename(columns={code_col: 'BranchCode'})
            agg = (
                m_df[~m_df['BranchCode'].isin(excluded_codes)]
                .groupby('BranchCode')[m['id']]
                .sum()
                .reset_index()
            )
            df_base = df_base.merge(agg, on='BranchCode', how='inner')
            
    return df_base

# Run the pipeline
df_analysis = prepare_analysis_df(physical, METRIC_MAP)

# --- Generate Figures ---
# 1. 4-Panel Bubble Chart
fig_bubble = make_subplots(
    rows=2, cols=2, subplot_titles=[m['label'] for m in METRIC_MAP],
    horizontal_spacing=0.1, vertical_spacing=0.15
)
for i, m in enumerate(METRIC_MAP):
    if m['id'] in df_analysis.columns:
        row, col = (i // 2 + 1), (i % 2 + 1)
        vals = df_analysis[m['id']]
        b_sizes = ((vals - vals.min()) / (vals.max() - vals.min()) * 30 + 8)
        colors = df_analysis['ServiceTier'].map(lambda x: TIER_CONFIG.get(x, {}).get('color', '#AAAAAA'))
        
        fig_bubble.add_trace(go.Scatter(
            x=df_analysis['SquareFootage'], y=vals, mode='markers',
            marker=dict(size=b_sizes, color=colors, opacity=0.7, line=dict(width=0.5, color='white')),
            text=df_analysis['BranchName'],
            hovertemplate="<b>%{text}</b><br>Sqft: %{x:,.0f}<br>Value: %{y:,.0f}<extra></extra>",
            showlegend=False
        ), row=row, col=col)
fig_bubble.update_layout(height=800, template="plotly_white", title_text="Performance vs. Size by Service Tier", title_x=0.5)

# 2. Heatmap Correlations
ids_list = [m['id'] for m in METRIC_MAP if m['id'] in df_analysis.columns]
labels_list = [m['label'] for m in METRIC_MAP if m['id'] in df_analysis.columns]
if ids_list:
    corr = df_analysis[ids_list].corr()
    fig_correlation = go.Figure(data=go.Heatmap(
        z=corr.values, x=labels_list, y=labels_list, colorscale="RdBu", zmin=-1, zmax=1,
        text=corr.values.round(2), texttemplate="%{text}"
    ))
    fig_correlation.update_layout(title="Metric Correlation Matrix", height=500, width=500, template="plotly_white", title_x=0.5)

# 3. Performance Rankings
fig_rankings = make_subplots(rows=4, cols=2, horizontal_spacing=0.2, vertical_spacing=0.08,
                            subplot_titles=[f"Top/Bottom 10: {m['label']}" for m in METRIC_MAP for _ in (1,2)])
for i, m in enumerate(METRIC_MAP):
    if m['id'] in df_analysis.columns:
        sorted_df = df_analysis.sort_values(m['id'], ascending=False)
        top, bot = sorted_df.head(10).iloc[::-1], sorted_df.tail(10)
        fig_rankings.add_trace(go.Bar(x=top[m['id']], y=top['BranchName'], orientation='h', marker_color='#1a6fc4', showlegend=False), row=i+1, col=1)
        fig_rankings.add_trace(go.Bar(x=bot[m['id']], y=bot['BranchName'], orientation='h', marker_color='#e05b3a', showlegend=False), row=i+1, col=2)
fig_rankings.update_layout(height=1200, title_text="Branch Metrics Ranking", template="plotly_white", margin=dict(l=200))

# --- Streamlit UI ---
st.title(APP_NAME)
st.write("LibTO is a civic intelligence app designed for Toronto denizens to get operational insights into the Toronto Public Library (TPL)")

choice_selection = st.radio("Select View", ('Overview', 'Branch Intelligence'))

if choice_selection == 'Overview':
    st.header(OVERVIEW_HEADER)
    
    # KPIs
    num_libraries = len(physical)
    avg_sq_ft = f"{physical['SquareFootage'].mean():,.0f}"
    oldest_info = f"{oldest['BranchName']}"
    avg_ws = f"{physical['Workstations'].mean():.0f}"
    kidstop = f"{physical['KidsStop'].sum():.0f}"
    leading_reading = f"{physical['LeadingReading'].sum():.0f}"
    teen_council = f"{physical['TeenCouncil'].sum():.0f}"
    youth_hub = f"{physical['YouthHub'].sum():.0f}"
    adult_literacy = f"{physical['AdultLiteracyProgram'].sum():.0f}"
    
    top_container = st.container()
    with top_container:
        st.subheader("Toronto Public Library Overview")
        col1, col2, col3 = st.columns(3)
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
    
    with st.container():
        st.subheader("Toronto Public Library Insights")
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['Size Map', "Rankings", "Size vs Performance", "Correlations", "Trends"])
        
        with tab1:
            st.write("Square footage Heatmap")
            map_clean = df_map_data.dropna(subset=['Lat', 'Long']).copy()
            map_clean['SquareFootage'] = pd.to_numeric(map_clean['SquareFootage'], errors='coerce')
            map_clean.dropna(subset=['SquareFootage'], inplace=True)
            fig_heatmap = px.scatter_map(
                map_clean, lat="Lat", lon="Long", size="SquareFootage", color="SquareFootage",
                hover_name="BranchName", hover_data={"Address": True, "SquareFootage": ':,.0f'},
                labels={"SquareFootage": "Sq. Ft"}, color_continuous_scale=px.colors.sequential.Plasma,
                zoom=10, center={"lat": 43.7, "lon": -79.4}, map_style="carto-positron"
            )
            fig_heatmap.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab2: st.plotly_chart(fig_rankings, use_container_width=True)
        with tab3: st.plotly_chart(fig_bubble, use_container_width=True)
        with tab4: st.plotly_chart(fig_correlation)
        with tab5: 
            st.write("Highlights yearly Trends")
            col_a, col_b = st.columns(2)
            for i, m in enumerate(METRIC_MAP):
                annual = m['df'].groupby('Year')[m['id']].sum().reset_index()
                fig_t = px.line(annual, x='Year', y=m['id'], title=f'{m["label"]} Trend')
                fig_t.update_layout(template='plotly_white', height=400)
                if i % 2 == 0: col_a.plotly_chart(fig_t)
                else: col_b.plotly_chart(fig_t)

elif choice_selection == 'Branch Intelligence':
    st.header(BRANCH_INTELLIGENCE_HEADER)
    branch_option = st.sidebar.selectbox("Branches", branch_list)
    branch_df = physical[physical['BranchName'] == branch_option].reset_index()
    
    top_container = st.container()
    middle_container = st.container()
    bottom_container = st.container()
    
    with top_container:
        st.subheader("TPL Branch Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Branch Name : {str(branch_df['BranchName'][0])}")
            st.write(f"Branch Code : {branch_df['BranchCode'][0]}")
            st.write(f"Address : {branch_df['Address'][0]}")
            st.write(f"Postal Code : {branch_df['PostalCode'][0]}")
        with col2:
            st.write(f"Telephone : {branch_df['Telephone'][0]}")
            st.write(f"Website : {branch_df['Website'][0]}")
            st.write(f"Ward Name : {branch_df['WardName'][0]}")
            st.write(f"Site Year : {str(int(branch_df['PresentSiteYear'][0]))}")  
            
    with middle_container:
        st.subheader("Branch Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Square Footage : {str(branch_df['SquareFootage'][0])}")
            st.write(f"No of workstations : {str(int(branch_df['Workstations'][0]))}")
            st.write(f"Public Parking Available : {str(branch_df['PublicParking'][0])}")
            st.write(f"KidStop Program Available : {'Yes' if branch_df['KidsStop'][0] == 1 else 'No'}")
            st.write(f"Teen Council Program Available : {'Yes' if branch_df['TeenCouncil'][0] == 1 else 'No'}")
        with col2:
            st.write(f"Adult literacy Program Available : {'Yes' if branch_df['AdultLiteracyProgram'][0] == 1 else 'No'}")
            st.write(f"Computer learning centre Available : {'Yes' if branch_df['CLC'][0] == 1 else 'No'}")
            st.write(f"Digital Innovation Hub Available : {'Yes' if branch_df['DIH'][0] == 1 else 'No'}")
            st.write(f"Youth Hub Available : {'Yes' if branch_df['YouthHub'][0] == 1 else 'No'}")
            st.write(f"Leading Reading Available : {'Yes' if branch_df['LeadingReading'][0] == 1 else 'No'}")
            
    with bottom_container:
        st.subheader("Branch Trends")
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
        
        col1, col2 = st.columns(2)
        with col1:
            if not branch_registrations.empty:
                st.plotly_chart(create_branch_bar_chart(branch_registrations, 'Year', 'Registrations', f'Annual Card Registrations for {branch_option}', 'Total Card Registrations'))
            if not branch_circulation.empty:
                st.plotly_chart(create_branch_bar_chart(branch_circulation, 'Year', 'Circulation', f'Annual Circulation for {branch_option}', 'Total Circulations'))
        with col2:
            if not branch_visits.empty:
                st.plotly_chart(create_branch_bar_chart(branch_visits, 'Year', 'Visits', f'Annual Visits for {branch_option}', 'Total Visits'))
            if not branch_workstation_usage.empty:
                st.plotly_chart(create_branch_bar_chart(branch_workstation_usage, 'Year', 'Sessions', f'Annual Workstation Usage for {branch_option}', 'Total Sessions'))
