import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker, DeclarativeBase
from ..server import create_app, engine,SessionLocal

app, graphql_app = create_app()



@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client

class Base(DeclarativeBase):
    pass    



@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db_session: Session = SessionLocal()
        yield db_session
    finally:
        db_session.close()
