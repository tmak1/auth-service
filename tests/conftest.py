import pytest
import sys
import os
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# 1. Add the parent directory to sys.path
# This allows us to import 'main', 'database', and 'User' from the service root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base

# 2. Configure In-Memory SQLite for fast, isolated tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='session')
def test_engine():
    # Create the engine once for the whole test session
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope='function')
def client(test_engine):
    """
    Creates a new database session for a test.
    Rolls back any changes at the end of the test.
    """
    # A. Create tables in the test database
    Base.metadata.create_all(test_engine)
    
    # B. Connect and start a transaction
    connection = test_engine.connect()
    transaction = connection.begin()
    
    # C. Create a Session factory bound to this connection
    TestSession = scoped_session(sessionmaker(bind=connection))
    
    # D. THE FIX: Monkeypatch the 'Session' object inside 'user_routes'
    # This intercepts the database call in your API and redirects it to SQLite.
    # We also patch 'main.Session' just in case you add routes there later.
    with patch('user_routes.Session', TestSession), \
         patch('database.Session', TestSession):
        
        with app.test_client() as client:
            yield client

    # E. Teardown: Rollback transaction and drop tables
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(test_engine)