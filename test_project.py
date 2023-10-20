import unittest
import pandas as pd
import os
from datetime import datetime
import logging
import shutil 

# Import the filter_and_save_data function here
def filter_and_save_data(input_dir, output_base_dir):
    try:
        # Get the current year
        current_year = datetime.now().year

        # Loop through each year and process the data
        for year in range(current_year, current_year - 4, -1):
            year_output_dir = os.path.join(output_base_dir, str(year))
            if not os.path.exists(year_output_dir):
                os.makedirs(year_output_dir)

            # Initialize an empty list to store the filtered DataFrames for the year
            combined_dfs = []

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

            # Concatenate the filtered DataFrames into a single DataFrame for the year
            combined_df = pd.concat(combined_dfs)

            # Save the filtered combined data to a single CSV file in the corresponding year-specific directory
            output_file = os.path.join(year_output_dir, f"{year}_filtered_data.csv")
            combined_df.to_csv(output_file, index=False)

            logging.info(f"Saved filtered data for year {year} to {output_file}")

    except Exception as e:
        logging.error(f"Error processing data: {e}")


# Define a test class for the filter_and_save_data function
class TestFilterAndSaveData(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_input_dir = 'test_input_dir'
        self.test_output_dir = 'test_output_dir'
        os.makedirs(self.test_input_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)

    

    def create_test_data(self, year):
        # Create test data for a specific year
        data = {
            'StatusFromDate': ['20210101', '20220115', '20200320', '20191210'],
            'State': ['NSW', 'VIC', 'ACT', 'QLD']
        }
        test_df = pd.DataFrame(data)
        test_df.to_csv(os.path.join(self.test_input_dir, f'test_data_{year}.csv'), index=False)

    def test_filter_and_save_data(self):
        # Create test data for each of the last 3 years
        current_year = datetime.now().year
        for year in range(current_year, current_year - 2, -1):
            self.create_test_data(year)

        # Call the function with test input and output directories
        filter_and_save_data(self.test_input_dir, self.test_output_dir)
        
        # Check if the output files were created for each year
        for year in range(current_year, current_year - 2, -1):
            output_file_path = os.path.join(self.test_output_dir, str(year), f"{year}_filtered_data.csv")
            self.assertTrue(os.path.isfile(output_file_path))

            # # Check if the output file contains the expected data
            # expected_output = pd.read_csv(output_file_path)
            # self.assertEqual(len(expected_output), 2)  # Check the number of rows in the output


    def tearDown(self):
    # Remove the temporary directory and its contents after testing
        shutil.rmtree(self.test_input_dir)  # Use shutil.rmtree to remove a non-empty directory
        shutil.rmtree(self.test_output_dir)
        


if __name__ == '__main__':
    unittest.main()

