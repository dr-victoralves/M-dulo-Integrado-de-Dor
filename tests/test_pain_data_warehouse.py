"""
Tests for Pain Data Warehouse
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pain_data_warehouse import PainDataWarehouse


def test_warehouse_initialization():
    """Test warehouse initialization."""
    warehouse = PainDataWarehouse()
    assert warehouse.patients == {}
    assert warehouse.clinical_data == []


def test_register_patient():
    """Test patient registration."""
    warehouse = PainDataWarehouse()
    
    patient_id = "PAT-001"
    patient_info = {"name": "John Doe", "age": 45}
    
    result = warehouse.register_patient(patient_id, patient_info)
    
    assert result["patient_id"] == patient_id
    assert result["status"] == "active"
    assert patient_id in warehouse.patients


def test_store_clinical_data():
    """Test storing clinical data."""
    warehouse = PainDataWarehouse()
    
    patient_id = "PAT-001"
    warehouse.register_patient(patient_id, {"name": "John Doe"})
    
    warehouse.store_clinical_data(patient_id, "assessment", {"pain_level": 7})
    
    assert len(warehouse.clinical_data) == 1
    assert warehouse.clinical_data[0]["patient_id"] == patient_id


def test_query_patient_data():
    """Test querying patient data."""
    warehouse = PainDataWarehouse()
    
    patient_id = "PAT-001"
    warehouse.register_patient(patient_id, {"name": "John Doe"})
    warehouse.store_clinical_data(patient_id, "assessment", {"pain_level": 7})
    
    data = warehouse.query_patient_data(patient_id)
    
    assert data is not None
    assert data["patient"]["patient_id"] == patient_id
    assert len(data["clinical_records"]) == 1


def test_get_statistics():
    """Test getting warehouse statistics."""
    warehouse = PainDataWarehouse()
    
    warehouse.register_patient("PAT-001", {"name": "John Doe"})
    warehouse.register_patient("PAT-002", {"name": "Jane Doe"})
    
    stats = warehouse.get_statistics()
    
    assert stats["total_patients"] == 2
    assert stats["active_patients"] == 2
