from difflib import SequenceMatcher
from utils.lower_title import lower

def check_similarity(text1, text2):
    text1 = lower(text1).split()
    text2 = lower(text2).split()

    text1.sort()
    text2.sort()

    threshold = 0.7
    is_similar = SequenceMatcher(None, text1, text2).ratio() > threshold
    return is_similar

from dotenv import load_dotenv
import os

load_dotenv()

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor()
cursor.execute("TRUNCATE TABLE book")

cursor.execute("SELECT kitapsec_id, name, publisher, number_of_page, subject, grade, year FROM kitapsec")
kitapsec = [book for book in cursor]

for book in kitapsec:
    kitapsec_id, name, publisher, number_of_page, subject, grade, year = book

    if number_of_page == None:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, kitapsec_id FROM book 
                    WHERE subject = %s AND grade = %s AND year = %s AND kitapsec_id IS NULL
                    """, (subject, grade, year))
    else:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, kitapsec_id FROM book 
                   WHERE number_of_page BETWEEN %s - 10 AND %s + 10 AND subject = %s AND grade = %s AND year = %s AND kitapsec_id IS NULL
                   """, (number_of_page, number_of_page, subject, grade, year))
    
    possible_matches = [match for match in cursor]

    if possible_matches:
        for match in possible_matches:
            possible_name, possible_publisher, *_ = match
            if check_similarity(possible_name, name) and check_similarity(possible_publisher, publisher):
                print("****************************************")
                print("This book already exists. Merging...")
                print("Book: ", book)
                print("Matched: ", match)
                print("****************************************")
                cursor.execute("UPDATE book SET kitapsec_id = %s WHERE name = %s", (kitapsec_id, possible_name))
                break
            else:
                cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, year, kitapsec_id) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                               (name, publisher, number_of_page, subject, grade, year, kitapsec_id))
                break
    else:
        cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, year, kitapsec_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                        (name, publisher, number_of_page, subject, grade, year, kitapsec_id))
        

cursor.execute("SELECT islerkitap_id, name, publisher, number_of_page, subject, grade, year FROM islerkitap")
islerkitap = [book for book in cursor]

for book in islerkitap:
    islerkitap_id, name, publisher, number_of_page, subject, grade, year = book

    if number_of_page == None:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, islerkitap_id FROM book 
                    WHERE subject = %s AND grade = %s AND year = %s AND islerkitap_id IS NULL
                    """, (subject, grade, year))
    else:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, islerkitap_id FROM book 
                   WHERE number_of_page BETWEEN %s - 10 AND %s + 10 AND subject = %s AND grade = %s AND year = %s AND islerkitap_id IS NULL
                   """, (number_of_page, number_of_page, subject, grade, year))
    
    possible_matches = [match for match in cursor]

    if possible_matches:
        for match in possible_matches:
            possible_name, possible_publisher, *_ = match
            if check_similarity(possible_name, name) and check_similarity(possible_publisher, publisher):
                print("**********")
                print("This book already exists. Merging...")
                print("Book: ", book)
                print("Matched: ", match)
                print("**********")
                cursor.execute("UPDATE book SET islerkitap_id = %s WHERE name = %s", (islerkitap_id, possible_name))
                break
            else:
                cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, year, islerkitap_id) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                               (name, publisher, number_of_page, subject, grade, year, islerkitap_id))
                break
    else:
        cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, year, islerkitap_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                        (name, publisher, number_of_page, subject, grade, year, islerkitap_id))
        

cursor.execute("SELECT kitapyurdu_id, name, publisher, number_of_page, subject, grade, year FROM kitapyurdu")
kitapyurdu = [book for book in cursor]

for book in kitapyurdu:
    kitapyurdu_id, name, publisher, number_of_page, subject, grade, year = book

    if number_of_page == None:
        if year == None:
            cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, kitapyurdu_id FROM book 
                        WHERE number_of_page IS NULL AND subject = %s AND grade = %s AND year IS NULL AND kitapyurdu_id IS NULL
                        """, (subject, grade))
        else:
            cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, kitapyurdu_id FROM book 
                        WHERE number_of_page IS NULL AND subject = %s AND grade = %s AND year = %s AND kitapyurdu_id IS NULL
                        """, (subject, grade, year))
    else:
        if year == None:
            cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, kitapyurdu_id FROM book 
                   WHERE number_of_page BETWEEN %s - 10 AND %s + 10 AND subject = %s AND grade = %s AND year IS NULL AND kitapyurdu_id IS NULL
                   """, (number_of_page, number_of_page, subject, grade))
        else:
            cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, year, kitapyurdu_id FROM book 
                        WHERE number_of_page BETWEEN %s - 10 AND %s + 10 AND subject = %s AND grade = %s AND year = %s AND kitapyurdu_id IS NULL
                        """, (number_of_page, number_of_page, subject, grade, year))
    
    possible_matches = [match for match in cursor]
    if possible_matches:
        for match in possible_matches:
            possible_name, possible_publisher, *_ = match
            if check_similarity(possible_name, name) and check_similarity(possible_publisher, publisher):
                print("**********")
                print("This book already exists. Merging...")
                print("Book: ", book)
                print("Matched: ", match)
                print("**********")
                cursor.execute("UPDATE book SET kitapyurdu_id = %s WHERE name = %s", (kitapyurdu_id, possible_name))
                break

    else:
        cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, year, kitapyurdu_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                        (name, publisher, number_of_page, subject, grade, year, kitapyurdu_id))


db.commit()