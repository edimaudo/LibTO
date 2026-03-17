import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Branches to exclude ---
BRANCHES_TO_EXCLUDE = {
    "Answerline", "Bookmobile One", "Bookmobile Two", "Departmental Staff",
    "Home Library Service", "Interloan", "Literacy Deposits", "Merril Collection",
    "Osborne Collection", "Automated Phone System", "Sunnybrook Hospital", "Virtual Library"
}

# --- Service Tier definitions ---
# NL = Neighborhood Library, DL = District Library, RR = Research & Reference Library
_TIER_LABELS = {
    'NL': 'Neighborhood Library (NL)',
    'DL': 'District Library (DL)',
    'RR': 'Research & Reference Library (RR)',
}
_TIER_COLORS = {
    'NL': '#00CC96',
    'DL': '#636EFA',
    'RR': '#EF553B',
}

# --- Load source dataframes ---
_df_card_registrations = dataframes['df_card_registrations']
_df_visits = dataframes['df_visits']
_df_circulation = dataframes['df_circulation']
_df_workstation_usage = dataframes['df_workstation_usage']

# --- Parse SquareFootage from df_general_info ---
# SquareFootage is stored as a string (e.g., "29000", "28957", "shared") — coerce to numeric
_df_sq = df_general_info[['BranchCode', 'BranchName', 'SquareFootage', 'ServiceTier']].copy()
_df_sq['SquareFootage'] = pd.to_numeric(_df_sq['SquareFootage'], errors='coerce')

# Drop branches with no square footage or in the exclusion list
_df_sq = _df_sq[
    ~_df_sq['BranchName'].isin(BRANCHES_TO_EXCLUDE) &
    _df_sq['SquareFootage'].notna()
]

# Normalise tier codes: map 'RL' -> 'RR' if present for consistency
_df_sq['ServiceTier'] = _df_sq['ServiceTier'].replace({'RL': 'RR'})

print(f"Branches with valid square footage: {len(_df_sq)}")

# --- Reverse branch_name_map to get BranchName -> BranchCode ---
_name_to_code = {v: k for k, v in branch_name_map.items()}
_codes_to_exclude = {_name_to_code[n] for n in BRANCHES_TO_EXCLUDE if n in _name_to_code}

# --- Helper: filter & aggregate metric by BranchCode ---
def _aggregate(df, value_col):
    _filtered = df[~df['BranchCode'].isin(_codes_to_exclude)].copy()
    return _filtered.groupby('BranchCode')[value_col].sum().reset_index()

_agg_reg   = _aggregate(_df_card_registrations, 'Registrations')
_agg_vis   = _aggregate(_df_visits,              'Visits')
_agg_circ  = _aggregate(_df_circulation,         'Circulation')
_agg_ws    = _aggregate(_df_workstation_usage,   'Sessions')

# --- Merge all metrics with square footage ---
_df_bubble = (
    _df_sq
    .merge(_agg_reg,  on='BranchCode', how='inner')
    .merge(_agg_vis,  on='BranchCode', how='inner')
    .merge(_agg_circ, on='BranchCode', how='inner')
    .merge(_agg_ws,   on='BranchCode', how='inner')
)

print(f"Branches in bubble chart: {len(_df_bubble)}")

# --- Chart config ---
_METRICS = [
    ('Registrations', 'Card Registrations', '#636EFA'),
    ('Visits',        'Visits',             '#EF553B'),
    ('Circulation',   'Circulation',        '#00CC96'),
    ('Sessions',      'Workstation Usage',  '#AB63FA'),
]

fig_bubble = make_subplots(
    rows=2, cols=2,
    subplot_titles=[m[1] for m in _METRICS],
    horizontal_spacing=0.14,
    vertical_spacing=0.20,
)

