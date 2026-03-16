## TPL Map Square footage Visualizations
import pandas as pd
import plotly.express as px

df_map_data = dataframes['df_merged_geo'].copy()

# 1. Handle missing geographical data (Lat and Long)
df_map_data.dropna(subset=['Lat', 'Long'], inplace=True)

# 2. Convert 'SquareFootage' column to numeric, coercing errors to NaN
df_map_data['SquareFootage'] = pd.to_numeric(df_map_data['SquareFootage'], errors='coerce')

# 3. Drop rows with NaN values in 'SquareFootage' after conversion
df_map_data.dropna(subset=['SquareFootage'], inplace=True)

# Print info and head of the cleaned DataFrame for verification
print("--- Cleaned DataFrame for mapping: df_map_data ---")
print("\ndf_map_data.head():")
print(df_map_data.head())

print("\ndf_map_data.info():")
df_map_data.info()

# Add the cleaned DataFrame to the dataframes dictionary
dataframes['df_map_data'] = df_map_data

# Get the cleaned DataFrame
df_map_data = dataframes['df_map_data']

# Create an interactive map centered around Toronto
# The centroid of Toronto is approximately 43.7, -79.4
fig = px.scatter_mapbox(
    df_map_data,
    lat="Lat",
    lon="Long",
    size="SquareFootage", # Size of markers based on SquareFootage for heatmap effect
    color="SquareFootage", # Color markers based on SquareFootage
    hover_name="BranchName",
    hover_data={
        "Address": True,
        "SquareFootage": ':.0f',
        "Lat": False,
        "Long": False # Hide Lat/Long from hover data
    },
    color_continuous_scale=px.colors.sequential.Plasma, # Choose a color scale
    zoom=9, # Adjust zoom level to show Toronto area
    center={"lat": 43.7, "lon": -79.4},
    mapbox_style="carto-positron", # Use a clear map style
    title="Toronto Library Branches by Square Footage"
)

fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
fig.show()