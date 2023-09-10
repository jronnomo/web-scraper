import os
import time
import dotenv
import requests
import selectorlib
import datetime
import streamlit as st
import plotly.express as px
import sqlite3

dotenv.load_dotenv()
URL = os.getenv("URL_TEMP")
connection = sqlite3.connect(database='temp-db.db')
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract_temp.yaml')
    value = extractor.extract(source)["temperatures"]
    return value


def read():

    # Establish connection
    cursor = connection.cursor()

    # Today date excluding time:
    today = date.split(' ')[0]

    # Read current state of database
    cursor.execute('SELECT * FROM temps WHERE dates=?', (date,))
    current_date_row = cursor.fetchall()
    cursor.execute('SELECT * FROM temps')
    all_rows = cursor.fetchall()

    return current_date_row, all_rows


def store(data):
    # Establish connection
    cursor = connection.cursor()

    # Create row value
    new_row = (date, data)

    # Store new value in database
    cursor.execute("INSERT INTO temps VALUES(?,?)", new_row)
    connection.commit()


st.title("Temperature Scraper")
scraped = scrape(URL)
extracted = extract(scraped)
current_date_row, all_rows = read()
if not current_date_row:
    store(extracted)
    print("Stored new temperature data")

dates = [row[0] for row in all_rows]
temps = [row[1] for row in all_rows]
figure = px.line(x=dates, y=temps, labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure)


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    current_date_row, all_rows = read()
    if not current_date_row:
        store(extracted)
        print("Stored new temperature data")

