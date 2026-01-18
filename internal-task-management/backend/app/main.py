from fastapi import FastAPI
from app.db import base  # Import the base module to ensure models are registered
from app.models import user, task  # Import models to register them with the Base
from app.db.session import engine
from app.api import auth, users, tasks
from app.core.wait_for_db import wait_for_db
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Internal Task Management System")


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    wait_for_db()  # wait for DB
    base.Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# serve frontend (last)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")