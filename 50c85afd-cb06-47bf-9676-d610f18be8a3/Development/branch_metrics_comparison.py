import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# --- Data Preparation (Using your provided variables) ---
df_card_registrations = dataframes['df_card_registrations']
df_visits = dataframes['df_visits']
df_circulation = dataframes['df_circulation']
df_workstation_usage = dataframes['df_workstation_usage']

# BranchNames to exclude (non-physical / administrative branches)
_excluded_branches = [
    "Answerline", "Bookmobile One", "Bookmobile Two", "Departmental Staff",
    "Home Library Service", "Interloan", "Literacy Deposits", "Merril Collection",
    "Osborne Collection", "Automated Phone System", "Sunnybrook Hospital", "Virtual Library",
]

# --- Helper: map BranchCode -> BranchName ---
branch_name_map = df_general_info.set_index("BranchCode")["BranchName"].to_dict()
_excluded_codes = {code for code, name in branch_name_map.items() if name in _excluded_branches}

def add_branch_name(df, code_col="BranchCode"):
    df = df.copy()
    df["BranchName"] = df[code_col].map(branch_name_map).fillna(df[code_col])
    return df

def filter_branches(df, code_col="BranchCode"):
    return df[~df[code_col].isin(_excluded_codes)].copy()

# Apply filters and groupings
# 1. Card Registrations
reg_by_branch = filter_branches(df_card_registrations).groupby("BranchCode", as_index=False)["Registrations"].sum().pipe(add_branch_name).sort_values("Registrations", ascending=False)
reg_top10 = reg_by_branch.head(10).sort_values("Registrations", ascending=True) # Ascending for horizontal bar orientation
reg_bot10 = reg_by_branch.tail(10).sort_values("Registrations", ascending=True)

# 2. Circulation
circ_by_branch = filter_branches(df_circulation).groupby("BranchCode", as_index=False)["Circulation"].sum().pipe(add_branch_name).sort_values("Circulation", ascending=False)
circ_top10 = circ_by_branch.head(10).sort_values("Circulation", ascending=True)
circ_bot10 = circ_by_branch.tail(10).sort_values("Circulation", ascending=True)

# 3. Visits
visits_by_branch = filter_branches(df_visits).groupby("BranchCode", as_index=False)["Visits"].sum().pipe(add_branch_name).sort_values("Visits", ascending=False)
visits_top10 = visits_by_branch.head(10).sort_values("Visits", ascending=True)
visits_bot10 = visits_by_branch.tail(10).sort_values("Visits", ascending=True)

# 4. Workstation Usage
ws_by_branch = filter_branches(df_workstation_usage).groupby("BranchCode", as_index=False)["Sessions"].sum().pipe(add_branch_name).sort_values("Sessions", ascending=False)
ws_top10 = ws_by_branch.head(10).sort_values("Sessions", ascending=True)
ws_bot10 = ws_by_branch.tail(10).sort_values("Sessions", ascending=True)

# --- Visual Settings ---
COLOR_TOP = "#1a6fc4"
COLOR_BOT = "#e05b3a"

metrics = [
    ("Card Registrations", reg_top10, reg_bot10, "BranchName", "Registrations"),
    ("Circulation",        circ_top10, circ_bot10, "BranchName", "Circulation"),
    ("Visits",             visits_top10, visits_bot10, "BranchName", "Visits"),
    ("Workstation Usage",  ws_top10, ws_bot10, "BranchName", "Sessions"),
]

subtitle_list = []
for m in metrics:
    subtitle_list.append(f"<b>{m[0]} – Top 10</b>")
    subtitle_list.append(f"<b>{m[0]} – Bottom 10</b>")

# --- Build Subplot Grid ---
fig_branch_rankings = make_subplots(
    rows=4, cols=2,
    subplot_titles=subtitle_list,
    vertical_spacing=0.12,    # Increased to prevent row overlap
    horizontal_spacing=0.18,  # Increased to give space for branch names
)

for row_idx, (label, top_df, bot_df, name_col, val_col) in enumerate(metrics, start=1):
    # Top 10
    fig_branch_rankings.add_trace(
        go.Bar(
            x=top_df[val_col], y=top_df[name_col],
            orientation="h", marker_color=COLOR_TOP,
            showlegend=False, hovertemplate="%{y}: %{x:,.0f}<extra></extra>",
        ),
        row=row_idx, col=1
    )
    # Bottom 10
    fig_branch_rankings.add_trace(
        go.Bar(
            x=bot_df[val_col], y=bot_df[name_col],
            orientation="h", marker_color=COLOR_BOT,
            showlegend=False, hovertemplate="%{y}: %{x:,.0f}<extra></extra>",
        ),
        row=row_idx, col=2
    )

# --- Layout and Spacing Fixes ---
fig_branch_rankings.update_layout(
    title_text="Toronto Public Library – Branch Metrics",
    title_font_size=24,
    title_x=0.5,
    height=2000,              # Tall height to accommodate 4 rows comfortably
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="white",
    font=dict(family="Arial", size=11),
    # Large left margin (220) for BranchNames, top (150) for main title
    margin=dict(l=220, r=50, t=150, b=100),
)

# Move Subplot Titles up so they don't sit on the X-axis of the chart above
for i in fig_branch_rankings['layout']['annotations']:
    i['y'] = i['y'] + 0.02
    i['font'] = dict(size=14)

# Axes formatting
fig_branch_rankings.update_xaxes(showgrid=True, gridcolor="#eeeeee", zeroline=False)
fig_branch_rankings.update_yaxes(tickfont=dict(size=10))

fig_branch_rankings.show()