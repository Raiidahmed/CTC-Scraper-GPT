import pandas as pd
import openai
import time
from bs4 import BeautifulSoup

# Your OpenAI API key
openai.api_key = ""

# Load the first CSV file
data1 = pd.read_csv('climate_tech_eventbrite_climate.csv')

# Load the second CSV file
data2 = pd.read_csv('Events-Grid view.csv')

# Save the header of the second CSV file in a variable
header2 = data2.columns.tolist()

# Add the two new columns to the header of the output CSV file
header_output = header2 + ['WorkedByGPT', 'Description']

# Define the model
#model = "gpt-4"

# Number of rows to test from the first CSV file
# Set to 'MAX' to process all rows
num_rows_to_test = 50

# If num_rows_to_test is 'MAX', process all rows
# Otherwise, process only the specified number of rows
if num_rows_to_test == 'MAX':
    num_rows_to_test = len(data1)

# Define the mapping between the columns of the first and second CSV files, and the cleaning operation for each column
# The format is: 'column1': ('column2', 'cleaning_operation')

column_mapping = {
    'Event-href': [('Event URL', 'Output as is')],
    'Title': [('Event Name', 'Clean up and format nicely and remove commas'), ('Relevance', 'If the event is relevant to climate tech, respond True')],
    'Date and Time': [('Start', 'Copy ONLY start date and time in form of Month Day HH:MM AM/PM or add a space if there is no data'), ('End', 'Copy ONLY end date and time in form of Month Day HH:MM AM/PM or add a space if there is no data')],
    'Location': [('Location', 'Remove commas and clean up'), ('City', 'Output city name (NYC if its a borough of nyc')],
    'Organizer_link-href': [('Organizer', 'Output as is')]
}

# Open a new text file in write mode
with open('output.tsv', 'w') as f:
    # Write the header from the second CSV file to the text file
    f.write('\t'.join(header2) + '\tWorkedByGPT\tDescription\n')

    # Iterate over the DataFrame rows of the first CSV file
    for i, row in data1.iterrows():
        # If we have processed the specified number of rows, break the loop
        if i >= num_rows_to_test:
            break

        # Convert the row to a dictionary and remove unnecessary characters
        row_dict = row.to_dict()

        # Create a list of messages for the API call
        messages = []

        # Iterate over the column mapping
        for column1, column2_cleaning_ops in column_mapping.items():
            for mapping in column2_cleaning_ops:
                column2, cleaning_operation = mapping
                # Add a message for each column to the list of messages
                messages.append({"role": "user", "content": f"Clean up the data using the following op"
                                                            f"eration: {cleaning_operation}. The data is: "
                                                            f"{row_dict[column1]}"})

        # Define the system message for the API call
        system_message = {"role": "system", "content": "ONLY OUTPUT THE RESULTS OF ALL THE OPERATIONS IN THE ORDER PRESENTED SEPARATED BY TABS."}

        # Add the system message to the beginning of the list of messages
        messages.insert(0, system_message)

        print(messages)

        while True:
            try:
                # Make the API call
                response = openai.ChatCompletion.create(
                    model='gpt-4',
                    messages=messages
                )
                # If the API call is successful, break the loop
                break
            except openai.error.OpenAIError:
                # If an OpenAI API error is encountered, pause for 30 seconds and then retry
                print("OpenAI API error encountered. Waiting for 30 seconds...")
                time.sleep(30)

        # Extract the model's message from the response
        model_message = response['choices'][0]['message']['content']

        # Define the system message for the API call
        system_message = {"role": "system", "content": "YOU ARE OUTPUTTING STANDARDIZED DATA. ONLY OUTPUT THE UNFORMATTED RESULTS OF THE OPERATION."}

        # Create a user message with the data and the cleaning operations
        user_message = {"role": "user",
                        "content": f"The data is: {row_dict['Description']}. The operation is to clean up the text as well as possible WITHOUT SUMMARIZING OR CHANGING THE MEANING! Delete all text up to and including the word eTicket. Present the text as one big block, without using indents, new lines, or paragraphs. End the text with a single period."}

        # Create a list of messages for the API call
        description_messages = [system_message, user_message]

        print(description_messages)

        # Try making the API call for the 'Description' column
        while True:
            try:
                # Make the API call
                description_response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=description_messages
                )
                # If the API call is successful, break the loop
                break
            except openai.error.OpenAIError:
                # If an OpenAI API error is encountered, pause for 30 seconds and then retry
                print("OpenAI API error encountered. Waiting for 30 seconds...")
                time.sleep(30)

        # Extract the model's message from the response
        description_model_message = description_response['choices'][0]['message']['content']

        # Define the system message for the API call
        system_message = {"role": "system",
                          "content": "YOU ARE OUTPUTTING STANDARDIZED DATA. ONLY OUTPUT THE UNFORMATTED RESULTS OF THE OPERATION."}

        # Create a user message with the data and the cleaning operations
        user_message = {"role": "user",
                        "content": f"The data is: {row_dict['Description']}. If the description is for an event relevant to climate tech, output True"}

        ''''# Create a list of messages for the API call
        curation_messages = [system_message, user_message]

        print(curation_messages)

        # Try making the API call for the 'Description' column
        while True:
            try:
                # Make the API call
                curation_response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=curation_messages
                )
                # If the API call is successful, break the loop
                break
            except openai.error.OpenAIError:
                # If an OpenAI API error is encountered, pause for 30 seconds and then retry
                print("OpenAI API error encountered. Waiting for 30 seconds...")
                time.sleep(30)

        # Extract the model's message from the response
        curation_model_message = curation_response['choices'][0]['message']['content']
'''
        # Write the model's message as a new line in the text file
        f.write(model_message + "\ttrue" + "\t" + description_model_message + '\n') #+ "\t" + curation_model_message + '\n')

        print(model_message)
        print(description_model_message)
        #print(curation_model_message)

