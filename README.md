## Database initialization
Use [sakila](https://dev.mysql.com/doc/sakila/en/) as test_db.

Import the sample data into the database with the following command:

```bash
python init_db.py --mode execute --sqlpath ./test_db/baseballdb.sql
```
To check whether schema and data successfully loaded in database, run
```bash
python init_db.py --mode check
```

## Running Server 
Start the server with the following command:

```bash
fastapi dev server.py
```

Then open your browser and go to [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)