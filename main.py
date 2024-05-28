import mysql.connector

cnx = mysql.connector.connect(user='mysql', password='mysql',
                              host='127.0.0.1')
cnx.close()