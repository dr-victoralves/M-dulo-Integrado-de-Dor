"""
Tests for Clinical Assessment System
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from clinical_assessment_system import ClinicalAssessment


def test_assessment_initialization():
    """Test assessment system initialization."""
    assessment = ClinicalAssessment()
    assert assessment.assessments == []


def test_create_assessment():
    """Test creating a pain assessment."""
    assessment = ClinicalAssessment()
    
    patient_id = "PAT-001"
    assessment_data = {
        "intensity": 7,
        "duration_hours": 24,
        "life_interference": 6
    }
    
    result = assessment.create_assessment(patient_id, assessment_data)
    
    assert result["patient_id"] == patient_id
    assert result["status"] == "completed"
    assert "id" in result
    assert "timestamp" in result


def test_calculate_pain_score():
    """Test pain score calculation."""
    assessment = ClinicalAssessment()
    
    assessment_data = {
        "intensity": 8,
        "duration_hours": 48,
        "life_interference": 7
    }
    
    score = assessment.calculate_pain_score(assessment_data)
    
    assert 0 <= score <= 10
    assert score > 0  # Should be positive given the inputs


def test_get_patient_assessments():
    """Test retrieving patient assessments."""
    assessment = ClinicalAssessment()
    
    patient_id = "PAT-001"
    
    # Create multiple assessments
    for i in range(3):
        assessment.create_assessment(patient_id, {"intensity": i + 5})
    
    patient_assessments = assessment.get_patient_assessments(patient_id)
    
    assert len(patient_assessments) == 3
    assert all(a["patient_id"] == patient_id for a in patient_assessments)


def test_assessment_summary():
    """Test getting assessment summary."""
    assessment = ClinicalAssessment()
    
    patient_id = "PAT-001"
    
    # Create assessments
    for intensity in [5, 6, 7]:
        assessment.create_assessment(patient_id, {
            "intensity": intensity,
            "duration_hours": 24,
            "life_interference": 5
        })
    
    summary = assessment.get_assessment_summary(patient_id)
    
    assert summary is not None
    assert summary["patient_id"] == patient_id
    assert summary["total_assessments"] == 3
    assert "average_pain_score" in summary
