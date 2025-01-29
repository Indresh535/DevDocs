from fastapi import FastAPI
from app.routes import events

app = FastAPI()

# Include the event routes
app.include_router(events.router, prefix="/api/events")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
