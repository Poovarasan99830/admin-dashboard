from fastapi import FastAPI
from src.squads.e3_3_services import routes as services_routes

app = FastAPI(title="Admin Dashboard Service", version="1.0.0")

# Register squad routers
app.include_router(services_routes.router)
