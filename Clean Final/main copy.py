import pandas as pd
from datetime import datetime
import re
import dateparser as dp
import usaddress
from dateutil import parser as dp
from usaddress import RepeatedLabelError
import openai

# openai.api_key =

def parse_address(row):
    try:
        addr = usaddress.tag(row[5])
        print(row[5])
        try:
            addr[0]
            values = list(addr[0].values())
            value_str = ', '.join(map(str, values))
            print(value_str)
        except KeyError:
            print('error')
    except RepeatedLabelError as e:
        print(f"Unable to parse address: {row[5]}")
        # Handle the error, for example, by logging it or returning a default value
        # ...

    return row


def parse_date(row):
    # Append am/pm
    if 'am' in str(row[4]) and all([x not in str(row[3]) for x in ['am', 'pm']]):
        row[3] += 'am'
    elif 'pm' in str(row[4]) and all([x not in str(row[3]) for x in ['am', 'pm']]):
        row[3] += 'pm'

    # Check for date
    s = str(row[4]).replace("¬∑", ",")
    s = re.sub(r"[^\w\s,-]", "", s)
    patterns = [
        r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep('
        r'?:tember)?|Oct(?:ober)?|(?:Nov|Dec)(?:ember)?)\b',
        r'\b\d{1,2},?\s(?:\d{4})?\b',
        r'\b(?:\d{4})\b'
    ]
    date_pattern = re.compile("|".join(patterns))
    flag = bool(date_pattern.search(s))

    # Parse date
    try:
        row[3] = str(dp.parse(str(row[3])))
        row[4] = str(dp.parse(str(row[4])))
        if not flag:
            row[4] = row[3][0:10] + row[4][10:]
        row[4] = row[4].rsplit('-', 1)[0].strip()

        dt3 = datetime.strptime(str(row[3]), "%Y-%m-%d %H:%M:%S")
        dt4 = datetime.strptime(str(row[4]), "%Y-%m-%d %H:%M:%S")

        row[3] = dt3.strftime("%B %d, %Y, %I:%M %p").replace(" 0", " ")
        row[4] = dt4.strftime("%B %d, %Y, %I:%M %p").replace(" 0", " ")

    except ValueError:
        print(f"Invalid input format: '{row[0]}'. Skipping this value.")

    return row


def parse_desc(row):
    count = row[6].find("eTicket")
    if count != -1:
        row[6] = row[6][count + len("eTicket"):]


# Set your CSV filenames here
input_csv = 'climate_tech_eventbrite.csv'
column_labels_csv = 'Events-Grid view.csv'

# Specify the column indices to drop from the input CSV
columns_to_drop = [0, 1, 2, 8]  # Change these indices as needed

# Specify the new column indices and corresponding labels indices from the column_labels CSV
new_columns = {1: 1, 4: 3, 7: 7, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18,
               19: 19}  # Add/modify key-value pairs as needed; keys are the new column indices, values are the label
# indices

# Read the input CSV
df = pd.read_csv(input_csv)

# Drop the specified columns
df.drop(columns=df.columns[columns_to_drop], inplace=True)

# Read the column labels CSV
column_labels_df = pd.read_csv(column_labels_csv)

# Insert the blank columns at specified indices using column labels from the second CSV
for index, label_index in new_columns.items():
    label = column_labels_df.columns[label_index]
    df.insert(index, label, '')

# Find the minimum length of the two DataFrames
min_len = min(len(df.columns), len(column_labels_df.columns))

# Create a new list of column names, combining the columns of the two DataFrames up to the minimum length
new_column_names = list(df.columns[:min_len])
new_column_names[:min_len] = list(column_labels_df.columns[:min_len])

# Assign the new list of column names to the first DataFrame
df.columns = new_column_names

# remove garbage text from description
df = df.apply(parse_desc, axis=1)

# Add AM and PM labels to the start time if they are not present
df = df.apply(parse_date, axis=1)

# Parse the dates
df = df.apply(parse_date, axis=1)

# Parse addresses
df = df.apply(parse_address, axis=1)

# Save the modified dataframe to output.csv
df.to_csv('output - NO AI.csv', index=False)
