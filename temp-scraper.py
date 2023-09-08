import os
import dotenv
import requests
import selectorlib
import datetime
import streamlit as st
from glob import glob
import pandas as pd
import plotly.express as px

dotenv.load_dotenv()
URL = os.getenv("URL_TEMP")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract_temp.yaml')
    value = extractor.extract(source)["temperatures"]
    return value


def store(data):
    if not glob('temp_data.txt'):
        with open('temp_data.txt', 'w') as new_file:
            new_file.write('Time,Temperature'+'\n')
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    with open('temp_data.txt', 'a') as file:
        file.write(f"{date},{data}\n")


def read():
    df = pd.read_csv('temp_data.txt')
    dates = [date for date in df["Time"]]
    temps = [temp for temp in df["Temperature"]]
    return dates, temps


st.title("Temperature Scraper")
scraped = scrape(URL)
extracted = extract(scraped)
store(extracted)
dates, temps = read()
figure = px.line(x=dates, y=temps, labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure)


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    store(extracted)
    read()
