import sys
sys.path.append('data')
from BookCategorizer import BookCategorizer as BC

import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=["name", "publisher", "number_of_page", "current_price", "original_price", "quantity", "score", "subject", "grade", "link"])

for i in range(2): 
    try: 
        response = requests.get(f"https://www.kitapisler.com/YKS-Yuksekogretim-Kurum-Sinavi-1196?start={(i-1)*40}&")
        response.raise_for_status()
        print(response)
    except: 
        print("Failed to load an index page.")
        continue

    soup = BeautifulSoup(response.content, "lxml")

    books = soup.find_all("div", class_="listingProductListingFull")
    print(len(books))
    for book in books[5:10]:
        
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

        df.loc[len(df)] = [name, publisher, number_of_page, current_price, original_price, quantity, score, subject, grade, link]


df = df.astype({"name": "string", "publisher": "string", "number_of_page": "int32", "current_price": "float32", "original_price": "float32", "quantity": "int32", "score" : "float32", "subject": "string", "grade": "string", "link": "string"})

df.to_csv("data/scraped-data/isler-kitap.csv", index=False)
