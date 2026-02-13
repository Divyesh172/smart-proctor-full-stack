from .token import Token, TokenPayload
from .student import Student, StudentCreate, StudentUpdate
# ADD KeystrokeUpdate to the end of this list 👇
from .exam import ExamSubmission, ExamResult, IntegrityLog, IntegrityCreate, IntegrityUpdate, KeystrokeUpdate

# ---------------------------------------------------------
# ALIASES (CRITICAL FIX)
# ---------------------------------------------------------
# The API endpoints in 'users.py' and 'admin.py' refer to 'schemas.User'.
# We map the 'Student' schemas to 'User' here so the code finds them.
User = Student
UserCreate = StudentCreate
UserUpdate = StudentUpdate