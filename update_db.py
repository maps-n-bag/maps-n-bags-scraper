from db_connection.db_connection import db_connection
conn=db_connection()
cur=conn.cursor()
#print the name of table and column
cur.execute("SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = 'public'")
rows=cur.fetchall()
for row in rows:
    print(row)
cur.close() 
conn.close()