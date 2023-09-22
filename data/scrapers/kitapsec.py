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

handler = logging.FileHandler(filename="log/kitapsec.log", mode="w")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.Logger("kitapsec")
logger.addHandler(handler)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor(buffered=True)

for i in range(5):  # range(301)
    page_link = f"https://www.kitapsec.com/Products/YKS-Kitaplari/{i+1}-2-0a0-0-0-0-0-0.xhtml"

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

    books = soup.find_all("a", attrs={"class": "text"})

    for book in books:
        book_link = book["href"]
        page_response = requests.get(book_link)

        page = BeautifulSoup(page_response.content, "lxml")

        name = page.find("div", attrs={"class": "dty_SagBlok"}).find("h1").text

        publisher = page.find("div", attrs={"itemprop": "publisher"}).find("span").text
        publisher = title(publisher)

        try:
            number_of_page = page.find("div", attrs={"itemprop": "numberOfPages"}).text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        current_price = page.find("span", attrs={"class": "fiyati"}).text
        current_price = current_price.replace("TL", "").strip()

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

        image = "https:" + page.find("a", attrs={"rel": "urunresim"})["href"]

        sql = "INSERT INTO kitapsec (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)

        try:
            cursor.execute(sql, val)
        except Exception as e:
            logger.error(val)
            logger.error(e)

        logger.debug(val)


db.commit()

cursor.execute("SELECT COUNT(*) FROM kitapsec")
result = cursor.fetchone()
row_count = result[0]

print(f"Completed: kitapsec ({row_count}/{row_count})")
logger.info(f"{row_count} book has been scraped from kitapsec.")
