"""Regression cases use synthetic identifiers and numeric fixtures only."""
import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lifestyle_biomarker_analytics import LifestyleBiomarkerAnalytics
from pain_data_warehouse import PainDataWarehouse
from research_protocols import ResearchProtocols


@pytest.mark.parametrize("required_value", ["chronic", None])
def test_cohort_requires_an_explicit_matching_field(required_value):
    warehouse = PainDataWarehouse()
    warehouse.register_patient("TEST_MATCH", {"pain_type": required_value})
    warehouse.register_patient("TEST_MISSING", {})
    warehouse.register_patient("TEST_WRONG", {"pain_type": "other"})
    records = warehouse.query_by_criteria({"pain_type": required_value})
    assert [record["patient"]["patient_id"] for record in records] == ["TEST_MATCH"]
    assert len(warehouse.export_research_dataset({"pain_type": required_value})) == 1


@pytest.mark.parametrize("outsider", ["TEST_OTHER_STUDY", "TEST_NOT_ENROLLED"])
def test_study_rejects_data_from_nonparticipants(outsider):
    research = ResearchProtocols()
    research.create_protocol("TEST_PROTOCOL", {"title": "Synthetic study"})
    research.create_protocol("TEST_OTHER_PROTOCOL", {"title": "Other synthetic study"})
    research.enroll_participant("TEST_PROTOCOL", "TEST_ENROLLED")
    research.enroll_participant("TEST_OTHER_PROTOCOL", "TEST_OTHER_STUDY")
    research.collect_study_data("TEST_PROTOCOL", "TEST_ENROLLED", "visit", {"value": 1})
    with pytest.raises(ValueError, match="not enrolled"):
        research.collect_study_data("TEST_PROTOCOL", outsider, "visit", {"value": 2})
    status = research.get_protocol_status("TEST_PROTOCOL")
    analysis = research.analyze_protocol_data("TEST_PROTOCOL")
    assert status["total_participants"] == 1
    assert status["data_points_collected"] == 1
    assert analysis["participants_with_data"] == 1
    assert analysis["total_data_points"] == 1


def test_duplicate_protocol_id_preserves_original_metadata_and_study():
    research = ResearchProtocols()
    research.create_protocol("TEST_PROTOCOL", {"title": "Original synthetic study"})
    research.enroll_participant("TEST_PROTOCOL", "TEST_ENROLLED")
    research.collect_study_data("TEST_PROTOCOL", "TEST_ENROLLED", "visit", {"value": 1})
    before = copy.deepcopy(research.export_study_results("TEST_PROTOCOL"))
    with pytest.raises(ValueError, match="already exists"):
        research.create_protocol("TEST_PROTOCOL", {"title": "Different synthetic study"})
    after = research.export_study_results("TEST_PROTOCOL")
    assert after["protocol"] == before["protocol"]
    assert after["status"] == before["status"]
    assert after["analysis"]["total_data_points"] == 1
    assert after["analysis"]["participants_with_data"] == 1


@pytest.mark.parametrize(
    "sleep,pain,expected",
    [
        ([1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7], 1.0),
        ([1, 2, 3, 4, 5, 6, 7], [7, 6, 5, 4, 3, 2, 1], -1.0),
        ([1, 2, 3, 4, 5, 6, 7], [1, 0, 1, 0, 1, 0, 1], 0.0),
    ],
)
def test_sleep_pain_correlation_uses_observed_pairs(sleep, pain, expected):
    analytics = LifestyleBiomarkerAnalytics()
    for index, (hours, level) in enumerate(zip(sleep, pain), start=1):
        analytics.record_lifestyle_data(
            "TEST_ONLY", f"2026-01-{index:02d}",
            {"sleep_hours": hours, "pain_level": level},
        )
    result = analytics.analyze_sleep_pain_correlation("TEST_ONLY")
    assert result["correlation"] == pytest.approx(expected)


@pytest.mark.parametrize(
    "sleep,pain",
    [
        ([7] * 7, [1, 2, 3, 4, 5, 6, 7]),
        ([1, 2, 3, 4, 5, 6, 7], [4] * 7),
    ],
)
def test_correlation_is_undefined_for_a_constant_series(sleep, pain):
    analytics = LifestyleBiomarkerAnalytics()
    for index, (hours, level) in enumerate(zip(sleep, pain), start=1):
        analytics.record_lifestyle_data(
            "TEST_ONLY", f"2026-01-{index:02d}",
            {"sleep_hours": hours, "pain_level": level},
        )
    result = analytics.analyze_sleep_pain_correlation("TEST_ONLY")
    assert result["correlation"] is None


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), float("-inf")])
def test_correlation_rejects_nonfinite_observations(invalid):
    analytics = LifestyleBiomarkerAnalytics()
    for index in range(1, 8):
        analytics.record_lifestyle_data(
            "TEST_ONLY", f"2026-01-{index:02d}",
            {"sleep_hours": invalid if index == 1 else index, "pain_level": index},
        )
    with pytest.raises(ValueError, match="finite"):
        analytics.analyze_sleep_pain_correlation("TEST_ONLY")
