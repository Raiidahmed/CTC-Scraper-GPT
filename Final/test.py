import re
from dateutil.parser import parse


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


# Test the function with sample strings
strings = [
    "9pm EDT",
    "12:15pm EDT",
    "September 21, 5:30pm EDT",
    "April 28, 4pm EDT",
    "Thu, 27 Apr 2023 13:30 EDT"
]

for s in strings:
    print(f"{s}: {contains_date(s)}")