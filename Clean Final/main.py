import pandas as pd
from datetime import datetime
import re
import dateparser as dp
import openai

#openai.api_key =

def remove_duplicates_and_non_alphanumeric(text):
    words = re.findall(r'\b\w+\b', text)
    unique_words = list(dict.fromkeys(words))
    cleaned_text = ' '.join(unique_words)
    return cleaned_text

def append_am_pm(row):
    if 'am' in str(row[4]) and all([x not in str(row[3]) for x in ['am', 'pm']]):
        row[3] += 'am'
    elif 'pm' in str(row[4]) and all([x not in str(row[3]) for x in ['am', 'pm']]):
        row[3] += 'pm'
    return row

def contains_date(s):
    # Replace the "¬∑" symbol with a comma
    s = s.replace("¬∑", ",")

    # Remove any non-alphanumeric characters (except comma, space, and hyphen) from the string
    s = re.sub(r"[^\w\s,-]", "", s)

    # Define patterns for date detection
    patterns = [
        r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(?:Nov|Dec)(?:ember)?)\b',
        r'\b\d{1,2},?\s(?:\d{4})?\b',
        r'\b(?:\d{4})\b'
    ]

    # Combine patterns into a single regular expression
    date_pattern = re.compile("|".join(patterns))

    # Search for a date in the input string
    if date_pattern.search(s):
        return True
    else:
        return False

def parse_date(row):
    try:
        # Parse the input string into a datetime object
        flag = contains_date(str(row[4]))

        row[3] = str(dp.parse(str(row[3])))
        row[4] = str(dp.parse(str(row[4])))

        if not flag:
            row[4] = row[3][0:10] + row[4][10:]

        row[4] = row[4].rsplit('-', 1)[0].strip()

        dt3 = datetime.strptime(str(row[3]), "%Y-%m-%d %H:%M:%S")
        dt4 = datetime.strptime(str(row[4]), "%Y-%m-%d %H:%M:%S")

        #Reformat the datetime object into the desired format
        row[3] = dt3.strftime("%B %d, %Y, %I:%M %p").replace(" 0", " ")
        row[4] = dt4.strftime("%B %d, %Y, %I:%M %p").replace(" 0", " ")

        return row

    except ValueError:
        print(f"Invalid input format: '{row[0]}'. Skipping this value.")
        return row

# Set your CSV filenames here
input_csv = 'climate_tech_eventbrite.csv'
column_labels_csv = 'Events-Grid view.csv'

# Specify the column indices to drop from the input CSV
columns_to_drop = [0, 1, 2, 8]  # Change these indices as needed

# Specify the new column indices and corresponding labels indices from the column_labels CSV
new_columns = {1: 1, 4: 3, 7: 7, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19}  # Add/modify key-value pairs as needed; keys are the new column indices, values are the label indices

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

# Split the 'Start' column values at the hyphen and put the resulting strings into the 'Start' and 'End' columns
start_end = df.iloc[:, 3].apply(lambda x: (x.split(' - ')[0], x.split(' - ')[1]) if isinstance(x, str) and ' - ' in x else (x, ''))

df.iloc[:, 3] = [start for start, _ in start_end]
df.iloc[:, 4] = [end for _, end in start_end]

df.iloc[:, 5] = df.iloc[:, 5].apply(lambda x: remove_duplicates_and_non_alphanumeric(x) if isinstance(x, str) else x)

#remove garbage text from description
for i in range(len(df.iloc[:, 6])):
    index = df.iloc[i, 6].find("eTicket")
    if index != -1:
        df.iloc[i, 6] = df.iloc[i, 6][index + len("eTicket"):]
    print(df.iloc[i, 6])

    """response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # maybe put in an exception to go to another model in case of rate limiting?
        messages=[
            {"role": "system",
             "content": "You are cleaning the description from eventbrite data sourced from a web scraper. DO NOT SUMMARIZE THE TEXT! You must preserve as much of the original language as possible, just remove any unreadable artifacts, unrelated artifacts, or noise in this text."},
            {"role": "system", "content": f"Here is the description: {df.iloc[i, 6]}"},
        ],
    )

    df.iloc[i,6] = cleaned_text = response['choices'][0]['message']['content']
    """

    print(df.iloc[i,6])



#Add AM and PM labels to the start time if they are not present
df = df.apply(append_am_pm, axis=1)

#Parse the dates
df = df.apply(parse_date, axis=1)

#Parse addresses
#df = df.apply(parse_address, axis=1)

# Save the modified dataframe to output.csv
df.to_csv('output - NO AI.csv', index=False)