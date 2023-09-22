import sys
sys.path.append("..")
from data.utils.BookCategorizer import BookCategorizer as BC
from data.utils.lower_title import title

import os
import requests
import logging
import mysql.connector
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

formatter = logging.Formatter("%(levelname)s:\n%(message)s \n ")

handler = logging.FileHandler(filename="log/sadecekitap.log", mode="w")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.Logger("sadecekitap")
logger.addHandler(handler)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor(buffered=True)

for i in range(5):  # range(28)
    page_link = f"https://www.sadecekitap.com/yks-hazirlik/{i+1}?flt=Stok%20Durumu_Stokta%20var"

    try:
        response = requests.get(page_link)
        response.raise_for_status()
        assert not response.history

    except requests.exceptions.HTTPError:
        logger.error(f"404 Not Found - Failed to load {page_link}")
        continue

    except AssertionError:
        logger.warning(f"301 Redirect - Failed to load {page_link}")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("a", attrs={"class": "imgLink"})

    for book in books:
        book_link = "https://www.sadecekitap.com/" + book["href"]
        page_response = requests.get(book_link)

        page = BeautifulSoup(page_response.content, "lxml")

        name = page.find("h1", attrs={"class": "product-name"}).text

        publisher = page.find("div", attrs={"class": "info-orther"}).find_all("p")[1].find("a").text
        publisher = title(publisher)

        number_of_page = None

        current_price = page.find("span", attrs={"id": "shopPHPUrunFiyatYTL"}).text

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

        image = "https://www.sadecekitap.com/" + book.find("img", attrs={"class": "image2"})["data-src"]

        sql = "INSERT INTO sadecekitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)

        try:
            cursor.execute(sql, val)
        except Exception as e:
            logger.error(val)
            logger.error(e)

        logger.debug(val)


db.commit()

cursor.execute("SELECT COUNT(*) FROM sadecekitap")
result = cursor.fetchone()
row_count = result[0]

print(f"Completed: sadecekitap ({row_count}/{row_count})")
logger.info(f"{row_count} book has been scraped from sadecekitap.")
