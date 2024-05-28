import mysql.connector

dbuser = 'root'
dbpassword = 'mysql'
dbhost = 'localhost'
dbname = 'mydb'

cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost)
with cnx.cursor() as cursor:
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {dbname} ;')
    cursor.execute(f'USE {dbname};')

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS test1 (
    column1 int
);''')
    
    
    result = cursor.execute(f'''
SELECT table_name FROM information_schema.tables
WHERE table_schema = '{dbname}';
''')

    rows = cursor.fetchall()

    for rows in rows:

        print(rows)

cnx.close()