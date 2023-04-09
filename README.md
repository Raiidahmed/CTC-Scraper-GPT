# CTC Scraper Data Cleaning Script

This is a data cleaning script for the webscraper.io output in the EventBrite sitemap for Climate Tech Cities.

This Python script processes and cleans data from event listings on Eventbrite. The script reads data from an input CSV file containing event information, cleans and parses the data, and then saves the processed data to a new output CSV file. The script is particularly useful for cleaning and formatting event data related to the climate tech industry.

## Features

- Cleans and parses event data from Eventbrite
- Removes duplicate and non-alphanumeric words from event descriptions
- Appends AM/PM information to event start times if not present
- Parses and formats event dates
- _(Optional)_ Utilizes OpenAI GPT-3.5-turbo model for cleaning event descriptions (requires API key)

## Dependencies

- pandas
- datetime
- re (regular expressions)
- dateparser
- openai (optional)

## Setup

1. Clone the repository:

`git clone https://github.com/Raiidahmed/CTC-Scraper/`

2. Install the required dependencies:

`pip install pandas datetime re dateparser openai`

3. _(Optional)_ If you would like to use the OpenAI GPT-3.5-turbo model for cleaning event descriptions, you will need to sign up for an API key at https://beta.openai.com/signup/. Then, replace the following line in the script with your API key:

`openai.api_key = "<your-api-key>"`

4. Prepare your input CSV file with the event data, and update the `input_csv` variable in the script with the filename:

`input_csv = '<your-input-csv-filename>'`

5. Update the `column_labels_csv` variable with the filename of the CSV file containing column labels:

`column_labels_csv = '<your-column-labels-csv-filename>'`

6. Adjust the `columns_to_drop` list and the `new_columns` dictionary in the script according to your specific input CSV structure, if necessary.

## Usage

1. Run the script:

`python <script-name.py>`

2. The script will process the input CSV file and save the cleaned data to a new output CSV file, named `output - NO AI.csv` by default.


