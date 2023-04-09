import pandas as pd

# Read the CSV file
df = pd.read_csv('output_data.csv', header=None)

# Define a function to append 'am' or 'pm' to the first column value
def append_am_pm(row):
    if 'am' in str(row[1]) and all([x not in row[0] for x in ['am', 'pm']]):
        row[0] += 'am'
    elif 'pm' in str(row[1]) and all([x not in row[0] for x in ['am', 'pm']]):
        row[0] += 'pm'
    return row

# Apply the function row by row
df = df.apply(append_am_pm, axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv('modified_file.csv', index=False, header=None)