# db/session.py -> creates the database engine and provides a safe way tp open and close DB sessions

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from app.db.base import Base
from app.db.models import reservation, user, resource  # import all models

# Engine & session
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

