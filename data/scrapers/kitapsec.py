import sys
sys.path.append('data')
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
cursor.execute("TRUNCATE TABLE kitapsec")

for i in range(30): # range(301)
    try: 
        response = requests.get(f"https://www.kitapsec.com/Products/YKS-Kitaplari/{i+1}-2-0a0-0-0-0-0-0.xhtml")
        response.raise_for_status()
    except: 
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("a", attrs={"class": "text"})
    
    for book in books:
        try: 
            page_response = requests.get(book["href"])
            page_response.raise_for_status()
        except: 
            print("Failed to load a book page.")
            continue

        page = BeautifulSoup(page_response.content, "lxml")

        try: 
            name = page.find("div", attrs={"class": "dty_SagBlok"}).find("h1").text 
            name = name.replace(",", "-").strip()
        except: 
            name = None

        try: 
            publisher = page.find("div", attrs={"itemprop": "publisher"}).find("span").text 
            publisher = title(publisher)
        except: 
            publisher = None

        try: 
            number_of_page = page.find("div", attrs={"itemprop": "numberOfPages"}).text
            number_of_page = int(number_of_page)
        except: 
            number_of_page = None

        try: 
            current_price = page.find("span", attrs={"class": "fiyati"}).text
            current_price = current_price.replace("TL", "").strip()
        except: 
            current_price = None

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

        try: 
            subject, grade, year = BC.determine_category(name)
        except: 
            subject, grade, year = "genel", "lise", None

        link = book["href"]

        try: 
            image = "https:" + page.find("a", attrs={"rel": "urunresim"})["href"]
        except:
            image = None

        sql = "INSERT INTO kitapsec (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, link, image)
        cursor.execute(sql, val)


cursor.execute("SELECT name FROM kitapsec GROUP BY name HAVING count(*) >= 2")

duplicates = [duplicate[0] for duplicate in cursor]
best_instances = []
print(f"{len(duplicates)} unique duplicated books detected and resolved.")

if duplicates:
    for duplicate in duplicates:
        cursor.execute("SELECT kitapsec_id, quantity FROM kitapsec WHERE name = %s", (duplicate, ))
        instances = [x for x in cursor]
        best_instances.append(max(instances, key = lambda i : i[1] if i[1] != None else -1)[0])

    duplicates_string = ','.join(['%s'] * len(duplicates))
    best_instances_string = ','.join(['%s'] * len(best_instances))
    sql = "DELETE FROM kitapsec WHERE name IN (%s)" % duplicates_string + "AND kitapsec_id NOT IN (%s)" % best_instances_string
    val = duplicates + best_instances
    cursor.execute(sql, val)

    cursor.execute("ALTER TABLE kitapsec DROP COLUMN kitapsec_id");
    cursor.execute("ALTER TABLE kitapsec ADD kitapsec_id INT PRIMARY KEY AUTO_INCREMENT FIRST");

db.commit()