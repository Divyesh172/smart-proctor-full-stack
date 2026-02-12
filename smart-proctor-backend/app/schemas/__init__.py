# Authentication DTOs
from .token import Token, TokenPayload

# User/Student DTOs
from .student import Student, StudentCreate

# Exam & Integrity DTOs
from .exam import ExamSubmission, ExamResult

# This allows: "from app.schemas import Token, Student, ExamSubmission"