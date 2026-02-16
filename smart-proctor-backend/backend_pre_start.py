import logging
import sys
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # [DEBUG] Print connection details to logs
        db_url = str(settings.SQLALCHEMY_DATABASE_URI)
        # Mask password for security in logs
        safe_url = db_url.replace(settings.POSTGRES_PASSWORD, "******")
        logger.info(f"Attempting connection to: {safe_url}")

        db = SessionLocal()
        # Try to execute a simple query to check connection
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Connection successful!")
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        raise e

def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")

if __name__ == "__main__":
    main()