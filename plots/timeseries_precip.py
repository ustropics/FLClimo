import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

        # Filter out rows where the date is invalid
        valid_data = []
        for _, row in data.iterrows():
            try:
                year = int(row['YEAR'])
                month = int(row['MONTH'])
                day = int(row['DAY'])
                date = pd.Timestamp(year=year, month=month, day=day)
                valid_data.append(row)
            except (ValueError, TypeError):
                pass

        # Convert the valid data to a dataframe
        data = pd.DataFrame(valid_data)

        # Convert the 'DATE' column to datetime type
        data['DATE'] = pd.to_datetime(data[['YEAR', 'MONTH', 'DAY']])

        # Drop the original year, month, and day columns
        data = data.drop(['YEAR', 'MONTH', 'DAY'], axis=1)

        # Convert 'PRECIPITATION' column to numeric dtype
        data['PRECIPITATION'] = pd.to_numeric(data['PRECIPITATION'], errors='coerce')

        # Replace values outside the range of -50 to 150 with NaN
        data.loc[~data['PRECIPITATION'].between(-50, 150), 'PRECIPITATION'] = np.nan

        # Remove any rows that contain NaN values
        data = data.dropna()

        # Set a threshold for the number of non-missing values in each year
        min_days_per_year = 300

        # Filter the data to include only years with enough non-missing values
        year_counts = data.groupby(data['DATE'].dt.year)['PRECIPITATION'].count()
        valid_years = year_counts[year_counts >= min_days_per_year].index
        valid_data = data[data['DATE'].dt.year.isin(valid_years)]

        # Convert the 'PRECIPITATION' column to numeric type, replacing non-numeric values with NaN
        valid_data['PRECIPITATION'] = pd.to_numeric(valid_data['PRECIPITATION'], errors='coerce')

        # Remove any rows that contain NaN values
        valid_data = valid_data.dropna()

        # Remove any mean values that are below -40 mm
        valid_data = valid_data[valid_data['PRECIPITATION'] >= -40]

        # Define the function for the trend line
        def trend(x, y):
            if len(x) > 0:
                return np.polyval(np.polyfit(x, y, 1), x)
            else:
                return np.zeros_like(x)

        # Set an empty trend line and the periods used
        trend_lines = []
        periods = [(1880, 1910),(1910, 1940), (1940, 1970), (1970, 2000), (2000,2022)]

        for period in periods:
            # Extract the data for the current period
            period_data = valid_data[valid_data['DATE'].dt.year.between(period[0], period[1])]

            if not period_data['DATE'].dt.year.empty and not period_data['PRECIPITATION'].empty:
                z = np.polyfit(period_data['DATE'].dt.year, period_data['PRECIPITATION'], deg=1)

                # Create a dictionary with the necessary information for the trend line
                trend_dict = {'period': f'{period[0]}-{period[1]}',
                            'slope': z[0],
                            'intercept': z[1]}

                # Append the trend dictionary to the list of trend lines for the current station
                trend_lines.append(trend_dict)

            # Create a plot of the precipitation data and the trend line for the current period
            fig, ax = plt.subplots(figsize=(16,9))
            ax.plot(period_data['DATE'], period_data['PRECIPITATION'], label='PRECIPITATION')
            ax.plot(period_data['DATE'], trend(period_data['DATE'].dt.year, period_data['PRECIPITATION']), label='Trend')
            ax.set_title(f'Mean Precipitation by year - {station_name} ({station_id}) ({period[0]}-{period[1]})')
            ax.set_xlabel('Year')
            ax.set_ylabel('Precipitation (mm)')
            ax.legend()

            # Set the x-ticks to show each year
            years = np.arange(period[0], period[1]+1)
            ax.set_xticks(pd.date_range(f"{period[0]}", f"{period[1]}", freq="AS"))
            ax.set_xticklabels(years, rotation=45)

            # Save the plot to a PNG file
            plot_filename = f'../static/img/plots/timeseries/precip_daily/{station_id}_{period[0]}-{period[1]}.png'
            plt.savefig(plot_filename)
            plt.close()

        # Add the trend lines to the weather_stations dictionary
        for station in weather_stations:
            if station['station_id'] == int(station_id):
                station['precip_trend_lines'] = trend_lines
                break

        # Save the weather_stations dictionary to the JSON file
        with open(json_file, 'w') as f:
            json.dump(weather_stations, f, indent=4)
