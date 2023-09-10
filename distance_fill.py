from db_connection.db_connection import db_connection
# from search import SearchDriver
conn=db_connection()
cur=conn.cursor()
prev_place_list=[1,2,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,30,31,32,33]
new_place_list=[61,62,64,65,66,67,68,69,70,71,72,73]
for i in new_place_list:
    for j in prev_place_list:
        query="""
        INSERT INTO public.distance(first_place_id, second_place_id, distance,est_time,journey_type) VALUES (%s,%s,%s,%s,%s)"""
        cur.execute(query,(i,j,0,0,'car'))
        conn.commit()
    temp_list=new_place_list[new_place_list.index(i)+1:]
    for j in temp_list:
        query="""
        INSERT INTO public.distance(first_place_id, second_place_id, distance,est_time,journey_type) VALUES (%s,%s,%s,%s,%s)"""
        cur.execute(query,(i,j,0,0,'car'))
        conn.commit()

cur.close()
conn.close()