from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# ---------------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------------
# We create the engine with 'pool_pre_ping=True'.
# This is a Production Best Practice: It checks if the DB connection
# is alive before trying to use it, preventing "Stale Connection" errors
# that plague Python apps in the cloud.
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    pool_size=20,  # Handle 20 concurrent connections
    max_overflow=10 # Allow bursts up to 30
)

# ---------------------------------------------------------
# SESSION FACTORY
# ---------------------------------------------------------
# This factory creates new database sessions for every request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)