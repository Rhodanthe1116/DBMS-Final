import strawberry
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@strawberry.type
class GenericResponse:
    success: bool


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)


def build_schema(metadata: MetaData) -> strawberry.Schema:
    # get all tables
    table_names = metadata.tables.keys()

    # Print the table names
    for table_name in table_names:
        print(table_name)


    return schema


def build_schema_from_db_config(
    host: str = None,
    port: int = None,
    user: str = None,
    password: str = None,
    db_name: str = None,
):
    # connect mysql db using sqlalchemy create_engine
    engine = create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}?charset=utf8mb4",
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return build_schema(metadata)


def build_schema_from_infile():
    pass


def build_schema_from_database():
    pass
