import pandas as pd

# Read the input data from a CSV file
input_csv = 'climate_tech_eventbrite copy.csv'
data = pd.read_csv(input_csv, header=None, names=['Date and Time'])

# Split the date and time strings at the hyphen character into two columns
data[['Start Time', 'End Time']] = data['Date and Time'].str.split(' - ', expand=True)

# Write the output to a new CSV file
output_csv = 'output_data.csv'
data.to_csv(output_csv, index=False)

