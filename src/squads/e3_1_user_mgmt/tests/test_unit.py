import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.common.database import Base
from src.models.disputes import User
from src.squads.e3_1_user_mgmt import service, schema

# Use in-memory SQLite for unit tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_list_users_empty(db):
    users, total = service.list_users(db)
    assert users == []
    assert total == 0

def test_suspend_and_restore_user(db):
    # Create a user
    user = User(name="John Doe", email="john@example.com", status="active")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Suspend
    request = schema.ActionRequest(reason="violation")
    suspended_user = service.suspend_user(db, user.id, admin_id=1, data=request)
    assert suspended_user.status == "suspended"

    # Restore
    request = schema.ActionRequest(reason="manual review")
    restored_user = service.restore_user(db, user.id, admin_id=1, data=request)
    assert restored_user.status == "active"

def test_suspend_nonexistent_user(db):
    request = schema.ActionRequest(reason="test")
    with pytest.raises(Exception):
        service.suspend_user(db, user_id=999, admin_id=1, data=request)

def test_restore_conflict(db):
    # Create user (already active)
    user = User(name="Jane Doe", email="jane@example.com", status="active")
    db.add(user)
    db.commit()
    db.refresh(user)

    request = schema.ActionRequest(reason="invalid")
    with pytest.raises(Exception):
        service.restore_user(db, user.id, admin_id=1, data=request)



























# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.database import Base
# from app import service, models

# # Setup in-memory database for unit tests
# SQLALCHEMY_TEST_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()
#     Base.metadata.drop_all(bind=engine)

# def test_suspend_user(db):
#     user = models.User(name="Test User", email="test@example.com")
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     result = service.suspend_user(db, user.id, admin_id=1)
#     assert result.status == "suspended"

# def test_restore_user(db):
#     user = models.User(name="Test User", email="test2@example.com", status="suspended")
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     result = service.restore_user(db, user.id, admin_id=1)
#     assert result.status == "active"

# def test_suspend_nonexistent_user(db):
#     result = service.suspend_user(db, 999, admin_id=1)
#     assert result is None

# def test_restore_nonexistent_user(db):
#     result = service.restore_user(db, 999, admin_id=1)
#     assert result is None
