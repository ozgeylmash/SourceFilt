from difflib import SequenceMatcher

def check_similarity(text1, text2):
    text1 = text1.lower().split()
    text2 = text2.lower().split()

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

cursor.execute("SELECT kitapsec_id, name, publisher, number_of_page, subject, grade FROM kitapsec")
kitapsec = [book for book in cursor]

for book in kitapsec:
    kitapsec_id, name, publisher, number_of_page, subject, grade = book

    if number_of_page == -1:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, kitapsec_id FROM book 
                    WHERE subject = %s AND grade = %s AND kitapsec_id IS NULL
                    """, (subject, grade))
    else:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, kitapsec_id FROM book 
                   WHERE number_of_page BETWEEN %s - 10 AND %s + 10 AND subject = %s AND grade = %s AND kitapsec_id IS NULL
                   """, (number_of_page, number_of_page, subject, grade))
    
    possible_matches = [match for match in cursor]

    if possible_matches:
        for match in possible_matches:
            possible_name, possible_publisher, *_ = match
            if check_similarity(possible_name, name) and check_similarity(possible_publisher, publisher):
                print("This book already exists. Merging...")
                print("Book: ", book)
                print("Matched: ", match)
                cursor.execute("UPDATE book SET kitapsec_id = %s WHERE name = %s", (kitapsec_id, possible_name))
                break
            else:
                cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, kitapsec_id) 
                               VALUES (%s, %s, %s, %s, %s, %s);""",
                               (name, publisher, number_of_page, subject, grade, kitapsec_id))
                break
    else:
        cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, kitapsec_id) 
                        VALUES (%s, %s, %s, %s, %s, %s);""",
                        (name, publisher, number_of_page, subject, grade, kitapsec_id))
        

cursor.execute("SELECT islerkitap_id, name, publisher, number_of_page, subject, grade FROM islerkitap")
islerkitap = [book for book in cursor]

for book in islerkitap:
    islerkitap_id, name, publisher, number_of_page, subject, grade = book

    if number_of_page == -1:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, islerkitap_id FROM book 
                    WHERE subject = %s AND grade = %s AND islerkitap_id IS NULL
                    """, (subject, grade))
    else:
        cursor.execute("""SELECT name, publisher, number_of_page, subject, grade, islerkitap_id FROM book 
                   WHERE number_of_page BETWEEN %s - 10 AND %s + 10 AND subject = %s AND grade = %s AND islerkitap_id IS NULL
                   """, (number_of_page, number_of_page, subject, grade))
    
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
                cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, islerkitap_id) 
                               VALUES (%s, %s, %s, %s, %s, %s);""",
                               (name, publisher, number_of_page, subject, grade, islerkitap_id))
                break
    else:
        cursor.execute("""INSERT INTO book (name, publisher, number_of_page, subject, grade, islerkitap_id) 
                        VALUES (%s, %s, %s, %s, %s, %s);""",
                        (name, publisher, number_of_page, subject, grade, islerkitap_id))
        

db.commit()

# cursor.execute(
# """
# CREATE TABLE islerkitap (
#     islerkitap_id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(300),
#     publisher VARCHAR(40),
#     number_of_page INT,
#     current_price DOUBLE(6, 2),
#     original_price DOUBLE(6, 2),
#     quantity INT,
#     score DOUBLE(2, 1),
#     subject VARCHAR(20),
#     grade VARCHAR(10),
#     link VARCHAR(300),
#     image VARCHAR(300)
# );
# """
# )

# cursor.execute(
# """
# CREATE TABLE book (
    # name VARCHAR(300) PRIMARY KEY,
    # publisher VARCHAR(40),
    # number_of_page INT,
    # subject VARCHAR(20),
    # grade VARCHAR(10),
    # kitapsec_id int,
    # islerkitap_id int,
    # FOREIGN KEY(kitapsec_id) REFERENCES kitapsec(kitapsec_id),
    # FOREIGN KEY(islerkitap_id) REFERENCES islerkitap(islerkitap_id)
# );
# """
# )