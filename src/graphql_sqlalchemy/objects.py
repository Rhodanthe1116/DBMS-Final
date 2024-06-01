from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import interfaces
from sqlalchemy.ext.declarative import DeclarativeMeta
from graphql import (
    GraphQLField,
    GraphQLFieldMap,
    GraphQLInt,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLOutputType,
)

from .graphql_types import get_graphql_type_from_column
from .helpers import get_relationships, get_table
from .names import get_model_mutation_response_object_name, get_table_name
from .resolvers import (
    make_dict_resolver,
    make_field_resolver,
)
from .types import Objects


def build_object_type(model: DeclarativeMeta, objects: Objects) -> GraphQLObjectType:
    def get_fields() -> GraphQLFieldMap:
        fields = {}

        for column in get_table(model).columns:
            graphql_type: GraphQLOutputType = get_graphql_type_from_column(column.type)
            if not column.nullable:
                graphql_type = GraphQLNonNull(graphql_type)

            fields[column.name] = GraphQLField(
                graphql_type, resolve=make_field_resolver(column.name)
            )
        for name, relationship in get_relationships(model):
            object_type: GraphQLOutputType = objects[
                get_table_name(relationship.mapper.entity)
            ]
            if relationship.direction in (interfaces.ONETOMANY, interfaces.MANYTOMANY):
                object_type = GraphQLList(object_type)

            fields[name] = GraphQLField(object_type, resolve=make_field_resolver(name))

        return fields

    return GraphQLObjectType(get_table_name(model), get_fields)


def build_sum_fields_object_type(
    model: DeclarativeMeta, objects: Objects
) -> GraphQLObjectType:
    def get_fields() -> GraphQLFieldMap:
        fields = {}

        for column in get_table(model).columns:
            graphql_type: GraphQLOutputType = get_graphql_type_from_column(column.type)
            if isinstance(column.type, (Integer, Float)):
                fields[column.name] = GraphQLField(
                    graphql_type, resolve=make_dict_resolver(column.name)
                )

            # if not column.nullable:
            #     graphql_type = GraphQLNonNull(graphql_type)

        return fields

    return GraphQLObjectType(get_table_name(model) + "_sum_fields", get_fields)


def build_avg_fields_object_type(
    model: DeclarativeMeta, objects: Objects
) -> GraphQLObjectType:
    def get_fields() -> GraphQLFieldMap:
        fields = {}

        for column in get_table(model).columns:
            graphql_type: GraphQLOutputType = get_graphql_type_from_column(column.type)
            if isinstance(column.type, (Integer, Float)):
                fields[column.name] = GraphQLField(
                    graphql_type, resolve=make_dict_resolver(column.name)
                )

            # if not column.nullable:
            #     graphql_type = GraphQLNonNull(graphql_type)

        return fields

    return GraphQLObjectType(get_table_name(model) + "_avg_fields", get_fields)


def build_max_fields_object_type(
    model: DeclarativeMeta, objects: Objects
) -> GraphQLObjectType:
    def get_fields() -> GraphQLFieldMap:
        fields = {}

        for column in get_table(model).columns:
            graphql_type: GraphQLOutputType = get_graphql_type_from_column(column.type)
            if isinstance(column.type, (Integer, Float, String)):
                fields[column.name] = GraphQLField(
                    graphql_type, resolve=make_dict_resolver(column.name)
                )

            # if not column.nullable:
            #     graphql_type = GraphQLNonNull(graphql_type)

        return fields

    return GraphQLObjectType(get_table_name(model) + "_max_fields", get_fields)


def build_aggregate_fields_object_type(
    model: DeclarativeMeta, objects: Objects
) -> GraphQLObjectType:
    def get_fields() -> GraphQLFieldMap:
        fields = {
            "count": GraphQLField(
                GraphQLNonNull(
                    GraphQLInt,
                ),
                resolve=lambda obj, info: obj["count"],
            ),
            "sum": GraphQLField(
                build_sum_fields_object_type(model, objects),
                resolve=lambda obj, info: obj["sum"],
            ),
            "avg": GraphQLField(
                build_avg_fields_object_type(model, objects),
                resolve=lambda obj, info: obj["avg"],
            ),
            "max": GraphQLField(
                build_max_fields_object_type(model, objects),
                resolve=lambda obj, info: obj["max"],
            ),
        }

        return fields

    return GraphQLObjectType(get_table_name(model) + "_aggregate_fields", get_fields)


def build_aggregate_object_type(
    model: DeclarativeMeta, objects: Objects
) -> GraphQLObjectType:
    def get_fields() -> GraphQLFieldMap:
        aggregate_fields = build_aggregate_fields_object_type(model, objects)
        fields = {
            "aggregate": GraphQLField(
                aggregate_fields, resolve=lambda root, info: root["aggregate"]
            ),
            "nodes": GraphQLField(
                GraphQLNonNull(
                    GraphQLList(GraphQLNonNull(objects[get_table_name(model)]))
                ),
                resolve=lambda root, info: root["nodes"],
            ),
        }

        return fields

    return GraphQLObjectType(get_table_name(model) + "_aggregate", get_fields)


def build_mutation_response_type(
    model: DeclarativeMeta, objects: Objects
) -> GraphQLObjectType:
    type_name = get_model_mutation_response_object_name(model)

    object_type = objects[get_table_name(model)]
    fields = {
        "affected_rows": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "returning": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(object_type)))
        ),
    }

    return GraphQLObjectType(type_name, fields)
