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

for s in source:
    cursor.execute(f"SELECT name FROM {s} GROUP BY name HAVING count(*) >= 2")

    duplicates = [duplicate[0] for duplicate in cursor]
    best_instances = []
    print(f"{len(duplicates)} unique duplicated books detected and resolved.")

    if duplicates:
        for duplicate in duplicates:
            cursor.execute(f"SELECT id, quantity FROM {s} WHERE name = %s", (duplicate, ))
            instances = [x for x in cursor]
            best_instances.append(max(instances, key=lambda i: i[1] if i[1] != None else -1)[0])

        duplicates_string = ",".join(["%s"] * len(duplicates))
        best_instances_string = ",".join(["%s"] * len(best_instances))
        sql = f"DELETE FROM {s} WHERE name IN (%s)" % duplicates_string + "AND id NOT IN (%s)" % best_instances_string
        val = duplicates + best_instances
        cursor.execute(sql, val)

        cursor.execute(f"ALTER TABLE {s} DROP COLUMN id")
        cursor.execute(f"ALTER TABLE {s} ADD id INT PRIMARY KEY AUTO_INCREMENT FIRST")

db.commit()
