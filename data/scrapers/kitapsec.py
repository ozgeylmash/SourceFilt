import sys
sys.path.append("..")
from data.utils.BookCategorizer import BookCategorizer as BC
from data.utils.lower_title import title

import os
import requests
import mysql.connector
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor(buffered=True)

for i in range(2):  # range(301)
    try:
        response = requests.get(f"https://www.kitapsec.com/Products/YKS-Kitaplari/{i+1}-2-0a0-0-0-0-0-0.xhtml")
        response.raise_for_status()
    except:
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("a", attrs={"class": "text"})

    for book in books:
        try:
            page_response = requests.get(book["href"])
            page_response.raise_for_status()
        except:
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try:
            name = page.find("div", attrs={"class": "dty_SagBlok"}).find("h1").text
        except:
            continue

        try:
            publisher = page.find("div", attrs={"itemprop": "publisher"}).find("span").text
            publisher = title(publisher)
        except:
            continue

        try:
            number_of_page = page.find("div", attrs={"itemprop": "numberOfPages"}).text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        try:
            current_price = page.find("span", attrs={"class": "fiyati"}).text
            current_price = current_price.replace("TL", "").strip()
        except:
            current_price = None

        try:
            original_price = page.find("span", attrs={"class": "piyasa"}).find("strike").text
            original_price = original_price.replace("TL", "").strip()
        except:
            original_price = current_price

        try:
            quantity = page.find("div", string="Toplam Satılan").find_next_siblings()[1].text
            quantity = quantity.replace("Adet", "").strip()
        except:
            quantity = None

        try:
            score = page.find("font", attrs={"class": "ortalamPuan"}).text
        except:
            score = None

        subject, grade, year, type = BC.determine_category(name, publisher)

        link = book["href"]

        try:
            image = "https:" + page.find("a", attrs={"rel": "urunresim"})["href"]
        except:
            image = None

        sql = "INSERT INTO kitapsec (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)
        cursor.execute(sql, val)


db.commit()
