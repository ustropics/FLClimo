import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# Set the directory where the CSV files are located
directory = '../data/weather_stations/'
json_file = '../static/json/weather_stations.json' 

# Load the data from the JSON file
with open(json_file) as f:
    weather_stations = json.load(f)

# Loop over all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read the CSV data file into a Pandas dataframe
        data = pd.read_csv(os.path.join(directory, filename))

        # Get the file name without extension and match the station_id with the corresponding station name
        station_id = os.path.splitext(os.path.basename(filename))[0]
        station_name = None
        for station in weather_stations:
            if station['station_id'] == int(station_id):
                station_name = station['station_name']
                break

        # Remove any leading or trailing spaces in column names
        data.columns = data.columns.str.strip()

        # Convert the 'YEAR' column to integer type
        data['YEAR'] = data['YEAR'].astype(int)

        # Convert 'MEAN TEMP' column to numeric dtype
        data['MEAN TEMP'] = pd.to_numeric(data['MEAN TEMP'], errors='coerce')

        # Replace values outside the range of -50 to 150 with NaN
        data.loc[~data['MEAN TEMP'].between(-50, 150), 'MEAN TEMP'] = np.nan

        # Remove any rows that contain NaN values
        data = data.dropna()

        # Set a threshold for the number of non-missing values in each year
        min_days_per_year = 300

        # Filter the data to include only years with enough non-missing values
        year_counts = data.groupby('YEAR')['MEAN TEMP'].count()
        valid_years = year_counts[year_counts >= min_days_per_year].index
        valid_data = data[data['YEAR'].isin(valid_years)]

        # Convert the 'MEAN TEMP' column to numeric type, replacing non-numeric values with NaN
        valid_data['MEAN TEMP'] = pd.to_numeric(valid_data['MEAN TEMP'], errors='coerce')

        # Remove any rows that contain NaN values
        valid_data = valid_data.dropna()

        # Remove any mean values that are below 50F
        valid_data = valid_data[valid_data['MEAN TEMP'] >= -40]

        # Calculate the mean temperature for each year
        mean_temps = valid_data.groupby('YEAR')['MEAN TEMP'].mean()

        # Calculate the trend line
        z = np.polyfit(mean_temps.index, mean_temps.values, 1)
        p = np.poly1d(z)

        # Get the slope coefficient of the trend line
        slope = 0
        slope = z[0]
        # print(slope)

        for station in weather_stations:
            if station['station_name'] == station_name:
                station['trend_meantemp_yearly'] = slope*100
                break

        plt.figure(figsize=(16,9))
        plt.plot(mean_temps.index, mean_temps.values, 'o')
        plt.plot(mean_temps.index, p(mean_temps.index), 'r--')
        plt.title('Minimum Temperature by Year - ' + station_name + ' (' + station_id + ')')
        plt.xlabel('Year')
        plt.ylabel('Mean Temperature (°F)')

        # Save the plot as an image
        plt.savefig('../static/img/plots/trends/meantemp_yearly/'+station_id+'_mean_trend_yearly.png', dpi=300, bbox_inches='tight')

        # Close the plot to free up memory
        plt.close()
# Write updated data to JSON file
with open(json_file, 'w') as f:
    json.dump(weather_stations, f, indent=4)