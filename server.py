from fastapi import FastAPI
from fastapi.responses import JSONResponse
from graphql import graphql_sync
from starlette.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL

from .builders.schema import (
    build_schema_from_db_config,
)
from .db_config import db_config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# schema = strawberry.Schema(gql_schema)

# print(schema)
# graphql_app = GraphQLRouter(schema)
# app.include_router(graphql_app, prefix="/graphql")


# Route to handle GraphQL queries
schema = build_schema_from_db_config(**db_config)

app.mount("/graphql/", GraphQL(schema, debug=True))
