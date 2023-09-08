import os
import dotenv
import requests
import selectorlib

dotenv.load_dotenv()
URL = os.getenv("URL")
URL2 = os.getenv("URL2")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email():
    print('Email sent')


def read(text):
    with open(text) as file:
        content = file.read()
    return content


def store(text):
    with open('data.txt', 'a') as file:
        file.write(text + '\n')


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    tours = read('data.txt')
    print(extracted)
    if extracted != 'No upcoming tours':
        if extracted not in tours:
            store(extracted)
            send_email()
