from fastapi import FastAPI
from src.squads.e3_5_analytics import routes as analytics_routes

app = FastAPI(title="Admin Dashboard Service")

# include analytics squad endpoints
app.include_router(analytics_routes.router)

@app.get("/")
def root():
    return {"status": "Admin Dashboard Service running"}
