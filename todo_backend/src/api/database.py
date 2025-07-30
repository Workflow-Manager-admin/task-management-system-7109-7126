import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PUBLIC_INTERFACE
def get_database_url():
    """Return the database URL from environment variable or use SQLite default for development."""
    # Use DATABASE_URL env var, fall back to SQLite for demo/dev
    return os.getenv("DATABASE_URL", "sqlite:///./todos.db")

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PUBLIC_INTERFACE
def get_db():
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
