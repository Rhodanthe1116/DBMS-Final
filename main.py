import mysql.connector

dbuser = 'root'
dbpassword = 'mysql'
dbhost = 'localhost'
dbname = 'mydb'

cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)
with cnx.cursor() as cursor:

    result = cursor.execute(f'''
SELECT table_name FROM information_schema.tables
WHERE table_schema = '{dbname}';
''')

    rows = cursor.fetchall()

    for rows in rows:

        print(rows)

cnx.close()