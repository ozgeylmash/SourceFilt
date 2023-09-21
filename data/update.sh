source .env
export PATH=${PATH}:/usr/local/mysql/bin/

mysql -h "localhost" --user="root" --password=${PASSWORD} "library" < "create_source.sql"

for f in scrapers/*.py; do source_env/bin/python3.11  "$f"; done

mysql -h "localhost" --user="root" --password=${PASSWORD} "library" < "create_book.sql"

source_env/bin/python3.11 book.py

mysql -h "localhost" --user="root" --password=${PASSWORD} "library" < "finalize_source.sql"