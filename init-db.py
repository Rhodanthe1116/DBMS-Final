import mysql.connector
from db_config import db_config

dbname = db_config["db_name"]

cnx = mysql.connector.connect(
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    database=dbname,
)
with cnx.cursor() as cursor:
    # excute sample.sql
    with open("sample.sql") as f:
        sql = f.read()
        cursor.execute(sql)


cnx.close()
