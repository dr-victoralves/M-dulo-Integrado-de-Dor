"""
Pain Data Warehouse
Central repository for all pain management data
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PainDataWarehouse:
    """
    Centralized data warehouse for storing and querying all pain-related data
    including clinical assessments, treatments, outcomes, and research data.
    """

    def __init__(self):
        """Initialize the Pain Data Warehouse."""
        self.patients = {}
        self.clinical_data = []
        self.treatment_data = []
        self.research_data = []
        logger.info("Pain Data Warehouse initialized")

    def register_patient(self, patient_id: str, patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new patient in the warehouse.

        Args:
            patient_id: Unique patient identifier
            patient_info: Patient demographic and clinical information

        Returns:
            Registered patient record
        """
        patient_record = {
            "patient_id": patient_id,
            "registration_date": datetime.now().isoformat(),
            "info": patient_info,
            "status": "active"
        }
        self.patients[patient_id] = patient_record
        logger.info(f"Registered patient {patient_id} in warehouse")
        return patient_record

    def store_clinical_data(self, patient_id: str, data_type: str, data: Dict[str, Any]) -> None:
        """
        Store clinical data for a patient.

        Args:
            patient_id: Unique patient identifier
            data_type: Type of clinical data (assessment, diagnosis, etc.)
            data: Clinical data to store
        """
        record = {
            "patient_id": patient_id,
            "data_type": data_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.clinical_data.append(record)
        logger.info(f"Stored {data_type} data for patient {patient_id}")

    def store_treatment_data(self, patient_id: str, treatment_type: str, data: Dict[str, Any]) -> None:
        """
        Store treatment data for a patient.

        Args:
            patient_id: Unique patient identifier
            treatment_type: Type of treatment
            data: Treatment data to store
        """
        record = {
            "patient_id": patient_id,
            "treatment_type": treatment_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.treatment_data.append(record)
        logger.info(f"Stored {treatment_type} treatment data for patient {patient_id}")

    def query_patient_data(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Query all data for a specific patient.

        Args:
            patient_id: Unique patient identifier

        Returns:
            Comprehensive patient data or None if not found
        """
        if patient_id not in self.patients:
            return None

        patient_clinical = [d for d in self.clinical_data if d["patient_id"] == patient_id]
        patient_treatments = [d for d in self.treatment_data if d["patient_id"] == patient_id]

        return {
            "patient": self.patients[patient_id],
            "clinical_records": patient_clinical,
            "treatment_records": patient_treatments,
            "total_records": len(patient_clinical) + len(patient_treatments)
        }

    def query_by_criteria(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query patients based on specific criteria.

        Args:
            criteria: Search criteria (pain_type, age_range, etc.)

        Returns:
            List of matching patient records
        """
        matching_patients = []

        for patient_id, patient in self.patients.items():
            match = True
            for key, value in criteria.items():
                if key not in patient["info"] or patient["info"][key] != value:
                    match = False
                    break

            if match:
                matching_patients.append(self.query_patient_data(patient_id))

        logger.info(f"Found {len(matching_patients)} patients matching criteria")
        return matching_patients

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get warehouse statistics.

        Returns:
            Statistical summary of warehouse data
        """
        return {
            "total_patients": len(self.patients),
            "total_clinical_records": len(self.clinical_data),
            "total_treatment_records": len(self.treatment_data),
            "total_research_records": len(self.research_data),
            "active_patients": sum(1 for p in self.patients.values() if p["status"] == "active")
        }

    def export_research_dataset(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Export anonymized data for research purposes.

        Args:
            criteria: Optional criteria to filter the dataset

        Returns:
            Anonymized research dataset
        """
        if criteria:
            patients = self.query_by_criteria(criteria)
        else:
            patients = [self.query_patient_data(pid) for pid in self.patients.keys()]

        # Anonymize data by removing identifiable information
        research_dataset = []
        for i, patient_data in enumerate(patients):
            if patient_data:
                anonymized = {
                    "subject_id": f"SUBJ-{i+1:04d}",
                    "clinical_records_count": len(patient_data["clinical_records"]),
                    "treatment_records_count": len(patient_data["treatment_records"])
                }
                research_dataset.append(anonymized)

        logger.info(f"Exported research dataset with {len(research_dataset)} subjects")
        return research_dataset
