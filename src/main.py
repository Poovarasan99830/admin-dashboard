from fastapi import FastAPI
from src.config.settings import settings
from src.squads.e3_1_user_mgmt import routes as user_routes
from src.common.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Routers
app.include_router(user_routes.router, prefix=settings.API_V1_PREFIX)

