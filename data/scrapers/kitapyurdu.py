import sys
sys.path.append("..")
from data.utils.BookCategorizer import BookCategorizer as BC
from data.utils.lower_title import title

import os
import re
import requests
import logging
import mysql.connector
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

formatter = logging.Formatter("%(levelname)s:\n%(message)s \n ")

handler = logging.FileHandler(filename="log/kitapyurdu.log", mode="w")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.Logger("kitapyurdu")
logger.addHandler(handler)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor(buffered=True)

for i in range(5):  # range(38)
    if i == 0:
        page_link = "https://www.kitapyurdu.com/index.php?route=product/category/&filter_category_all=true&category_id=293&sort=purchased_365&order=DESC&filter_in_stock=1"
    else:
        page_link = f"https://www.kitapyurdu.com/index.php?route=product/category&page={i}&filter_category_all=true&path=1_737_1067&filter_in_stock=1&sort=purchased_365&order=DESC"

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

    books = soup.find_all("div", attrs={"class": "product-cr"})

    for book in books:
        book_link = book.find("a", attrs={"class": "pr-img-link"})["href"]
        page_response = requests.get(book_link)

        page = BeautifulSoup(page_response.content, "lxml")

        name = page.find("h1", attrs={"class": "pr_header__heading"}).text

        publisher = page.find("div", attrs={"class": "pr_producers__publisher"}).find("a").text
        publisher = title(publisher)

        try:
            number_of_page = page.find("td", string="Sayfa Sayısı:").find_next_sibling().text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        current_price = page.find("div", attrs={"class": "pr_price__content"}).find("div").text
        current_price = current_price.replace(".", "")
        current_price = current_price.replace(",", ".")

        try:
            original_price = page.find("span", attrs={"class": "pr_price__strikeout-list"}).text.strip()
            original_price = original_price.replace(".", "")
            original_price = original_price.replace(",", ".")
        except:
            original_price = current_price

        try:
            quantity = page.find("p", attrs={"class": "purchased"}).text
            quantity = quantity.replace(".", "")
            quantity = re.findall("[0-9]+", quantity)[0]
        except:
            quantity = None

        try:
            score = len(book.find("div", attrs={"class": "rating"}).find_all("i", attrs={"class": "active"}))
        except:
            score = None

        subject, grade, year, type = BC.determine_category(name, publisher)

        link = book.find("a", attrs={"class": "pr-img-link"})["href"]

        image = page.find("a", attrs={"class": "js-jbox-book-cover"})["href"]

        sql = "INSERT INTO kitapyurdu (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)

        try:
            cursor.execute(sql, val)
        except Exception as e:
            logger.error(val)
            logger.error(e)

        logger.debug(val)

db.commit()

cursor.execute("SELECT COUNT(*) FROM kitapyurdu")
result = cursor.fetchone()
row_count = result[0]

print(f"Completed: kitapyurdu ({row_count}/{row_count})")
logger.info(f"{row_count} book has been scraped from kitapyurdu.")
