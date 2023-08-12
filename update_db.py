from db_connection.db_connection import db_connection
from search import SearchDriver
conn=db_connection()
cur=conn.cursor()
#print the name of table and column
cur.execute("SELECT username from public.user")
rows=cur.fetchall()
for row in rows:
    print(row)
location = "Lal Dighi (Pond)/ লাল দিঘী"
print(location)
d = SearchDriver()
d.scrape(location)
d.exit()
cur.close() 
conn.close()