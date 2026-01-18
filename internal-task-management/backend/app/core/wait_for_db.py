import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.db.session import DATABASE_URL

def wait_for_db():
    engine = create_engine(DATABASE_URL)
    retries = 10
    while retries > 0:
        try:
            conn = engine.connect()
            conn.close()
            print("Database is ready!")
            return
        except OperationalError:
            retries -= 1
            print("Database not ready, waiting 2s...")
            time.sleep(2)
    raise Exception("Database connection failed after retries")
