from utils import *

# Load data
@st.cache_data
def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    for col in ['GIFT_DATE', 'CRM_INTERACTION_DATE', 'SENT_DATE','StartDateLocal']:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col])
    return data

# Datasets
path = "data/"
branch_info = load_data(path + "tpl-branch-general-information-2023.csv")
df_visits = load_data(path + "tpl-visits-annual-by-branch.csv")
df_card_registration = load_data(path + "tpl-card-registrations-annual-by-branch.csv")
df_circulation = load_data(path + "tpl-circulation-annual-by-branch.csv")
df_workstation_usage = load_data(path + "tpl-workstation-usage-annual-by-branch.csv")
df_space_rental = load_data(path + "tpl-branch-space-rentals-2024.csv")
df_neighborhoods = load_data(path + "Neighbourhoods.csv")
df_events = load_data(path + "tpl-events-feed.csv")

# Physical branches        
physical = branch_info[branch_info['PhysicalBranch'] != 0]
physical.columns = physical.columns.str.strip() # Clean columns for physical base to avoid hidden spaces
physical['SquareFootage'] = pd.to_numeric(physical['SquareFootage'].astype(str).str.replace(',', ''), errors='coerce')      
physical['Workstations'] = pd.to_numeric(physical['Workstations'], errors='coerce')
physical['KidsStop'] = pd.to_numeric(physical['KidsStop'], errors='coerce')
physical['LeadingReading'] = pd.to_numeric(physical['LeadingReading'], errors='coerce')
physical['TeenCouncil'] = pd.to_numeric(physical['TeenCouncil'], errors='coerce')
physical['YouthHub'] = pd.to_numeric(physical['YouthHub'], errors='coerce')
physical['AdultLiteracyProgram'] = pd.to_numeric(physical['AdultLiteracyProgram'], errors='coerce')
physical['PresentSiteYear'] = pd.to_numeric(physical['PresentSiteYear'], errors='coerce')
oldest = physical.sort_values('PresentSiteYear').iloc[0]

# Branch List
branch_list = physical['BranchName'].unique()
branch_list = branch_list.astype('str')
branch_list.sort()

COMMON_LAYOUT = dict(
    template='plotly_white',
    margin=dict(l=10, r=10, t=40, b=10),
    title_font_size=20,
    title_x=0.5,
    height=400
)

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

# Merge df_general_info and df_neighbourhoods
df_merged_geo = pd.merge(
    physical,
    df_neighborhoods,
    left_on='NBHDNo',
    right_on='AREA_ID',
    how='left'
)

df_map_data = df_merged_geo

# Create massive dataset
# --- Combine Annual Metrics ---
# Start with card registrations
df_combined = df_card_registration

# Merge circulation
df_combined = pd.merge(
    df_combined,
    df_circulation.drop(columns=['_id']), # Drop _id to avoid duplicate columns
    on=['BranchCode', 'Year'],
    how='outer' # Use outer merge to keep all years and branches
)

# Merge visits
df_combined = pd.merge(
    df_combined,
    df_visits.drop(columns=['_id']), # Drop _id to avoid duplicate columns
    on=['BranchCode', 'Year'],
    how='outer'
)

# Merge workstation usage
df_combined = pd.merge(
    df_combined,
    df_workstation_usage.drop(columns=['_id']), # Drop _id to avoid duplicate columns
    on=['BranchCode', 'Year'],
    how='outer'
)

# Fill NaN values for numerical annual metrics with 0 (assuming no activity if data is missing)
df_combined['Registrations'].fillna(0, inplace=True)
df_combined['Circulation'].fillna(0, inplace=True)
df_combined['Visits'].fillna(0, inplace=True)
df_combined['Sessions'].fillna(0, inplace=True)

# Ensure 'Year' is an integer, coercing errors for any potential NaNs after merge
df_combined['Year'] = df_combined['Year'].fillna(0).astype(int)



# --- Prepare Space Rentals  ---
# Rename 'Branch Code' to 'BranchCode' for consistency
df_space_rental.rename(columns={'Branch Code': 'BranchCode'}, inplace=True)

# Convert 'Square footage' to numeric, coercing errors to NaN
df_space_rental['Square footage'] = pd.to_numeric(df_space_rental['Square footage'], errors='coerce')
df_space_rental['MaxCapacity'] = pd.to_numeric(df_space_rental['MaxCapacity'], errors='coerce')

