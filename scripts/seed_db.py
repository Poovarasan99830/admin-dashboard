from src.common.database import SessionLocal, Base, engine
from src.models.disputes import User

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add sample users
users = [
    User(name="John Doe", email="john@example.com", status="active"),
    User(name="Alice", email="alice@example.com", status="suspended"),
    User(name="Bob Smith", email="bob@example.com", status="active")
]

db.add_all(users)
db.commit()
db.close()

print("✅ Seed data inserted!")




