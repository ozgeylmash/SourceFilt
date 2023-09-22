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

for i in range(2):  # range(28)
    try:
        response = requests.get(f"https://www.sadecekitap.com/yks-hazirlik/{i+1}?flt=Stok%20Durumu_Stokta%20var")
        response.raise_for_status()
    except:
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("a", attrs={"class": "imgLink"})

    for book in books:
        try:
            page_response = requests.get("https://www.sadecekitap.com/" + book["href"])
            page_response.raise_for_status()
        except:
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try:
            name = page.find("h1", attrs={"class": "product-name"}).text
        except:
            continue

        try:
            publisher = page.find("div", attrs={"class": "info-orther"}).find_all("p")[1].find("a").text
            publisher = title(publisher)
        except:
            continue

        number_of_page = None

        try:
            current_price = page.find("span", attrs={"id": "shopPHPUrunFiyatYTL"}).text
        except:
            current_price = None

        try:
            original_price = page.find("span", attrs={"class": "old-price"}).text
            original_price = original_price.replace("TL", "").strip()
            assert original_price
        except:
            original_price = current_price

        quantity = None

        score = None

        subject, grade, year, type = BC.determine_category(name, publisher)

        link = "https://www.sadecekitap.com/" + book["href"]

        try:
            image = "https://www.sadecekitap.com/" + book.find("img", attrs={"class": "image2"})["data-src"]
        except:
            image = None

        sql = "INSERT INTO sadecekitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)
        cursor.execute(sql, val)


db.commit()
