Fields = {
    'Event Name': 'The name of the event',
    'Short Description': 'a short but informative description of the event',
    'Start': 'the start datetime of the event in the following format: YYYY-MM-DD HH:MM',
    'End': 'the end datetime of the event in the following format: YYYY-MM-DD HH:MM',
    'Location': 'The full address of the event',
    'City': 'the city the event takes place in'
}

url_content = "URL content goes here."

# List comprehension to convert the Fields dictionary into a list of formatted strings
prompt_fields = [f"{value}" for key, value in Fields.items()]

# Join the formatted strings together using the semicolon delimiter
prompt_fields = ",\n".join(prompt_fields)

prompt = f"""
Extract the following information from the event webpage content:
{prompt_fields},
and the amount of tokens used for the input prompt.
Use the semicolon character ; to delimit each of the fields.
The content of the webpage is:

---\n{url_content}\n---"""

print(prompt)