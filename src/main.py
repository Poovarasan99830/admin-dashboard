from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.common.database import engine, Base  
app = FastAPI()

# Create tables (only for dev; in prod use Alembic migrations)
Base.metadata.create_all(bind=engine)

# --- Token route ---
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # For now we just return a fixed token
    return {"access_token": "admin-token", "token_type": "bearer"}


# --- Import your squad routes AFTER app is created ---
from src.squads.e3_5_analytics import routes as analytics_routes
app.include_router(analytics_routes.router, prefix="/api/v1/admin", tags=["analytics"])



