from sqlalchemy.orm import Session
from core.models import LivenessResult
from core.logging_config import logger
from typing import Optional


class LivenessDbService:
    @staticmethod
    def create_liveness_result(
        db: Session,
        session_id: str,
        confidence: Optional[float] = None,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        face_id: Optional[str] = None,
        image_id: Optional[str] = None,
        image_url: Optional[str] = None,
        recognition_confidence: Optional[float] = None,
        similarity: Optional[float] = None,
        match_count: Optional[int] = None,
    ) -> LivenessResult:
        """Create a new liveness result record in the database."""
        try:
            liveness_result = LivenessResult(
                session_id=session_id,
                confidence=confidence,
                status=status or "FAILED",
                user_id=user_id,
                face_id=face_id,
                image_id=image_id,
                image_url=image_url,
                recognition_confidence=recognition_confidence,
                similarity=similarity,
                match_count=match_count,
            )
            db.add(liveness_result)
            db.commit()
            db.refresh(liveness_result)
            logger.info(f"Stored liveness result for session {session_id}")
            return liveness_result
        except Exception as e:
            db.rollback()
            logger.error(
                f"Failed to store liveness result for session {session_id}: {str(e)}"
            )
            raise