for _idx, (_col, _label, _colour) in enumerate(_METRICS):
    _row = _idx // 2 + 1
    _col_pos = _idx % 2 + 1

    # Bubble size proportional to the metric itself (scaled for aesthetics)
    _sizes = _df_bubble[_col]
    _bubble_sizes = ((_sizes - _sizes.min()) / (_sizes.max() - _sizes.min()) * 38 + 7)

    _hover_text = (
        "<b>" + _df_bubble['BranchName'] + "</b><br>"
        + "Square Footage: " + _df_bubble['SquareFootage'].apply(lambda x: f"{x:,.0f} sq ft") + "<br>"
        + f"{_label}: " + _sizes.apply(lambda x: f"{x:,.0f}")
        + "<br>Service Tier: " + _df_bubble['ServiceTier'].map(_TIER_LABELS).fillna(_df_bubble['ServiceTier'])
    )

    # Colour by ServiceTier
    _tier_colors = _df_bubble['ServiceTier'].map(_TIER_COLORS).fillna('#AAAAAA')

    fig_bubble.add_trace(
        go.Scatter(
            x=_df_bubble['SquareFootage'],
            y=_sizes,
            mode='markers',
            marker=dict(
                size=_bubble_sizes,
                color=_tier_colors,
                opacity=0.72,
                line=dict(width=0.8, color='white'),
            ),
            text=_hover_text,
            hovertemplate="%{text}<extra></extra>",
            name=_label,
            showlegend=False,
        ),
        row=_row, col=_col_pos,
    )

    # # Trend line (linear regression)
    # _x_vals = _df_bubble['SquareFootage'].values
    # _y_vals = _sizes.values
    # _valid = ~(np.isnan(_x_vals) | np.isnan(_y_vals))
    # _m, _b = np.polyfit(_x_vals[_valid], _y_vals[_valid], 1)
    # _x_line = np.linspace(_x_vals[_valid].min(), _x_vals[_valid].max(), 200)
    # _y_line = _m * _x_line + _b

    # fig_bubble.add_trace(
    #     go.Scatter(
    #         x=_x_line,
    #         y=_y_line,
    #         mode='lines',
    #         line=dict(color='rgba(80,80,80,0.45)', dash='dash', width=1.5),
    #         hoverinfo='skip',
    #         showlegend=False,
    #     ),
    #     row=_row, col=_col_pos,
    # )

    # Axis labels
    fig_bubble.update_xaxes(
        title_text="Square Footage",
        title_font=dict(size=11),
        tickformat=",",
        gridcolor='rgba(200,200,200,0.4)',
        showgrid=True,
        row=_row, col=_col_pos,
    )
    fig_bubble.update_yaxes(
        title_text=_label,
        title_font=dict(size=11),
        tickformat=",",
        gridcolor='rgba(200,200,200,0.4)',
        showgrid=True,
        row=_row, col=_col_pos,
    )

# --- Legend: Service Tier colour guide (full labels with abbreviations) ---
for _tier_code, _tc in [('DL', _TIER_COLORS['DL']), ('NL', _TIER_COLORS['NL']), ('RR', _TIER_COLORS['RR'])]:
    fig_bubble.add_trace(
        go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color=_tc, opacity=0.8),
            name=_TIER_LABELS[_tier_code],
            showlegend=True,
        )
    )

# --- Annotation note at the bottom explaining each tier ---
_note_text = (
    "<b>Service Tier Guide:</b>  "
    "<b>NL</b> — Local hubs focusing on community needs, core collections, browsing, and public internet access.  "
    "<b>DL</b> — Larger branches with extended hours, expanded collections, and more specialized programs or services for the surrounding district.  "
    "<b>RR</b> — Libraries offering specialized, in-depth collections, research assistance, and large-scale public spaces."
)

fig_bubble.add_annotation(
    text=_note_text,
    xref="paper", yref="paper",
    x=0.5, y=-0.22,
    xanchor="center", yanchor="top",
    showarrow=False,
    font=dict(size=10.5, color="#444444"),
    align="center",
    bgcolor="rgba(245,245,245,0.9)",
    bordercolor="lightgrey",
    borderwidth=1,
    borderpad=8,
)

fig_bubble.update_layout(
    title=dict(
        text="<b>Toronto Public Library — Branch Metrics vs. Square Footage</b><br>",
        x=0.5,
        xanchor='center',
        font=dict(size=17),
    ),
    width=1200,
    height=980,  # extra height to accommodate note at bottom
    margin=dict(l=80, r=60, t=130, b=160),  # increased bottom margin for the note
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        title=dict(text="Service Tier", font=dict(size=12)),
        orientation='h',
        x=0.5,
        xanchor='center',
        y=-0.10,
        font=dict(size=12),
        bgcolor='rgba(255,255,255,0.85)',
        bordercolor='lightgrey',
        borderwidth=1,
    ),
)

fig_bubble.show()
print(f"\nBubble chart rendered with {len(_df_bubble)} branches across 4 metrics.")