import json, random

# Helper functions
def read_json():
    with open("./static/quotes.json", "r") as file:
        file_content = json.load(file)
    return file_content

# Returns quote randomly
def get_quote():
    quotes = read_json()
    random_number = random.randint(0, len(quotes) - 1)
    return quotes[random_number]

# Currency formatter
def currency_formatter(number):
    return "{:,.2f}".format(number)