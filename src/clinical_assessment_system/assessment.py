"""
Clinical Assessment Module
Handles patient pain assessments and clinical evaluations
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ClinicalAssessment:
    """
    Manages clinical pain assessments including pain scales,
    functional evaluations, and patient reported outcomes.
    """

    def __init__(self):
        """Initialize the Clinical Assessment System."""
        self.assessments = []
        logger.info("Clinical Assessment System initialized")

    def create_assessment(self, patient_id: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new pain assessment for a patient.

        Args:
            patient_id: Unique patient identifier
            assessment_data: Assessment details including pain scores, location, etc.

        Returns:
            Created assessment with metadata
        """
        assessment = {
            "id": f"ASSESS-{len(self.assessments) + 1}",
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat(),
            "data": assessment_data,
            "status": "completed"
        }
        self.assessments.append(assessment)
        logger.info(f"Created assessment {assessment['id']} for patient {patient_id}")
        return assessment

    def get_patient_assessments(self, patient_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all assessments for a specific patient.

        Args:
            patient_id: Unique patient identifier

        Returns:
            List of assessments for the patient
        """
        return [a for a in self.assessments if a["patient_id"] == patient_id]

    def calculate_pain_score(self, assessment_data: Dict[str, Any]) -> float:
        """
        Calculate comprehensive pain score from assessment data.

        Args:
            assessment_data: Raw assessment data

        Returns:
            Calculated pain score (0-10 scale)
        """
        # Simple calculation - can be enhanced with more sophisticated algorithms
        intensity = assessment_data.get("intensity", 0)
        duration = assessment_data.get("duration_hours", 0)
        interference = assessment_data.get("life_interference", 0)

        score = (intensity * 0.5 + min(duration / 24, 1) * 2 + interference * 0.3)
        return min(score, 10.0)

    def get_assessment_summary(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Get summary statistics for a patient's assessments.

        Args:
            patient_id: Unique patient identifier

        Returns:
            Summary statistics or None if no assessments found
        """
        patient_assessments = self.get_patient_assessments(patient_id)
        if not patient_assessments:
            return None

        pain_scores = [self.calculate_pain_score(a["data"]) for a in patient_assessments]
        return {
            "patient_id": patient_id,
            "total_assessments": len(patient_assessments),
            "average_pain_score": sum(pain_scores) / len(pain_scores),
            "max_pain_score": max(pain_scores),
            "min_pain_score": min(pain_scores),
            "latest_assessment": patient_assessments[-1]["timestamp"]
        }
