# tests/conftest.py
import sys, os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv(dotenv_path=".env.test")
TEST_DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    return sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session(engine, TestingSessionLocal):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db

    class AuthorizedClient(TestClient):
        def request(self, method, url, **kwargs):
            headers = kwargs.pop("headers", {}) or {}
            headers.setdefault("X-API-Key", API_KEY)
            return super().request(method, url, headers=headers, **kwargs)

    return AuthorizedClient(app)
