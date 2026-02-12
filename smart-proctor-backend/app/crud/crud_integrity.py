from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.integrity import IntegrityViolation
from app.schemas.exam import IntegrityCreate, IntegrityUpdate
# You will need to ensure these Schemas exist in the next step

class CRUDIntegrity(CRUDBase[IntegrityViolation, IntegrityCreate, IntegrityUpdate]):
    def create_violation(
            self,
            db: Session,
            *,
            student_id: int,
            violation_type: str,
            evidence_score: float,
            metadata_log: str
    ) -> IntegrityViolation:
        """
        Custom create method for system-generated violations.
        """
        db_obj = IntegrityViolation(
            student_id=student_id,
            violation_type=violation_type,
            evidence_score=evidence_score,
            metadata_log=metadata_log
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_student(
            self, db: Session, *, student_id: int, skip: int = 0, limit: int = 100
    ) -> List[IntegrityViolation]:
        """
        Get all violations for a specific student.
        """
        return (
            db.query(IntegrityViolation)
            .filter(IntegrityViolation.student_id == student_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Instantiate the CRUD object
integrity = CRUDIntegrity(IntegrityViolation)