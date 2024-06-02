from fastapi import Depends, FastAPI, Request
from sqlalchemy import create_engine
from starlette.middleware.cors import CORSMiddleware
from ariadne.asgi import GraphQL
from sqlalchemy.orm import sessionmaker
from .graphql_sqlalchemy import build_schema_from_db_config

# from .builders.schema import (
#     build_schema_from_db_config,
# )
from .db_config import db_config
import logging

logging.basicConfig(format="%(message)s\n")
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)



engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['db_name']}?charset=utf8mb4",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_context_value(request_or_ws: Request, _data) -> dict:
    return {
        "request": request_or_ws,
        "session": request_or_ws.scope["session"],
    }


def setup_routers(app: FastAPI, graphql_app: GraphQL):
    app.add_route("/graphql/", graphql_app, methods=["GET", "POST", "OPTIONS"])


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    schema = build_schema_from_db_config(**db_config)
    graphql_app = GraphQL(schema, debug=True, context_value=get_context_value)
    # setup_routers(app, graphql_app)

    # app.add_route("/graphql/", handle_graphql_query, methods=["POST"])
    # app.add_route("/graphql/", handle_graphql_explorer, methods=["GET", "OPTIONS"])
    return app, graphql_app


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app, graphql_app = create_app()


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
