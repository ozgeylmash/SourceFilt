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
cursor.execute("TRUNCATE TABLE isemkitap")

try: 
    response = requests.get(f"https://www.isemkitap.com/yks-kitaplari?stock=1&sort=1&ps=5") # ps=238
    response.raise_for_status()
except: 
    print("Failed to load the index page.")

soup = BeautifulSoup(response.content, "lxml")

books = soup.find_all("div", attrs={"class": "productDetails"})

for book in books:
    try: 
        page_response = requests.get("https://www.isemkitap.com" + book.find("a", attrs={"class": "detailLink"})["href"])
        page_response.raise_for_status()
    except: 
        print("Failed to load a book page.")
        continue

    page = BeautifulSoup(page_response.content, "lxml")

    try: 
        name = page.find("h1", attrs={"id": "productName"}).text
        name = name.strip()
    except: 
        name = None

    try: 
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
    except: 
        publisher = None

    try: 
        number_of_page = page.find("span", string="Sayfa Sayısı").find_next_siblings()[1].text
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
        subject, grade, year, type = BC.determine_category(name, publisher)
    except: 
        subject, grade, year, type = "genel", "lise", None, None

    link = "https://www.isemkitap.com" + book.find("a", attrs={"class": "detailLink"})["href"]

    try: 
        image = page.find("span", attrs={"class": "imgInner"}).find("img")["src"]
    except:
        image = None

    sql = "INSERT INTO isemkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, type, link, image)
    cursor.execute(sql, val)


cursor.execute("SELECT name FROM isemkitap GROUP BY name HAVING count(*) >= 2")

duplicates = [duplicate[0] for duplicate in cursor]
best_instances = []
print(f"{len(duplicates)} unique duplicated books detected and resolved.")

if duplicates:
    for duplicate in duplicates:
        cursor.execute("SELECT isemkitap_id, quantity FROM isemkitap WHERE name = %s", (duplicate, ))
        instances = [x for x in cursor]
        best_instances.append(max(instances, key = lambda i : i[1] if i[1] != None else -1)[0])

    duplicates_string = ",".join(["%s"] * len(duplicates))
    best_instances_string = ",".join(["%s"] * len(best_instances))
    sql = "DELETE FROM isemkitap WHERE name IN (%s)" % duplicates_string + "AND isemkitap_id NOT IN (%s)" % best_instances_string
    val = duplicates + best_instances
    cursor.execute(sql, val)

    cursor.execute("ALTER TABLE isemkitap DROP COLUMN isemkitap_id");
    cursor.execute("ALTER TABLE isemkitap ADD isemkitap_id INT PRIMARY KEY AUTO_INCREMENT FIRST");

db.commit()