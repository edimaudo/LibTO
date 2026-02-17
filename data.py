from utils import *

# Load data
@st.cache_data
def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    #for col in ['GIFT_DATE', 'CRM_INTERACTION_DATE', 'SENT_DATE']:
    #    if col in data.columns:
    #        data[col] = pd.to_datetime(data[col])
    return data

# Datasets
path = "data/"
branch_info = load_data(path + "tpl-branch-general-information-2023.csv")
visits = load_data(path + "tpl-visits-annual-by-branch.csv")
registration = load_data(path + "tpl-card-registrations-annual-by-branch.csv")
circulation = load_data(path + "tpl-circulation-annual-by-branch.csv")
workstation = load_data(path + "tpl-workstation-usage-annual-by-branch.csv")
space_rental = load_data(path + "tpl-branch-space-rentals-2024.csv")
neighborhood = load_data(path + "Neighbourhoods.csv")

# Physical branches        
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