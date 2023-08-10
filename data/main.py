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

# cursor.execute("select * from kitapsec")

# for x in cursor:
#   print(x)