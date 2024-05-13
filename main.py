import requests
import selectorlib
from send_email import send_email
import os
import sqlite3
import time

connection = sqlite3.connect("data.db")

URL = "http://programmer100.pythonanywhere.com/tours/"
head = """HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}"""


def scrape(URL):
    response = requests.get(URL)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def read(extracted):
    cursor = connection.cursor()
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band,city,date))
    rows = cursor.fetchall()
    return rows


def store(extracted):
    row = extracted.split(",")
    row = [item.strip(' ') for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        if extracted != "No upcoming tours":
            row = read(extracted)
            print(row)
            if not row:
                messsage = f"""Subject:A new music event was found \n                   
                                   
                {extracted}!!!"""
                send_email(message=messsage)
                store(extracted)
        time.sleep(2)