# Group by BranchCode and sum relevant metrics
df_space_rentals_summary = df_space_rental.groupby('BranchCode').agg(
    TotalRentalMaxCapacity=('MaxCapacity', 'sum'),
    TotalRentalSquareFootage=('Square footage', 'sum')
).reset_index()

# Fill NaN values in the summary with 0
df_space_rentals_summary.fillna(0, inplace=True)

# --- Step 4: Final Merge ---
# Merge combined annual metrics with general info
df_master = pd.merge(
    df_combined,
    physical.drop(columns=['_id']), # Drop _id from general_info to avoid duplicate column after merge
    on='BranchCode',
    how='left'
)

# Convert 'SquareFootage' in df_master to numeric, coercing errors to NaN before filling
df_master['SquareFootage'] = pd.to_numeric(df_master['SquareFootage'], errors='coerce')

# Merge with space rentals summary
df_master = pd.merge(
    df_master,
    df_space_rentals_summary,
    on='BranchCode',
    how='left'
)

# Fill any remaining NaN values in numerical columns that originated from the merges
df_master['TotalRentalMaxCapacity'].fillna(0, inplace=True)
df_master['TotalRentalSquareFootage'].fillna(0, inplace=True)

# --- Generate Figures ---
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
            hovertemplate="<b>%{text}</b><br>Sq. ft: %{x:,.0f}<br>Value: %{y:,.0f}<extra></extra>",
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
fig_rankings.update_layout(height=1200, title_text="Branch Metrics Ranking", template="plotly_white", margin=dict(l=200), title_x=0.5)

def create_branch_bar_chart(df, x_col, y_col, title, y_label):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={y_col: y_label},
        hover_data={x_col: True, y_col: ':.0f'}
    )
    
    fig.update_layout(
        template='plotly_white',
        margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20,
        title_x=0.5,
        height=400
    )
    
    return fig

def prepare_time_series(df, value_col):
    """Clean and format time series dataframe."""
    df = df.copy()
    df['Year'] = df['Year'].astype(int)
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
    df = df.dropna(subset=[value_col])
    df = df.set_index('Year')
    return df


def forecast_series(series, n_periods):
    """Fit ARIMA model and generate forecasts."""
    model = pm.auto_arima(
        series,
        seasonal=False,  # annual data → typically non-seasonal
        stepwise=True,
        suppress_warnings=True,
        error_action='ignore',
        trace=False
    )

    forecast_values, conf_int = model.predict(
        n_periods=n_periods,
        return_conf_int=True
    )

    forecast_index = pd.date_range(
        start=str(series.index.max() + 1),
        periods=n_periods,
        freq='Y'
    ).year

    return forecast_index, forecast_values, conf_int

def plot_forecast(df, value_col, forecast_index, forecast_values, title, y_label):
    """Create Plotly forecast bar chart."""
    fig = go.Figure()

    # Historical data (bars)
    fig.add_trace(go.Bar(
        x=df.index,
        y=df[value_col],
        name=f'Historical {y_label}',
        hovertemplate='<b>Year</b>: %{x}<br>'
                      f'<b>{y_label}</b>: %{{y:,.0f}}<extra></extra>'
    ))

    # Forecast data (bars)
    fig.add_trace(go.Bar(
        x=forecast_index,
        y=forecast_values,
        name=f'Forecasted {y_label}',
        hovertemplate='<b>Year</b>: %{x}<br>'
                      '<b>Forecast</b>: %{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title=f'Total {y_label}',
        barmode='group',  # places historical and forecast bars side-by-side
        template='plotly_white',
        margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20,
        title_x=0.5,
        height=400
    )

    return fig

# Gemini Model
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")
def analyze_dataframe(df, user_query, instructions="Provide a clear, concise analysis in Markdown."):
    # 1. Convert the existing DataFrame to a CSV-formatted string
    csv_data = df.to_csv(index=False)
    
    # 2. Build a structured prompt using the flexible instructions
    prompt = f"""
    You are an expert data analyst. Below is a dataset in CSV format.
    
    DATASET:
    {csv_data}
    
    USER QUERY:
    {user_query}
    
    INSTRUCTIONS:
    {instructions}
    """
    
    # 3. Get the response
    response = model.generate_content(prompt)
    return response.text