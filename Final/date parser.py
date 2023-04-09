import dateparser as dp
import pandas as pd
from datetime import datetime

def convert_datetime_format(date_str):
    try:
        # Parse the input string into a datetime object
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # Reformat the datetime object into the desired format
        formatted_dt = dt.strftime("%B %d, %Y, %I:%M %p").replace(" 0", " ")
        print(formatted_dt)
        return formatted_dt

    except ValueError:
        print(f"Invalid input format: '{date_str}'. Skipping this value.")
        return None

dates = pd.read_csv('modified_file.csv')

for x in range(len(dates)):
    print(convert_datetime_format(str(dp.parse(str(dates.iloc[x,0])))))


