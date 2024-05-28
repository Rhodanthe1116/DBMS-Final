from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import (
    GraphQLField,
    GraphQLList,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    ThunkMapping,
    validate_schema,
)
from sqlalchemy import Table, create_engine, MetaData, Engine
from sqlalchemy.orm import sessionmaker

from ..utils import format_type_name


def build_schema(engine: Engine) -> GraphQLSchema:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    models = {}
    associations = []

    # get all tables
    tables = metadata.tables
    table_names = metadata.tables.keys()

    # Print the table names
    for table_name in table_names:
        print(table_name)

    # for table_name in table_names:
    #     table = Table(table_name, metadata, autoload_with=engine)
    #     models[table_name] = table

    # inspector = inspect(engine)
    # foreign_keys = inspector.get_foreign_keys(table_name)

    # if is_join_table(table, engine.table_names()):
    #     associations.extend(join_table_associations(table, foreign_keys))
    # else:
    #     associations.extend(table_associations(table, foreign_keys))

    types = {}
    mutations = {}
    queries: ThunkMapping[GraphQLField] = {}

    for table_name in table_names:
        table = tables[table_name]
        model = SQLAlchemyObjectType()

        # entity type, ex: Post
        object_type = GraphQLObjectType(
            name=format_type_name(table_name),
            fields=lambda: {
                # should handle mysql type
                column.name: GraphQLField(
                    GraphQLString, resolve=lambda obj, info: obj[column.name]
                )
                for column in tables[table_name].columns
                # should handle relation
            },
        )
        # get many, ex: posts
        queries[table_name] = GraphQLField(
            GraphQLList(object_type),
            # how to get db session and query all in Table?
            resolve=lambda obj, info: print(obj, info),
        )

        # {
        #     type: new GraphQLList(type),
        #     args: defaultListArgs(model),
        #     resolve: resolver(model),
        #   };

    query = GraphQLObjectType("Query", queries)
    schema = GraphQLSchema(query=query)

    errors = validate_schema(schema)
    if errors:
        formatted_errors = "\n\n".join(f"❌ {error.message}" for error in errors)
        raise ValueError(f"Invalid Schema. Errors:\n\n{formatted_errors}")

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

    return build_schema(engine)


def build_schema_from_infile():
    pass


def build_schema_from_database():
    pass
