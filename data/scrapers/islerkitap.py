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

for i in range(2):  # range(112)
    try:
        response = requests.get(f"https://www.kitapisler.com/YKS-Yuksekogretim-Kurum-Sinavi-1196?start={(i-1)*40}&")
        response.raise_for_status()
    except:
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("div", class_="listingProductListingFull")

    for book in books:
        try:
            page_response = requests.get("https://www.kitapisler.com/" + book.find("div", class_="list_title_type1_text").find("a")["href"])
            page_response.raise_for_status()
        except:
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try:
            name = page.find("div", class_="dName").find("span").text
        except:
            continue

        try:
            publisher = page.find("div", class_="dMarka").find("span").text
            publisher = title(publisher)
        except:
            continue

        try:
            number_of_page = page.find("div", class_="dSayfa").text
            number_of_page = int(number_of_page)
        except:
            number_of_page = None

        try:
            current_price = page.find_all("span", id="pric")[3].text
            current_price = current_price.replace("TL", "").strip()
            current_price = current_price.replace(".", "")
            current_price = current_price.replace(",", ".")
        except:
            current_price = None

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

        try:
            image = "https://www.kitapisler.com/" + page.find("img", attrs={"class": "product_imagesplaceholder"})["src"]
        except:
            image = None

        sql = "INSERT INTO islerkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)
        cursor.execute(sql, val)


db.commit()
