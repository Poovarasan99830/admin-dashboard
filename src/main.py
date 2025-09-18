from fastapi import FastAPI
from src.squads.e3_4_payments import routes as payments_routes

app = FastAPI(title="Admin Dashboard Service")

app.include_router(payments_routes.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
