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

handler = logging.FileHandler(filename="log/islerkitap.log", mode="w")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.Logger("islerkitap")
logger.addHandler(handler)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor(buffered=True)

for i in range(5):  # range(112)
    page_link = f"https://www.kitapisler.com/YKS-Yuksekogretim-Kurum-Sinavi-1196?start={(i-1)*40}&"

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

    books = soup.find_all("div", class_="listingProductListingFull")

    for book in books:
        book_link = "https://www.kitapisler.com/" + book.find("div", class_="list_title_type1_text").find("a")["href"]
        page_response = requests.get(book_link)

        page = BeautifulSoup(page_response.content, "lxml")

        name = page.find("div", class_="dName").find("span").text

        publisher = page.find("div", class_="dMarka").find("span").text
        publisher = title(publisher)

        try:
            number_of_page = page.find("div", class_="dSayfa").text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        current_price = page.find_all("span", id="pric")[3].text
        current_price = current_price.replace("TL", "").strip()
        current_price = current_price.replace(".", "")
        current_price = current_price.replace(",", ".")

        try:
            original_price = page.find_all("span", id="pric")[2].text
            original_price = original_price.replace("TL", "").strip()
            original_price = original_price.replace(".", "")
            original_price = original_price.replace(",", ".")
        except:
            original_price = current_price

        try:
            quantity = page.find("div", class_="dYayinevi").text
            quantity = quantity.replace("Adet", "").strip()
        except:
            quantity = None

        try:
            score = page.find("div", class_="ratingblock").find("cite").text
        except:
            score = None

        subject, grade, year, type = BC.determine_category(name, publisher)

        link = "https://www.kitapisler.com/" + book.find("div", class_="list_title_type1_text").find("a")["href"]

        image = "https://www.kitapisler.com/" + page.find("img", attrs={"class": "product_imagesplaceholder"})["src"]

        sql = "INSERT INTO islerkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)

        try:
            cursor.execute(sql, val)
        except Exception as e:
            logger.error(val)
            logger.error(e)

        logger.debug(val)


db.commit()

cursor.execute("SELECT COUNT(*) FROM islerkitap")
result = cursor.fetchone()
row_count = result[0]

print(f"Completed: islerkitap ({row_count}/{row_count})")
logger.info(f"{row_count} book has been scraped from islerkitap.")
