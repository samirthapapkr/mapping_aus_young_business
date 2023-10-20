import os
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='filtering_log_single.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to filter data and save to a single CSV file for all years
def filter_and_save_data(input_dir, output_base_dir):
    try:
        # Get the current year
        current_year = datetime.now().year

        # Initialize an empty list to store the filtered DataFrames for all years
        combined_dfs = []

        # Loop through each year and process the data
        for year in range(current_year, current_year - 4, -1):
            # Loop through each CSV file in the input directory
            for root, _, files in os.walk(input_dir):
                for file in files:
                    if file.endswith('.csv'):
                        file_path = os.path.join(root, file)

                        # Read the data into a pandas DataFrame
                        df = pd.read_csv(file_path, encoding="ISO-8859-1")

                        # Convert the 'StatusFromDate' column to a pandas datetime object
                        df['StatusFromDate'] = pd.to_datetime(df['StatusFromDate'], format='%Y%m%d')

                        # Filter data for the current year and Australian states
                        df_filtered = df[(df['StatusFromDate'].dt.year == year) &
                                         (df['State'].isin(['ACT', 'NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT']))]

                        # Append the filtered DataFrame to the list
                        combined_dfs.append(df_filtered)

        # Concatenate the filtered DataFrames into a single DataFrame for all years
        combined_df = pd.concat(combined_dfs)

        # Filter data less than 3 years from the current date
        cutoff_date = datetime.now() - pd.DateOffset(years=3)
        combined_df = combined_df[combined_df['StatusFromDate'] > cutoff_date]

        # Save the filtered combined data to a single CSV file
        output_file = os.path.join(output_base_dir, 'combined_filtered_data.csv')
        combined_df.to_csv(output_file, index=False)

        logging.info(f"Saved filtered data for all years to {output_file}")

    except Exception as e:
        logging.error(f"Error processing data: {e}")

# Define the input and output directories
input_dir = 'CSVData'
output_base_dir = 'FilteredSingleData'

# Call the function to filter and save data for all years
filter_and_save_data(input_dir, output_base_dir)

