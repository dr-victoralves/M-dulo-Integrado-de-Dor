"""
Research Protocols
Manages clinical research protocols for pain studies
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResearchProtocols:
    """
    Manages research protocols, study designs, data collection,
    and analysis for pain-related clinical research.
    """

    def __init__(self):
        """Initialize the Research Protocols system."""
        self.protocols = {}
        self.studies = {}
        logger.info("Research Protocols system initialized")

    def create_protocol(self, protocol_id: str, protocol_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new research protocol.

        Args:
            protocol_id: Unique protocol identifier
            protocol_details: Protocol specifications and details

        Returns:
            Created protocol record

        Raises:
            ValueError: If the protocol identifier already exists.
        """
        if protocol_id in self.protocols:
            raise ValueError(f"Protocol {protocol_id} already exists")

        protocol = {
            "protocol_id": protocol_id,
            "title": protocol_details.get("title", ""),
            "objective": protocol_details.get("objective", ""),
            "design": protocol_details.get("design", "observational"),
            "inclusion_criteria": protocol_details.get("inclusion_criteria", []),
            "exclusion_criteria": protocol_details.get("exclusion_criteria", []),
            "data_collection_points": protocol_details.get("data_collection_points", []),
            "status": "draft",
            "created_date": datetime.now().isoformat()
        }
        self.protocols[protocol_id] = protocol
        logger.info(f"Created research protocol {protocol_id}")
        return protocol

    def activate_protocol(self, protocol_id: str) -> bool:
        """
        Activate a research protocol for enrollment.

        Args:
            protocol_id: Unique protocol identifier

        Returns:
            True if activated successfully, False otherwise
        """
        if protocol_id not in self.protocols:
            return False

        self.protocols[protocol_id]["status"] = "active"
        self.protocols[protocol_id]["activation_date"] = datetime.now().isoformat()
        logger.info(f"Activated research protocol {protocol_id}")
        return True

    def enroll_participant(self, protocol_id: str, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Enroll a participant in a research protocol.

        Args:
            protocol_id: Unique protocol identifier
            patient_id: Unique patient identifier

        Returns:
            Enrollment record or None if enrollment failed
        """
        if protocol_id not in self.protocols:
            return None

        if protocol_id not in self.studies:
            self.studies[protocol_id] = {"participants": [], "data": []}

        enrollment = {
            "patient_id": patient_id,
            "protocol_id": protocol_id,
            "enrollment_date": datetime.now().isoformat(),
            "status": "active",
            "compliance_score": 100.0
        }
        self.studies[protocol_id]["participants"].append(enrollment)
        logger.info(f"Enrolled patient {patient_id} in protocol {protocol_id}")
        return enrollment

    def collect_study_data(self, protocol_id: str, patient_id: str, 
                          data_point: str, data: Dict[str, Any]) -> None:
        """
        Collect data for a study participant.

        Args:
            protocol_id: Unique protocol identifier
            patient_id: Unique patient identifier
            data_point: Type of data being collected
            data: Collected data

        Raises:
            ValueError: If the patient is not enrolled in this study.
        """
        if protocol_id not in self.studies:
            logger.warning(f"Protocol {protocol_id} not found for data collection")
            return

        if not any(
            participant["patient_id"] == patient_id
            for participant in self.studies[protocol_id]["participants"]
        ):
            raise ValueError(f"Patient {patient_id} is not enrolled in protocol {protocol_id}")

        data_record = {
            "patient_id": patient_id,
            "data_point": data_point,
            "data": data,
            "collection_date": datetime.now().isoformat()
        }
        self.studies[protocol_id]["data"].append(data_record)
        logger.info(f"Collected {data_point} data for patient {patient_id} in protocol {protocol_id}")

    def get_protocol_status(self, protocol_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current status and statistics of a research protocol.

        Args:
            protocol_id: Unique protocol identifier

        Returns:
            Protocol status information or None if not found
        """
        if protocol_id not in self.protocols:
            return None

        protocol = self.protocols[protocol_id]
        study_data = self.studies.get(protocol_id, {"participants": [], "data": []})

        return {
            "protocol_id": protocol_id,
            "title": protocol["title"],
            "status": protocol["status"],
            "total_participants": len(study_data["participants"]),
            "active_participants": sum(1 for p in study_data["participants"] if p["status"] == "active"),
            "data_points_collected": len(study_data["data"]),
            "completion_rate": self._calculate_completion_rate(protocol_id)
        }

    def _calculate_completion_rate(self, protocol_id: str) -> float:
        """
        Calculate study completion rate.

        Args:
            protocol_id: Unique protocol identifier

        Returns:
            Completion rate as percentage
        """
        if protocol_id not in self.studies:
            return 0.0

        study = self.studies[protocol_id]
        if not study["participants"]:
            return 0.0

        completed = sum(1 for p in study["participants"] if p["status"] == "completed")
        return (completed / len(study["participants"])) * 100

    def analyze_protocol_data(self, protocol_id: str) -> Optional[Dict[str, Any]]:
        """
        Analyze data collected for a protocol.

        Args:
            protocol_id: Unique protocol identifier

        Returns:
            Analysis results or None if insufficient data
        """
        if protocol_id not in self.studies:
            return None

        study_data = self.studies[protocol_id]
        if not study_data["data"]:
            return None

        analysis = {
            "protocol_id": protocol_id,
            "total_data_points": len(study_data["data"]),
            "data_types": list(set(d["data_point"] for d in study_data["data"])),
            "participants_with_data": len(set(d["patient_id"] for d in study_data["data"])),
            "analysis_date": datetime.now().isoformat()
        }

        logger.info(f"Analyzed data for protocol {protocol_id}")
        return analysis

    def export_study_results(self, protocol_id: str) -> Optional[Dict[str, Any]]:
        """
        Export study results for publication or reporting.

        Args:
            protocol_id: Unique protocol identifier

        Returns:
            Exported study results or None if not available
        """
        if protocol_id not in self.protocols:
            return None

        protocol = self.protocols[protocol_id]
        status = self.get_protocol_status(protocol_id)
        analysis = self.analyze_protocol_data(protocol_id)

        results = {
            "protocol": protocol,
            "status": status,
            "analysis": analysis,
            "export_date": datetime.now().isoformat()
        }

        logger.info(f"Exported results for protocol {protocol_id}")
        return results
