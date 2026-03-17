import pandas as pd
import plotly.graph_objects as go

# --- Load dataframes directly from the dataframes dict (avoid upstream variable conflicts) ---
_df_card_registrations = dataframes['df_card_registrations']
_df_visits             = dataframes['df_visits']
_df_circulation        = dataframes['df_circulation']
_df_workstation_usage  = dataframes['df_workstation_usage']

# --- Build branch_name_map locally from df_general_info ---
_branch_name_map = df_general_info.set_index('BranchCode')['BranchName'].to_dict()

# --- BranchCodes to exclude (non-physical / special service branches) ---
_BRANCHES_TO_EXCLUDE = {
    "Answerline", "Bookmobile One", "Bookmobile Two", "Departmental Staff",
    "Home Library Service", "Interloan", "Literacy Deposits", "Merril Collection",
    "Osborne Collection", "Automated Phone System", "Sunnybrook Hospital", "Virtual Library"
}

_name_to_code    = {v: k for k, v in _branch_name_map.items()}
_codes_to_exclude = {_name_to_code[n] for n in _BRANCHES_TO_EXCLUDE if n in _name_to_code}

print(f"Excluding {len(_codes_to_exclude)} branch codes: {sorted(_codes_to_exclude)}")

# --- Helper: filter out excluded branches and aggregate by BranchCode ---
def _aggregate_metric(df, value_col):
    _df = df[~df['BranchCode'].isin(_codes_to_exclude)].copy()
    return _df.groupby('BranchCode')[value_col].sum().reset_index()

_agg_registrations = _aggregate_metric(_df_card_registrations, 'Registrations')
_agg_visits        = _aggregate_metric(_df_visits,              'Visits')
_agg_circulation   = _aggregate_metric(_df_circulation,         'Circulation')
_agg_workstation   = _aggregate_metric(_df_workstation_usage,   'Sessions')

# --- Merge all metrics on BranchCode ---
df_corr = (
    _agg_registrations
    .merge(_agg_visits,       on='BranchCode', how='inner')
    .merge(_agg_circulation,  on='BranchCode', how='inner')
    .merge(_agg_workstation,  on='BranchCode', how='inner')
)

# Add readable branch names
df_corr['BranchName'] = df_corr['BranchCode'].map(_branch_name_map)
print(f"Branches included in correlation matrix: {len(df_corr)}")

# --- Compute Pearson correlation matrix ---
metric_cols  = ['Registrations', 'Visits', 'Circulation', 'Sessions']
corr_matrix  = df_corr[metric_cols].corr()

# Rename columns/index for display clarity
display_labels = {
    'Registrations': 'Card Registrations',
    'Visits':        'Visits',
    'Circulation':   'Circulation',
    'Sessions':      'Workstation Usage',
}
corr_display = corr_matrix.rename(index=display_labels, columns=display_labels)

labels    = corr_display.columns.tolist()
z_vals    = corr_display.values.tolist()
text_vals = [[f"{v:.2f}" for v in row] for row in z_vals]

# --- Plotly heatmap ---
fig_correlation = go.Figure(
    data=go.Heatmap(
        z=z_vals,
        x=labels,
        y=labels,
        text=text_vals,
        texttemplate="%{text}",
        textfont={"size": 16, "color": "white"},
        colorscale="RdBu",
        zmin=-1,
        zmax=1,
        reversescale=False,
        colorbar=dict(
            title="Pearson Correlation",
            thickness=18,
            tickvals=[-1, -0.5, 0, 0.5, 1],
        ),
    )
)

fig_correlation.update_layout(
    title=dict(
        text="<b>Toronto Public Library — Branch Metrics Correlation</b><br>",
        x=0.5,
        xanchor="center",
        font=dict(size=18),
    ),
    xaxis=dict(title="", tickfont=dict(size=13), side="bottom"),
    yaxis=dict(title="", tickfont=dict(size=13), autorange="reversed"),
    width=650,
    height=600,
    margin=dict(l=160, r=60, t=120, b=120),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

fig_correlation.show()
print("\nCorrelation matrix values:")
print(corr_display.round(3).to_string())
