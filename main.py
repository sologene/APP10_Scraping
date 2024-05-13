import requests
import selectorlib
from send_email import send_email
import os
import time

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

def read():
    with open("data.txt", "r") as file:
        return file.read()


def store(extracted):
    with open("data.txt","a") as file:
        file.write(extracted + "\n")


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        if extracted != "No upcoming tours":
            if extracted not in read():
                messsage = f"""Subject:A new music event was found \n                        
                {extracted}!!!"""
                send_email(message=messsage)
                store(extracted)
        time.sleep(2)