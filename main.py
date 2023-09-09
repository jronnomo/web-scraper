import os
import time
import dotenv
import requests
import selectorlib
from send_email import send_mail
import sqlite3

dotenv.load_dotenv()
URL = os.getenv("URL_TOURS")
# Establish connection
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def read(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    # Query data with condition
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                store(extracted)
                send_mail(extracted)
                print("Email Sent!")
        time.sleep(2)