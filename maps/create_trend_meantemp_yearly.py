import folium
import json

# define coordinates for boundary box
min_lat, max_lat = 25.0, 32.0
min_lon, max_lon = -90.0, -75.0

# Read the location data from the JSON file
with open('json/weather_stations.json') as f:
    locations = json.load(f)

# Create map centered on Florida
florida_map = folium.Map(
    location=[28.0, -82.5],
    tiles="CartoDB dark_matter",
    zoom_start = 7,
    min_zoom = 7,
    zoom_control= False,
)

# Add markers for each location
# Add markers for each location
for location in locations:
    popup_html = "<b>{station_name} ({station_id})</b><br>lat: {station_lat}, lon: {station_lon}<br><a href='static/img/yearly_trend/{station_id}_mean_trend_yearly.png'><img src='static/img/yearly_trend/{station_id}_mean_trend_yearly.png' width='100%' height='100%'></a>".format(
        station_name=location['station_name'],
        station_id=location['station_id'],
        station_lat=location['station_lat'],
        station_lon=location['station_lon']
    )

    marker = folium.Marker(
        location=(location["station_lat"],location["station_lon"]), 
        icon=folium.Icon(color=location["color"]),
        popup=folium.Popup(html=popup_html, max_width=1000, min_width=500)
    )
    marker.add_to(florida_map)


# Save map as HTML file
florida_map.save('florida_map.html')
