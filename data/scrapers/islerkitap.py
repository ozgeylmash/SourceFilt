import sys
sys.path.append('data')
from BookCategorizer import BookCategorizer as BC

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

for i in range(3): 
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
            name = ""

        try: 
            publisher = page.find("div", class_="dMarka").find("span").text 
        except: 
            publisher = ""

        try: 
            number_of_page = page.find("div", class_="dSayfa").text
            number_of_page = int(number_of_page)
        except: 
            number_of_page = -1

        try: 
            current_price = page.find_all("span", id="pric")[3].text
            current_price = current_price.replace("TL", "").strip()
            current_price = current_price.replace(",", ".")
        except: 
            current_price = -1

        try: 
            original_price = page.find_all("span", id="pric")[2].text
            original_price = original_price.replace("TL", "").strip()
            original_price = original_price.replace(",", ".")
        except: 
            original_price = current_price

        try:
            quantity = page.find("div", class_="dYayinevi").text
            quantity = quantity.replace("Adet", "").strip()
        except:
            quantity = -1

        try: 
            score = page.find("div",class_="ratingblock").find("cite").text
        except:
            score = -1

        try: 
            subject, grade = BC.determine_category(name)
        except: 
            subject, grade = "genel", "lise"

        link = "https://www.kitapisler.com/"+book.find("div",class_="list_title_type1_text").find("a")["href"]

        try: 
            image = "https://www.kitapisler.com/" + page.find("img", attrs={"class": "product_imagesplaceholder"})["src"]
        except:
            image = ""

        sql = "INSERT INTO islerkitap (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, link, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, link, image)
        cursor.execute(sql, val)


cursor.execute("SELECT name FROM islerkitap GROUP BY name HAVING count(*) >= 2")

duplicates = [duplicate[0] for duplicate in cursor]
best_instances = []
print(f"{len(duplicates)} unique duplicated books detected and resolved.")

if duplicates:
    for duplicate in duplicates:
        cursor.execute("SELECT islerkitap_id, quantity FROM islerkitap WHERE name = %s", (duplicate, ))
        instances = [x for x in cursor]
        best_instances.append(max(instances, key = lambda i : i[1])[0])
    cursor.execute(f"DELETE FROM islerkitap WHERE name IN {str(tuple(duplicates))} AND islerkitap_id NOT IN {str(tuple(best_instances))}")

    cursor.execute("ALTER TABLE islerkitap DROP COLUMN islerkitap_id");
    cursor.execute("ALTER TABLE islerkitap ADD islerkitap_id INT PRIMARY KEY AUTO_INCREMENT FIRST");

db.commit()
