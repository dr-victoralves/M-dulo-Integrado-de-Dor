"""
Lifestyle and Biomarker Analytics
Analyzes lifestyle factors and biomarkers to understand pain patterns
"""

from typing import Dict, Any, List, Optional
import logging
from math import fsum, isfinite, sqrt

logger = logging.getLogger(__name__)


class LifestyleBiomarkerAnalytics:
    """
    Analyzes lifestyle factors (sleep, diet, exercise, stress) and
    biomarkers to identify pain triggers and patterns.
    """

    def __init__(self):
        """Initialize the Lifestyle and Biomarker Analytics system."""
        self.patient_data = {}
        logger.info("Lifestyle and Biomarker Analytics system initialized")

    def record_lifestyle_data(self, patient_id: str, date: str, data: Dict[str, Any]) -> None:
        """
        Record daily lifestyle data for a patient.

        Args:
            patient_id: Unique patient identifier
            date: Date of the record
            data: Lifestyle data (sleep, activity, diet, stress, etc.)
        """
        if patient_id not in self.patient_data:
            self.patient_data[patient_id] = []

        record = {
            "date": date,
            "sleep_hours": data.get("sleep_hours", 0),
            "exercise_minutes": data.get("exercise_minutes", 0),
            "stress_level": data.get("stress_level", 0),
            "pain_level": data.get("pain_level", 0),
            "diet_quality": data.get("diet_quality", "moderate")
        }
        self.patient_data[patient_id].append(record)
        logger.info(f"Recorded lifestyle data for patient {patient_id} on {date}")

    def analyze_sleep_pain_correlation(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Calculate Pearson correlation between recorded sleep and pain pairs.

        Args:
            patient_id: Unique patient identifier

        Returns:
            Analysis or None if fewer than seven records are available.
            The correlation field is None when either series has zero variance.

        Raises:
            ValueError: If a sleep or pain observation is not finite.
        """
        if patient_id not in self.patient_data or len(self.patient_data[patient_id]) < 7:
            return None

        data = self.patient_data[patient_id]
        sleep_hours = [d["sleep_hours"] for d in data]
        pain_levels = [d["pain_level"] for d in data]

        if not all(isfinite(value) for value in sleep_hours + pain_levels):
            raise ValueError("Sleep and pain observations must be finite")

        avg_sleep = fsum(sleep_hours) / len(sleep_hours)
        avg_pain = fsum(pain_levels) / len(pain_levels)
        sleep_deviations = [value - avg_sleep for value in sleep_hours]
        pain_deviations = [value - avg_pain for value in pain_levels]
        numerator = fsum(a * b for a, b in zip(sleep_deviations, pain_deviations))
        denominator = (
            sqrt(fsum(value * value for value in sleep_deviations))
            * sqrt(fsum(value * value for value in pain_deviations))
        )
        correlation = (
            max(-1.0, min(1.0, numerator / denominator)) if denominator > 0 else None
        )

        return {
            "patient_id": patient_id,
            "average_sleep_hours": avg_sleep,
            "average_pain_level": avg_pain,
            "correlation": correlation,
            "recommendation": "increase_sleep" if avg_sleep < 7 else "maintain_sleep"
        }

    def analyze_exercise_impact(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Analyze the impact of exercise on pain levels.

        Args:
            patient_id: Unique patient identifier

        Returns:
            Exercise impact analysis or None if insufficient data
        """
        if patient_id not in self.patient_data:
            return None

        data = self.patient_data[patient_id]
        exercise_days = [d for d in data if d["exercise_minutes"] > 0]
        sedentary_days = [d for d in data if d["exercise_minutes"] == 0]

        if not exercise_days or not sedentary_days:
            return None

        avg_pain_with_exercise = sum(d["pain_level"] for d in exercise_days) / len(exercise_days)
        avg_pain_without_exercise = sum(d["pain_level"] for d in sedentary_days) / len(sedentary_days)

        return {
            "patient_id": patient_id,
            "pain_with_exercise": avg_pain_with_exercise,
            "pain_without_exercise": avg_pain_without_exercise,
            "benefit": avg_pain_without_exercise - avg_pain_with_exercise,
            "recommendation": "increase_activity" if avg_pain_with_exercise < avg_pain_without_exercise else "moderate_activity"
        }

    def identify_pain_triggers(self, patient_id: str) -> List[str]:
        """
        Identify potential lifestyle-related pain triggers.

        Args:
            patient_id: Unique patient identifier

        Returns:
            List of identified triggers
        """
        if patient_id not in self.patient_data:
            return []

        data = self.patient_data[patient_id]
        triggers = []

        # Analyze patterns
        high_pain_days = [d for d in data if d["pain_level"] > 6]

        if high_pain_days:
            avg_sleep_high_pain = sum(d["sleep_hours"] for d in high_pain_days) / len(high_pain_days)
            avg_stress_high_pain = sum(d["stress_level"] for d in high_pain_days) / len(high_pain_days)

            if avg_sleep_high_pain < 6:
                triggers.append("insufficient_sleep")
            if avg_stress_high_pain > 7:
                triggers.append("high_stress")

            low_activity_days = sum(1 for d in high_pain_days if d["exercise_minutes"] < 15)
            if low_activity_days / len(high_pain_days) > 0.7:
                triggers.append("sedentary_lifestyle")

        logger.info(f"Identified {len(triggers)} triggers for patient {patient_id}")
        return triggers

    def generate_lifestyle_recommendations(self, patient_id: str) -> Dict[str, Any]:
        """
        Generate personalized lifestyle recommendations based on analytics.

        Args:
            patient_id: Unique patient identifier

        Returns:
            Personalized recommendations
        """
        sleep_analysis = self.analyze_sleep_pain_correlation(patient_id)
        exercise_analysis = self.analyze_exercise_impact(patient_id)
        triggers = self.identify_pain_triggers(patient_id)

        recommendations = {
            "patient_id": patient_id,
            "sleep": sleep_analysis.get("recommendation") if sleep_analysis else "maintain_regular_schedule",
            "exercise": exercise_analysis.get("recommendation") if exercise_analysis else "start_light_activity",
            "triggers_to_avoid": triggers,
            "priority_actions": []
        }

        if "insufficient_sleep" in triggers:
            recommendations["priority_actions"].append("Improve sleep hygiene and aim for 7-9 hours")
        if "high_stress" in triggers:
            recommendations["priority_actions"].append("Implement stress management techniques")
        if "sedentary_lifestyle" in triggers:
            recommendations["priority_actions"].append("Gradually increase daily physical activity")

        logger.info(f"Generated lifestyle recommendations for patient {patient_id}")
        return recommendations
