from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from .builders.schema import (
    build_schema,
)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = build_schema()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

