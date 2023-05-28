import openai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, parse_qs, urljoin
import re
import csv

# Replace 'your_api_key' with your actual API key
openai.api_key = ""


# Initialize the OpenAI API client
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def crawl_url(url, max_pages=6):
    crawled_urls = set()
    to_crawl = [url]

    while to_crawl and len(crawled_urls) < max_pages:
        current_url = to_crawl.pop(0)

        if current_url in crawled_urls:
            continue

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
            }
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
        except (requests.RequestException, ValueError) as e:
            print(f"Error while crawling {current_url}: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")
            if href and not href.startswith("#"):
                parsed_href = urlparse(href)
                if not parsed_href.netloc:
                    href = urljoin(url, href)
                if is_valid_url(href) and urlparse(href).netloc == urlparse(url).netloc:
                    if href != url and href != url + "/":
                        to_crawl.append(href)

        crawled_urls.add(current_url)

    return crawled_urls


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove boilerplate elements
    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "meta",
            "head",
            "header",
            "footer",
            "aside",
            "nav",
        ]
    ):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def truncate_text(text, max_tokens=4000):
    tokens = text.split()
    truncated_tokens = tokens[:max_tokens]
    truncated_text = " ".join(truncated_tokens)
    return truncated_text


def summarize_text(text, url):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    # "content": "You are an investment analyst writing a high-level memo of this company based off of the provided information. Please provide a summary of the company and how it stands out in the market",
                    "content": "You are an NY Magazine writer describing a climate organization in NYC based off of information scraped from their website.\
                        Please provide: the name of the organization, a superlative that describes the organization in a useful and entertaining way, \
                        who might be interested in the organization, and a description of the organization.\
                        Also include a general category tag for this organization.",
                },
                {
                    "role": "user",
                    "content": f"Please write an entry for an article on cliamte tech organizations in the US \
                        based on the organization's website text:\n\n{text}\n",
                },
            ],
        )

        summary = response.choices[0].message.content
    except:
        print("Error for ", url)
        print("~~~~~~~~~~~~~~~~")
        print("Text for ", text)
        summary = ""

    with open("resources.txt", "a+") as f:
        f.write("\n~~~~~~\n")
        f.write(url)
        f.write("\n")
        f.writelines(summary)

    return summary


def process_urls(urls):
    summaries = {}

    for url in urls:
        crawled_urls = crawl_url(url)
        all_text = ""

        for crawled_url in crawled_urls:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
                }
                response = requests.get(crawled_url, headers=headers)
                response.raise_for_status()
            except (requests.RequestException, ValueError) as e:
                print(f"Error while getting {crawled_url}: {e}")
                continue

            extracted_text = extract_text(response.content)
            all_text += extracted_text + "\n"

        truncated_text = truncate_text(all_text, 2500)
        summary = summarize_text(truncated_text, url)
        print(summary)
        summaries[url] = summary
        # with open(output_filename, "a", newline="", encoding="utf-8") as csvfile:
        #     csv_writer = csv.writer(csvfile, delimiter="|")
        #     csv_writer.writerow([url, summary])
        #     print("Added ", url)


def read_urls_from_file(filename):
    with open(filename, "r") as file:
        urls = [line.strip() for line in file]
    return urls


if __name__ == "__main__":
    input_filename = "competitor_urls.txt"
    output_filename = "competitor_output.csv"

    urls = read_urls_from_file(input_filename)
    process_urls(urls)

    # Save output to a CSV file
