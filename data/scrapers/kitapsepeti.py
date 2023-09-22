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

for i in range(2):  # range(88)
    try:
        response = requests.get(f"https://www.kitapsepeti.com/yks-tyt-ayt-hazirlik-kitaplari?stock=1&sort=1&pg={i+1}")
        response.raise_for_status()
    except:
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("div", attrs={"class": "productDetails"})

    for book in books:
        try:
            page_response = requests.get("https://www.kitapsepeti.com" + book.find("a", attrs={"class": "detailLink"})["href"])
            page_response.raise_for_status()
        except:
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try:
            name = page.find("h1", attrs={"id": "productName"}).text
        except:
            continue

        try:
            publisher = page.find("a", attrs={"class": "product-brand"})["title"]
            publisher = publisher.replace("Yayınevi: ", "").strip()
            publisher = title(publisher)
        except:
            continue

        try:
            number_of_page = page.find("span", string="Sayfa Sayısı:").find_next_sibling().text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        try:
            current_price = page.find("span", attrs={"class": "product-price"}).text
            current_price = current_price.replace(".", "")
            current_price = current_price.replace(",", ".")
        except:
            current_price = None

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

        link = "https://www.kitapsepeti.com" + book.find("a", attrs={"class": "detailLink"})["href"]

        try:
            image = page.find("span", attrs={"class": "imgInner"}).find("img")["src"]
        except:
            image = None

        sql = "INSERT INTO kitapsepeti (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)
        cursor.execute(sql, val)


db.commit()
