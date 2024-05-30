import mysql.connector
from db_config import db_config
import argparse

dbname = db_config["db_name"]
cnx = mysql.connector.connect(
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    # database=dbname,
)


def execute_sql_file(filename):
    with cnx.cursor() as cursor:

        with open(filename) as f:
            sql = f.read()
            result = cursor.execute(sql)
            rows = cursor.fetchall()
    cnx.close()

def check_sqlfile_success():
    with cnx.cursor() as cursor:   
        try: 
            print("Checking database schema")
            cursor.execute(f'USE {dbname};')
            cursor.execute(f'''
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = '{dbname}';
            ''')
            rows = cursor.fetchall()
            if rows == []:
                raise Exception("Database schema not found")
            print(rows)
        except:
            print("Database schema not found")
            print("Please run the sql file to create the database schema")
            cnx.close()
            return
        try:
            print("Checking data in database")
            cursor.execute(f'''
                select * from category;
            ''')
            rows = cursor.fetchall()
            if rows == []:
                raise Exception("Data not found in database")
            print(rows)
        except:
            print("Data not found in database")
            print("Please run the sql file to insert data into the database")
            cnx.close()
            return
    cnx.close()


def main():
    parser = argparse.ArgumentParser()
    # './test_db/sakila-mv-schema.sql', './test_db/sakila-mv-data.sql'
    parser.add_argument("--mode", type=str, default='check', help='check or execute sql', choices=['check', 'execute'])
    parser.add_argument("--sqlpath", help="sql file path to execute")

    args = parser.parse_args()
    if args.mode == 'execute':
        print(f"Database initializing through {args.sqlpath}.")
        execute_sql_file(args.sqlpath)
    else:
        print("Checking database schema and data")
        check_sqlfile_success()


if __name__ == "__main__":
    main()    
