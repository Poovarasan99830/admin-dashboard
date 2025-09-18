import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import service, models

# Setup in-memory database for unit tests
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_suspend_user(db):
    user = models.User(name="Test User", email="test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    result = service.suspend_user(db, user.id, admin_id=1)
    assert result.status == "suspended"

def test_restore_user(db):
    user = models.User(name="Test User", email="test2@example.com", status="suspended")
    db.add(user)
    db.commit()
    db.refresh(user)

    result = service.restore_user(db, user.id, admin_id=1)
    assert result.status == "active"

def test_suspend_nonexistent_user(db):
    result = service.suspend_user(db, 999, admin_id=1)
    assert result is None

def test_restore_nonexistent_user(db):
    result = service.restore_user(db, 999, admin_id=1)
    assert result is None
