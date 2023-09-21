from difflib import SequenceMatcher
from slugify import slugify
from utils.lower_title import lower


def check_similarity(text1, text2, thresh):
    text1 = lower(text1).split()
    text2 = lower(text2).split()

    text1.sort()
    text2.sort()

    is_similar = SequenceMatcher(None, text1, text2).ratio() > thresh
    return is_similar


from dotenv import load_dotenv

load_dotenv()

import os
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="library"
)

cursor = db.cursor()

source = ["kitapsec", "islerkitap", "kitapyurdu", "bkmkitap", "isemkitap", "sadecekitap", "kitapsepeti"]
merged_books = set()

for s in source:
    cursor.execute(f"SELECT id, name, publisher, number_of_page, subject, grade, year, type FROM {s}")
    for book in [book for book in cursor]:
        id, name, publisher, number_of_page, subject, grade, year, type = book

        if number_of_page == None:
            if year == None:
                cursor.execute(f"""SELECT name, publisher, number_of_page, subject, grade, year, {s}_id FROM book 
                               WHERE (subject = %s) AND (grade = %s) AND ({s}_id IS NULL)
                               """, (subject, grade))
            else:
                cursor.execute(f"""SELECT name, publisher, number_of_page, subject, grade, year, {s}_id FROM book 
                               WHERE (year = %s OR year IS NULL) AND (subject = %s) AND (grade = %s) AND ({s}_id IS NULL)
                               """, (year, subject, grade))
        else:
            if year == None:
                cursor.execute(f"""SELECT name, publisher, number_of_page, subject, grade, year, {s}_id FROM book 
                               WHERE (number_of_page = %s OR number_of_page IS NULL) AND (subject = %s) AND (grade = %s) AND ({s}_id IS NULL)
                               """, (number_of_page, subject, grade))
            else:
                cursor.execute(f"""SELECT name, publisher, number_of_page, subject, grade, year, {s}_id FROM book 
                               WHERE (number_of_page = %s OR number_of_page IS NULL) AND (year = %s OR year IS NULL) AND (subject = %s) AND (grade = %s) AND ({s}_id IS NULL)
                               """, (number_of_page, year, subject, grade))

        possible_matches = [match for match in cursor]

        if possible_matches:
            for match in possible_matches:
                possible_name, possible_publisher, *_ = match
                if (check_similarity(possible_name, name, 0.8) and check_similarity(possible_publisher, publisher, 0.8)) or check_similarity(possible_name, name, 0.95):
                    print("This book already exists. Merging...")
                    print("Book: ", book)
                    print("Matched: ", match)
                    print("****************************************")
                    cursor.execute(f"UPDATE book SET {s}_id = %s WHERE name = %s", (id, possible_name))
                    merged_books.add(possible_name)
                    break

        else:
            cursor.execute(f"""INSERT INTO book (slug, name, publisher, number_of_page, subject, grade, year, type, {s}_id) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                           """, (slugify(name), name, publisher, number_of_page, subject, grade, year, type, id))


db.commit()

cursor.execute("SELECT COUNT(*) FROM book")
result = cursor.fetchone()
row_count = result[0]

print("----------------------------------------")
print(f"{len(merged_books)}/{row_count} ({100 * len(merged_books)//row_count}%) books in total with multiple sources.")
print("----------------------------------------")
