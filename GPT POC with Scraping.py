import pandas as pd
import openai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import time

input_csv = "climate_tech_eventbrite_climate_amsterdam.csv"

# Your OpenAI API key
openai.api_key = ""

num_urls = 'MAX'

Column_Mapping = {
    'Event Name': 'The name of the event',
    'Short Description': 'a short but informative description of the event',
    'Start': 'the start datetime of the event in the following format: YYYY-MM-DD HH:MM',
    'End': 'the end datetime of the event in the following format: YYYY-MM-DD HH:MM',
    'Location': 'The full address of the event',
    'City': 'the city the event takes place in',
    'Relevance': 'A TRUE or FALSE value linked to whether the event is relevant to climate tech or not'
}

def read_urls_from_csv(file_path, num_rows):
    df = pd.read_csv(file_path)
    if num_rows == 'MAX':
        num_rows = len(df.iloc[:, 1])
    urls = df.iloc[range(num_rows), 0].tolist()
    additional_data = df.iloc[range(num_rows), 1:]
    return urls, additional_data

def strip_url_parameters(url):
    parsed_url = urlparse(url)
    cleaned_url = urlunparse(parsed_url._replace(query=None))
    return cleaned_url

def extract_body_text(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    body = soup.body
    if body:
        return body.get_text(separator="\n", strip=True)
    return ""

def extract_event_details(url_content, url, fields):
    prompt_fields = [f"{value}" for key, value in fields.items()]
    prompt_fields = ",".join(prompt_fields)

    prompt = f"""
    Extract the following information from the event webpage content:
    {prompt_fields},
    Use the semicolon character ; to delimit each of the fields.
    The content of the webpage is:

    ---\n{url_content}\n---"""

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an event data extractor. All date times should be for year 2023 and should not include timezone. Use a semicolon character ; to delimit different fields extracted. Do not provide field names, just the extracted field.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            break
        except openai.error.OpenAIError:
            print("OpenAI API error encountered. Waiting for 30 seconds...")
            time.sleep(30)

    details = response.choices[0]["message"]["content"]
    stripped_url = strip_url_parameters(url)

    return details

def write_events_to_csv(events, additional_data, file_path, Fields):
    df_output = pd.DataFrame(events)
    n_cols = df_output.shape[1]
    base_cols = list(Fields.keys()) + ['Event URL']
    n_base_cols = len(base_cols)
    if n_cols > n_base_cols:
        extra_cols = [f'Extra{c + 1}' for c in range(n_cols - n_base_cols)]
        df_output.columns = base_cols + extra_cols
    else:
        df_output.columns = base_cols
    df_output = pd.concat([df_output, additional_data.reset_index(drop=True)], axis=1)
    df_output.to_csv(file_path, index=False)

urls, additional_data = read_urls_from_csv(input_csv, num_urls)
event_info = []

for url in urls:
    print(f"Getting {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    url_content = response.text
    print("Parsing...")
    body_text = extract_body_text(url_content)
    print("Sending to GPT...")
    details = extract_event_details(body_text, url, Column_Mapping)

    event_details = details.split(';')
    event_details = [s.replace(';', '\t') for s in event_details]
    event_details.append(strip_url_parameters(url))
    print(event_details)
    event_info.append(event_details)

write_events_to_csv(event_info, additional_data, "events.csv", Column_Mapping)
