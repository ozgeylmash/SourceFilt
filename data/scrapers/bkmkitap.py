import sys
sys.path.append("data")
from BookCategorizer import BookCategorizer as BC
from utils.lower_title import title

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
cursor.execute("TRUNCATE TABLE bkmkitap")

for i in range(20): # range(50)
    try: 
        response = requests.get(f"https://www.bkmkitap.com/2024-yks-tyt-ve-ayt-kitaplari?sort=1&stock=1&pg={i+1}")
        response.raise_for_status()
    except: 
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("div", attrs={"class": "productDetails"})
    
    for book in books:
        try: 
            page_response = requests.get("https://www.bkmkitap.com" + book.find("a", attrs={"class": "detailLink"})["href"])
            page_response.raise_for_status()
        except: 
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try: 
            name = page.find("h1", attrs={"id": "productName"}).text
        except: 
            name = None

        try: 
            publisher = page.find("a", attrs={"class": "product-brand"})["title"]
            publisher = publisher.replace("Yayınevi: ", "").strip()
            publisher = title(publisher)
        except: 
            publisher = None

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

        try: 
            subject, grade, year = BC.determine_category(name, publisher)
        except: 
            subject, grade, year = "genel", "lise", None

        link = "https://www.bkmkitap.com" + book.find("a", attrs={"class": "detailLink"})["href"]

        try: 
            image = page.find("span", attrs={"class": "imgInner"}).find("img")["src"]
        except:
            image = None

        sql = "INSERT INTO bkmkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, link, image)
        cursor.execute(sql, val)


cursor.execute("SELECT name FROM bkmkitap GROUP BY name HAVING count(*) >= 2")

duplicates = [duplicate[0] for duplicate in cursor]
best_instances = []
print(f"{len(duplicates)} unique duplicated books detected and resolved.")

if duplicates:
    for duplicate in duplicates:
        cursor.execute("SELECT bkmkitap_id, quantity FROM bkmkitap WHERE name = %s", (duplicate, ))
        instances = [x for x in cursor]
        best_instances.append(max(instances, key = lambda i : i[1] if i[1] != None else -1)[0])

    duplicates_string = ",".join(["%s"] * len(duplicates))
    best_instances_string = ",".join(["%s"] * len(best_instances))
    sql = "DELETE FROM bkmkitap WHERE name IN (%s)" % duplicates_string + "AND bkmkitap_id NOT IN (%s)" % best_instances_string
    val = duplicates + best_instances
    cursor.execute(sql, val)

    cursor.execute("ALTER TABLE bkmkitap DROP COLUMN bkmkitap_id");
    cursor.execute("ALTER TABLE bkmkitap ADD bkmkitap_id INT PRIMARY KEY AUTO_INCREMENT FIRST");

db.commit()