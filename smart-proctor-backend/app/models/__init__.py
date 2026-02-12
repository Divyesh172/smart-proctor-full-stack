# Import all models here.
# If you add a new model (e.g., 'Course' or 'ExamSession'),
# you MUST import it here, or Alembic won't detect it
# and won't generate the migration script.

from .user import User
from .integrity import IntegrityViolation