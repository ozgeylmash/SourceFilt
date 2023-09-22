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

handler = logging.FileHandler(filename="log/isemkitap.log", mode="w")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.Logger("isemkitap")
logger.addHandler(handler)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor(buffered=True)

page_link = "https://www.isemkitap.com/yks-kitaplari?stock=1&sort=1&ps=5"  # ps=238

try:
    response = requests.get(page_link)
    response.raise_for_status()
    assert not response.history

except requests.exceptions.HTTPError:
    logger.error(f"404 Not Found - Failed to load {page_link}")

except AssertionError:
    logger.warning(f"301 Redirect - Failed to load {page_link}")

soup = BeautifulSoup(response.content, "lxml")

books = soup.find_all("div", attrs={"class": "productDetails"})

for book in books:
    book_link = "https://www.isemkitap.com" + book.find("a", attrs={"class": "detailLink"})["href"]
    page_response = requests.get(book_link)

    page = BeautifulSoup(page_response.content, "lxml")

    name = page.find("h1", attrs={"id": "productName"}).text
    name = name.strip()

    publisher = page.find("a", attrs={"id": "product-brand"})["title"]
    publisher = publisher.replace("Marka:", "")
    publisher = publisher.replace("TYT-AYT", "")
    publisher = publisher.replace("TYT", "")
    publisher = publisher.replace("AYT", "")
    publisher = publisher.replace("ÖABT", "")
    publisher = publisher.replace("Set", "")
    publisher = publisher.replace("-", "")
    publisher = publisher.replace("YKS", "").strip()
    publisher = title(publisher)

    try:
        number_of_page = page.find("span", string="Sayfa Sayısı").find_next_siblings()[1].text
        number_of_page = int(number_of_page)
    except:
        number_of_page = None

    current_price = page.find("span", attrs={"class": "product-price"}).text
    current_price = current_price.replace(".", "")
    current_price = current_price.replace(",", ".")

    try:
        original_price = page.find("span", attrs={"class": "product-price-not-discounted"}).text
        original_price = original_price.replace(".", "")
        original_price = original_price.replace(",", ".")
    except:
        original_price = current_price

    quantity = None

    try:
        score = page.find("div", attrs={"id": "productRight"}).find("div", attrs={"class": "stars"})["style"]
        score = score.replace("width:", "")
        score = score.replace("%;", "")
        score = int(score) / 20
    except:
        score = None

    subject, grade, year, type = BC.determine_category(name, publisher)

    link = "https://www.isemkitap.com" + book.find("a", attrs={"class": "detailLink"})["href"]

    image = page.find("span", attrs={"class": "imgInner"}).find("img")["src"]

    sql = "INSERT INTO isemkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)

    try:
        cursor.execute(sql, val)
    except Exception as e:
        logger.error(val)
        logger.error(e)

    logger.debug(val)


db.commit()

cursor.execute("SELECT COUNT(*) FROM isemkitap")
result = cursor.fetchone()
row_count = result[0]

print(f"Completed: isemkitap ({row_count}/{row_count})")
logger.info(f"{row_count} book has been scraped from isemkitap.")
