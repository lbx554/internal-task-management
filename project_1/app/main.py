# app/main.py -> main application entry point

# Create a FastAPI application instance
# Include routers (users, resources, reservations)
# Wire in middleware (if needed later)
# Setup startup/shutdown events (optional for DB etc...)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import SessionLocal, engine
from app.db.models import user, resource, reservation

from api.v1.routers import users, resources, reservations

# Create database tables if they don't exist
user.Base.metadata.create_all(bind=engine)
resource.Base.metadata.create_all(bind=engine)
reservation.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resource Reservation API", 
    version="1.0.0"
)

# Middleware configuration -> frontend JS can call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(resources.router, prefix="/resources", tags=["resources"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])

# Test route
@app.get("/")
def root():
    return {"message": "Resource Reservation API is running!"}

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()