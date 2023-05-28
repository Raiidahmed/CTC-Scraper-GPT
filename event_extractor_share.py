import pandas as pd
import openai
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import csv

# Your OpenAI API key
openai.api_key = ""

#input should be a list of urls followed by an organizer link selector
def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        urls = file.readlines()
    return set([url.strip() for url in urls])


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


Fields = {'Event Name': 'The name of the event',
          'Short Description': 'a short but informative description of the event',
          'Start': 'the start datetime of the event in the following format: YYYY-MM-DD HH:MM',
          'End': 'the end datetime of the event in the following format: YYYY-MM-DD HH:MM',
          'Location': 'The full address of the event',
          'City': 'the city the event takes place in'}


def extract_event_details(url_content, url):
    prompt = f"""
        Extract the following information from the event webpage content:
        the name of the event, 
        a short but informative description of the event,
        the start datetime of the event in the following format: YYYY-MM-DD HH:MM, 
        the end datetime of the event in the same format, 
        the amount of tokens used for the input prompt,
        and the location of the event.
        Use the semicolon character ; to delimit each of the fields.
        The content of the webpage is:
        \n\n---\n{url_content}\n---"""

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

    details = response.choices[0]["message"]["content"]
    stripped_url = strip_url_parameters(url)

    return details


def write_events_to_csv(events, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        headers = [
            "Event Name",
            "Description",
            "Start Datetime",
            "End Datetime",
            "Tokens",
            "Location",
            "URL",
        ]
        writer.writerow(headers)
        for event in events:
            writer.writerow(event)


urls = read_urls_from_file("climate_tech_eventbrite_climate copy 3.txt")
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
    details = extract_event_details
    details = extract_event_details(body_text, url)
    print(details)

    # Split the details string into a list
    event_details = details.split(';')

    # Replace semicolon characters within fields, if any, with a different character to avoid conflict with the delimiter
    event_details = [s.replace(';', '|') for s in event_details]

    # Append the URL to the event details
    event_details.append(strip_url_parameters(url))

    # Append to the event information list
    event_info.append(event_details)

write_events_to_csv(event_info, "events.tsv")
