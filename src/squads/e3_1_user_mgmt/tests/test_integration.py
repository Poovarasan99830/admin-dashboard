import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app import models

client = TestClient(app)

# Recreate tables for integration tests
@pytest.fixture(autouse=True, scope="function")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_list_users_empty():
    response = client.get("/api/v1/admin/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_suspend_and_restore_user():
    # Create a user directly in DB
    db = SessionLocal()
    user = models.User(name="Integration User", email="int@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    # Suspend user
    suspend_res = client.post(f"/api/v1/admin/users/{user.id}/suspend", json={"reason": "testing"})
    assert suspend_res.status_code == 200
    assert suspend_res.json()["status"] == "suspended"

    # Restore user
    restore_res = client.post(f"/api/v1/admin/users/{user.id}/restore", json={"reason": "manual check"})
    assert restore_res.status_code == 200
    assert restore_res.json()["status"] == "active"

def test_suspend_nonexistent_user():
    response = client.post("/api/v1/admin/users/999/suspend", json={"reason": "fake"})
    assert response.status_code == 409

def test_restore_nonexistent_user():
    response = client.post("/api/v1/admin/users/999/restore", json={"reason": "fake"})
    assert response.status_code == 409
