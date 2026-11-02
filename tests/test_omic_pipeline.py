"""
Tests for Omic Integration Pipeline
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from omic_integration_pipeline import OmicPipeline


def test_pipeline_initialization():
    """Test pipeline initialization."""
    pipeline = OmicPipeline()
    assert "genomic" in pipeline.omic_data
    assert "proteomic" in pipeline.omic_data


def test_ingest_genomic_data():
    """Test genomic data ingestion."""
    pipeline = OmicPipeline()
    
    patient_id = "PAT-001"
    data = {"SNPs": ["rs123", "rs456"]}
    
    result = pipeline.ingest_genomic_data(patient_id, data)
    
    assert result["patient_id"] == patient_id
    assert result["type"] == "genomic"
    assert result["processed"] is True


def test_ingest_proteomic_data():
    """Test proteomic data ingestion."""
    pipeline = OmicPipeline()
    
    patient_id = "PAT-001"
    data = {"proteins": ["IL-6", "TNF-alpha"]}
    
    result = pipeline.ingest_proteomic_data(patient_id, data)
    
    assert result["patient_id"] == patient_id
    assert result["type"] == "proteomic"


def test_integrate_patient_omics():
    """Test patient omic data integration."""
    pipeline = OmicPipeline()
    
    patient_id = "PAT-001"
    
    # Ingest different types of omic data
    pipeline.ingest_genomic_data(patient_id, {"SNPs": ["rs123"]})
    pipeline.ingest_proteomic_data(patient_id, {"proteins": ["IL-6"]})
    
    integrated = pipeline.integrate_patient_omics(patient_id)
    
    assert integrated is not None
    assert len(integrated["genomic"]) > 0
    assert len(integrated["proteomic"]) > 0


def test_identify_pain_biomarkers():
    """Test biomarker identification."""
    pipeline = OmicPipeline()
    
    patient_id = "PAT-001"
    
    pipeline.ingest_genomic_data(patient_id, {"SNPs": ["rs123"]})
    pipeline.ingest_proteomic_data(patient_id, {"proteins": ["IL-6"]})
    
    biomarkers = pipeline.identify_pain_biomarkers(patient_id)
    
    assert isinstance(biomarkers, list)
    assert len(biomarkers) > 0
