from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from graphql import graphql_sync, validate_schema
from sqlalchemy import create_engine
from starlette.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .src.graphql_sqlalchemy import build_schema


from .builders.schema import (
    build_schema_from_db_config,
)
from .db_config import db_config

engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['db_name']}?charset=utf8mb4",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
# schema = build_schema_from_db_config(**db_config)
schema = build_schema(Base)
print(schema)
errors = validate_schema(schema)
if errors:
    formatted_errors = "\n\n".join(f"❌ {error.message}" for error in errors)
    raise ValueError(f"Invalid Schema. Errors:\n\n{formatted_errors}")

def get_context_value(request_or_ws: Request, _data) -> dict:
    return {
        "request": request_or_ws,
        "session": request_or_ws.scope["session"],
    }


# Create GraphQL App instance
graphql_app = GraphQL(
    schema,
    debug=True,
    context_value=get_context_value,
)


# Handle GET requests to serve GraphQL explorer
# Handle OPTIONS requests for CORS
@app.get("/graphql/")
@app.options("/graphql/")
async def handle_graphql_explorer(request: Request):
    return await graphql_app.handle_request(request)


# Handle POST requests to execute GraphQL queries
@app.post("/graphql/")
async def handle_graphql_query(
    request: Request,
    db=Depends(get_db),
):
    # Expose database connection to the GraphQL through request's scope
    request.scope["session"] = db
    return await graphql_app.handle_request(request)
