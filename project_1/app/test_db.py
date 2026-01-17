from db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    results = db.execute(text("SELECT 1"))
    print("Database connection successful:", results.scalar())
finally:
    db.close()