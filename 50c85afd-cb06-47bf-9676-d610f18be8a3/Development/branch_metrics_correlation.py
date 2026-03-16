import pandas as pd
import plotly.graph_objects as go

# --- Load dataframes from the dataframes dict ---
df_card_registrations = dataframes['df_card_registrations']
df_visits = dataframes['df_visits']
df_circulation = dataframes['df_circulation']
df_workstation_usage = dataframes['df_workstation_usage']

# --- BranchCodes to exclude (non-physical / special service branches) ---
BRANCHES_TO_EXCLUDE = {
    "Answerline", "Bookmobile One", "Bookmobile Two", "Departmental Staff",
    "Home Library Service", "Interloan", "Literacy Deposits", "Merril Collection",
    "Osborne Collection", "Automated Phone System", "Sunnybrook Hospital", "Virtual Library"
}

# Reverse the branch_name_map to get BranchCode -> BranchName and vice versa
name_to_code = {v: k for k, v in branch_name_map.items()}
codes_to_exclude = {name_to_code[n] for n in BRANCHES_TO_EXCLUDE if n in name_to_code}

print(f"Excluding {len(codes_to_exclude)} branch codes: {sorted(codes_to_exclude)}")

# --- Helper: filter out excluded branches and aggregate by BranchCode ---
def aggregate_metric(df, value_col):
    _df = df[~df['BranchCode'].isin(codes_to_exclude)].copy()
    return _df.groupby('BranchCode')[value_col].sum().reset_index()

agg_registrations  = aggregate_metric(df_card_registrations, 'Registrations')
agg_visits         = aggregate_metric(df_visits,              'Visits')
agg_circulation    = aggregate_metric(df_circulation,         'Circulation')
agg_workstation    = aggregate_metric(df_workstation_usage,   'Sessions')

# --- Merge all metrics on BranchCode ---
df_corr = (
    agg_registrations
    .merge(agg_visits,      on='BranchCode', how='inner')
    .merge(agg_circulation, on='BranchCode', how='inner')
    .merge(agg_workstation, on='BranchCode', how='inner')
)

# Add readable branch names
df_corr['BranchName'] = df_corr['BranchCode'].map(branch_name_map)
print(f"Branches included in correlation matrix: {len(df_corr)}")

# --- Compute Pearson correlation matrix ---
metric_cols = ['Registrations', 'Visits', 'Circulation', 'Sessions']
corr_matrix = df_corr[metric_cols].corr()

# Rename columns/index for display clarity
display_labels = {
    'Registrations':  'Card Registrations',
    'Visits':         'Visits',
    'Circulation':    'Circulation',
    'Sessions':       'Workstation Usage',
}
corr_display = corr_matrix.rename(index=display_labels, columns=display_labels)

labels = corr_display.columns.tolist()
z_vals = corr_display.values.tolist()

# Build annotation text (2 decimal places)
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
            title="Pearson r",
            thickness=18,
            tickvals=[-1, -0.5, 0, 0.5, 1],
        ),
    )
)

fig_correlation.update_layout(
    title=dict(
        text="<b>Toronto Public Library — Branch Metrics Correlation Matrix</b><br>"
             "<sup>Pearson correlation across all years (physical branches only)</sup>",
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
