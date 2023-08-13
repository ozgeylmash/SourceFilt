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
cursor.execute("TRUNCATE TABLE islerkitap")

for i in range(30): 
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
            page_response = requests.get("https://www.kitapisler.com/"+book.find("div",class_="list_title_type1_text").find("a")["href"])
            page_response.raise_for_status()
        except: 
            print("Failed to load a book page.")
            continue
           
        page = BeautifulSoup(page_response.content, "lxml")

        try: 
            name = page.find("div", class_ = "dName").find("span").text
            name = name.replace(",", "-").strip()
        except: 
            name = None

        try: 
            publisher = page.find("div", class_="dMarka").find("span").text 
            publisher = title(publisher)
        except: 
            publisher = None

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
            score = page.find("div",class_="ratingblock").find("cite").text
        except:
            score = None

        try: 
            subject, grade, year = BC.determine_category(name)
        except: 
            subject, grade, year = "genel", "lise", None

        link = "https://www.kitapisler.com/" + book.find("div",class_="list_title_type1_text").find("a")["href"]

        try: 
            image = "https://www.kitapisler.com/" + page.find("img", attrs={"class": "product_imagesplaceholder"})["src"]
        except:
            image = None

        sql = "INSERT INTO islerkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, year, link, image)
        cursor.execute(sql, val)


cursor.execute("SELECT name FROM islerkitap GROUP BY name HAVING count(*) >= 2")

duplicates = [duplicate[0] for duplicate in cursor]
best_instances = []
print(f"{len(duplicates)} unique duplicated books detected and resolved.")

if duplicates:
    for duplicate in duplicates:
        cursor.execute("SELECT islerkitap_id, quantity FROM islerkitap WHERE name = %s", (duplicate, ))
        instances = [x for x in cursor]
        best_instances.append(max(instances, key = lambda i : i[1] if i[1] != None else -1)[0])

    duplicates_string = ','.join(['%s'] * len(duplicates))
    best_instances_string = ','.join(['%s'] * len(best_instances))

    sql = "DELETE FROM islerkitap WHERE name IN (%s)" % duplicates_string + "AND islerkitap_id NOT IN (%s)" % best_instances_string
    val = duplicates + best_instances
    cursor.execute(sql, val)

    cursor.execute("ALTER TABLE islerkitap DROP COLUMN islerkitap_id");
    cursor.execute("ALTER TABLE islerkitap ADD islerkitap_id INT PRIMARY KEY AUTO_INCREMENT FIRST");

db.commit()
