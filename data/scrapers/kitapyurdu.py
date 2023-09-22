import sys
sys.path.append("..")
from data.utils.BookCategorizer import BookCategorizer as BC
from data.utils.lower_title import title

import os
import re
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

for i in range(2):  # range(38)
    try:
        if i == 0:
            response = requests.get("https://www.kitapyurdu.com/index.php?route=product/category/&filter_category_all=true&category_id=293&sort=purchased_365&order=DESC&filter_in_stock=1")
        else:
            response = requests.get(f"https://www.kitapyurdu.com/index.php?route=product/category&page={i}&filter_category_all=true&path=1_737_1067&filter_in_stock=1&sort=purchased_365&order=DESC")
        response.raise_for_status()
    except:
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("div", attrs={"class": "product-cr"})

    for book in books:
        try:
            page_response = requests.get(book.find("a", attrs={"class": "pr-img-link"})["href"])
            page_response.raise_for_status()
        except:
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try:
            name = page.find("h1", attrs={"class": "pr_header__heading"}).text
        except:
            continue

        try:
            publisher = page.find("div", attrs={"class": "pr_producers__publisher"}).find("a").text
            publisher = title(publisher)
        except:
            continue

        try:
            number_of_page = page.find("td", string="Sayfa Sayısı:").find_next_sibling().text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        try:
            current_price = page.find("div", attrs={"class": "pr_price__content"}).find("div").text

            current_price = current_price.replace(".", "")
            current_price = current_price.replace(",", ".")
        except:
            current_price = None

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

        try:
            image = page.find("a", attrs={"class": "js-jbox-book-cover"})["href"]
        except:
            image = None

        sql = "INSERT INTO kitapyurdu (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)
        cursor.execute(sql, val)


db.commit()
