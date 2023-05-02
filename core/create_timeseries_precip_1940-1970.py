import folium
import json

# define coordinates for boundary box
min_lat, max_lat = 25.0, 32.0
min_lon, max_lon = -90.0, -75.0

# Read the location data from the JSON file
with open('../static/json/weather_stations.json') as f:
    locations = json.load(f)

# Create map centered on Florida
florida_map = folium.Map(
    location=[28.0, -82.5],
    tiles="CartoDB dark_matter",
    zoom_start=7,
    min_zoom=7,
    zoom_control=False,
)

# Add markers for each location
for location in locations:
    # Find the trend data for the desired period
    period = "1940-1970"
    trend_lines = location.get("precip_trend_lines")
    trend = None
    for trend_line in trend_lines:
        if trend_line.get("period") == period:
            trend = trend_line.get("slope")
            break

    # Skip locations without the desired period
    if trend is None:
        continue

    # Set the color of the marker based on the trend value
    if trend < -2:
        color = 'red'
    elif trend >= -2 and trend <= 0:
        color = 'orange'
    elif trend >= 0 and trend <= 2:
        color = 'lightgreen'
    elif trend > 2:
        color = 'green'

    popup_html = "<b>{station_name} ({station_id})</b><br>lat: {station_lat}, lon: {station_lon}<br><a href='../../static/img/plots/timeseries/precip_daily/{station_id}_1940-1970.png' target='_BLANK'><img src='../../static/img/plots/timeseries/precip_daily/{station_id}_1940-1970.png' width='100%' height='100%'></a>".format(
        station_name=location['station_name'],
        station_id=location['station_id'],
        station_lat=location['station_lat'],
        station_lon=location['station_lon']
    )

    marker = folium.Marker(
        location=(location["station_lat"], location["station_lon"]),
        icon=folium.Icon(color=color),
        popup=folium.Popup(html=popup_html, max_width=1000, min_width=500)
    )
    marker.add_to(florida_map)

# Save map as HTML file
florida_map.save('../template/maps/map_timeseries_precip_1940-1970.html')
