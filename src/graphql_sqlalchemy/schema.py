from graphql import GraphQLField, GraphQLFieldMap, GraphQLList, GraphQLNonNull, GraphQLObjectType, GraphQLSchema, validate_schema
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta

from .args import (
    make_args,
    make_delete_args,
    make_insert_args,
    make_insert_one_args,
    make_pk_args,
    make_update_args,
    make_update_by_pk_args,
)
from .helpers import get_table
from .names import (
    get_model_delete_by_pk_name,
    get_model_delete_name,
    get_model_insert_object_name,
    get_model_insert_one_object_name,
    get_model_pk_field_name,
    get_model_update_by_pk_name,
    get_model_update_name,
    get_table_name,
)
from .objects import build_aggregate_object_type, build_mutation_response_type, build_object_type
from .resolvers import (
    make_delete_by_pk_resolver,
    make_delete_resolver,
    make_insert_one_resolver,
    make_insert_resolver,
    make_object_aggregate_resolver,
    make_object_resolver,
    make_pk_resolver,
    make_update_by_pk_resolver,
    make_update_resolver,
)
from .types import Inputs, Objects

from sqlalchemy.ext.automap import automap_base

def build_queries(model: DeclarativeMeta, objects: Objects, queries: GraphQLFieldMap, inputs: Inputs) -> None:
    object_type = build_object_type(model, objects)

    objects[object_type.name] = object_type

    filter_args = make_args(model, inputs=inputs)

    queries[object_type.name] = GraphQLField(
        GraphQLNonNull(GraphQLList(GraphQLNonNull(object_type))),
        args=filter_args,
        resolve=make_object_resolver(model),
    )

    aggregate_object_type = build_aggregate_object_type(model, objects)
    queries[aggregate_object_type.name] = GraphQLField(
        GraphQLNonNull(aggregate_object_type),
        args=filter_args,
        resolve=make_object_aggregate_resolver(model),
    )

    if get_table(model).primary_key:
        pk_field_name = get_model_pk_field_name(model)
        queries[pk_field_name] = GraphQLField(object_type, args=make_pk_args(model), resolve=make_pk_resolver(model))


def build_mutations(model: DeclarativeMeta, objects: Objects, mutations: GraphQLFieldMap, inputs: Inputs) -> None:
    mutation_response_type = build_mutation_response_type(model, objects)
    object_type = objects[get_table_name(model)]

    insert_type_name = get_model_insert_object_name(model)
    mutations[insert_type_name] = GraphQLField(
        mutation_response_type, args=make_insert_args(model, inputs), resolve=make_insert_resolver(model)
    )

    insert_one_type_name = get_model_insert_one_object_name(model)
    mutations[insert_one_type_name] = GraphQLField(
        object_type, args=make_insert_one_args(model, inputs), resolve=make_insert_one_resolver(model)
    )

    delete_type_name = get_model_delete_name(model)
    mutations[delete_type_name] = GraphQLField(
        mutation_response_type, args=make_delete_args(model, inputs), resolve=make_delete_resolver(model)
    )

    update_type_name = get_model_update_name(model)
    mutations[update_type_name] = GraphQLField(
        mutation_response_type, args=make_update_args(model, inputs), resolve=make_update_resolver(model)
    )

    if get_table(model).primary_key:
        delete_by_pk_type_name = get_model_delete_by_pk_name(model)
        mutations[delete_by_pk_type_name] = GraphQLField(
            object_type, args=make_pk_args(model), resolve=make_delete_by_pk_resolver(model)
        )

        update_by_pk_type_name = get_model_update_by_pk_name(model)
        mutations[update_by_pk_type_name] = GraphQLField(
            object_type, args=make_update_by_pk_args(model, inputs), resolve=make_update_by_pk_resolver(model)
        )


def build_schema(base: DeclarativeMeta, enable_subscription: bool = False) -> GraphQLSchema:
    """

    Args:
        base:
        enable_subscription:

    Returns: :class:`graphql:graphql.type.GraphQLSchema`

    """
    queries: GraphQLFieldMap = {}
    mutations: GraphQLFieldMap = {}

    objects: Objects = {}
    inputs: Inputs = {}

    for model in base.__subclasses__():
        build_queries(model, objects, queries, inputs)
        build_mutations(model, objects, mutations, inputs)

    return GraphQLSchema(
        GraphQLObjectType("Query", queries),
        GraphQLObjectType("Mutation", mutations),
        GraphQLObjectType("Subscription", {}) if enable_subscription else None,
    )


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

    Base = automap_base()
    Base.prepare(autoload_with=engine)

    schema = build_schema(Base)

    errors = validate_schema(schema)
    if errors:
        formatted_errors = "\n\n".join(f"❌ {error.message}" for error in errors)
        raise ValueError(f"Invalid Schema. Errors:\n\n{formatted_errors}")

    return schema
