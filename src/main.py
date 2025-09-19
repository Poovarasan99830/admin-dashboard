from fastapi import FastAPI
from src.common.logger import logger
from src.common.database import engine, Base
from src.squads.e3_2_marketplace import routes as marketplace_routes
from src.config.settings import settings

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # include routers
    app.include_router(marketplace_routes.router)

    @app.on_event("startup")
    def on_startup():
        logger.info("Starting %s", settings.APP_NAME)
        # Create tables for demo purposes (in production, use Alembic migrations)
        Base.metadata.create_all(bind=engine)
        logger.info("DB tables created/checked")

    @app.on_event("shutdown")
    def on_shutdown():
        logger.info("Shutting down")

    return app

app = create_app()
