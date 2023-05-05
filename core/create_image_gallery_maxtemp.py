import json

with open('../static/json/weather_stations.json') as f:
    stations = json.load(f)


html_lines = []
for station in stations:
    html_lines.append('<div class="column"><img src="website/static/img/plots/trends/meantemp_yearly/{}_mean_trend_yearly.png" class="image-preview" onclick="myFunction(this);"></div>'.format(station['station_id']))

with open('output.html', 'w') as f:
    f.write('\n'.join(html_lines))