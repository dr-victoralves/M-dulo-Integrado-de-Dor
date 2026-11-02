#!/usr/bin/env python3
"""
Basic Usage Example for Integrated Pain Management System

This example demonstrates how to use the core features of each module.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from integrated_pain_management import PainManagementSystem
from clinical_assessment_system import ClinicalAssessment
from omic_integration_pipeline import OmicPipeline
from neuromodulation_ai import NeuromodulationAI
from lifestyle_biomarker_analytics import LifestyleBiomarkerAnalytics
from pain_data_warehouse import PainDataWarehouse
from clinical_dashboard import ClinicalDashboard
from research_protocols import ResearchProtocols


def main():
    """Demonstrate basic usage of the Integrated Pain Management System."""
    
    print("=" * 70)
    print("Integrated Pain Management System - Basic Usage Example")
    print("Experimental prototype with synthetic fixtures; outputs are not clinically validated.")
    print("=" * 70)
    print()
    
    # 1. Initialize the main system
    print("1. Initializing Pain Management System...")
    pain_system = PainManagementSystem()
    
    # 2. Initialize all modules
    print("2. Initializing system modules...")
    assessment = ClinicalAssessment()
    omic_pipeline = OmicPipeline()
    neuro_ai = NeuromodulationAI()
    lifestyle_analytics = LifestyleBiomarkerAnalytics()
    warehouse = PainDataWarehouse()
    dashboard = ClinicalDashboard(data_warehouse=warehouse)
    research = ResearchProtocols()
    
    # Register modules with the main system
    pain_system.register_module("clinical_assessment", assessment)
    pain_system.register_module("omic_pipeline", omic_pipeline)
    pain_system.register_module("neuromodulation_ai", neuro_ai)
    pain_system.register_module("lifestyle_analytics", lifestyle_analytics)
    pain_system.register_module("data_warehouse", warehouse)
    pain_system.register_module("dashboard", dashboard)
    pain_system.register_module("research", research)
    
    print(f"   Registered {len(pain_system.modules)} modules")
    print()
    
    # 3. Register a patient
    print("3. Registering patient in data warehouse...")
    patient_id = "PAT-001"
    patient_info = {
        "name": "John Doe",
        "age": 45,
        "pain_type": "chronic_lower_back"
    }
    warehouse.register_patient(patient_id, patient_info)
    print(f"   Patient {patient_id} registered")
    print()
    
    # 4. Create a clinical assessment
    print("4. Creating clinical pain assessment...")
    assessment_data = {
        "intensity": 7,
        "duration_hours": 48,
        "life_interference": 8
    }
    assessment_result = assessment.create_assessment(patient_id, assessment_data)
    pain_score = assessment.calculate_pain_score(assessment_data)
    print(f"   Assessment ID: {assessment_result['id']}")
    print(f"   Calculated pain score: {pain_score:.2f}/10")
    print()
    
    # 5. Ingest omic data
    print("5. Ingesting multi-omic data...")
    omic_pipeline.ingest_genomic_data(patient_id, {
        "SNPs": ["rs6746030", "rs1799971"],
        "genes": ["COMT", "OPRM1"]
    })
    omic_pipeline.ingest_proteomic_data(patient_id, {
        "proteins": ["IL-6", "TNF-alpha", "CRP"],
        "levels": [5.2, 3.1, 2.8]
    })
    biomarkers = omic_pipeline.identify_pain_biomarkers(patient_id)
    print(f"   Identified biomarkers: {', '.join(biomarkers)}")
    print()
    
    # 6. Display illustrative neuromodulation outputs (not a validated model)
    print("6. Demonstrating illustrative neuromodulation outputs...")
    patient_profile = {
        "pain_level": 7,
        "pain_type": "chronic"
    }
    parameters = neuro_ai.predict_optimal_parameters(patient_profile)
    print(f"   Recommended frequency: {parameters['frequency_hz']:.1f} Hz")
    print(f"   Recommended amplitude: {parameters['amplitude_ma']:.2f} mA")
    print(f"   Placeholder confidence (not calibrated): {parameters['confidence_score']:.2%}")
    print()
    
    # 7. Record lifestyle data
    print("7. Recording lifestyle data...")
    for day in range(1, 8):
        lifestyle_analytics.record_lifestyle_data(
            patient_id, 
            f"2025-11-{17+day:02d}",
            {
                "sleep_hours": 6 + (day % 3),
                "exercise_minutes": 30 if day % 2 == 0 else 0,
                "stress_level": 7 - (day % 4),
                "pain_level": 7 - (day // 3)
            }
        )
    print(f"   Recorded 7 days of lifestyle data")
    
    sleep_analysis = lifestyle_analytics.analyze_sleep_pain_correlation(patient_id)
    if sleep_analysis:
        correlation = sleep_analysis["correlation"]
        if correlation is None:
            print("   Sleep-pain correlation: undefined (constant series)")
        else:
            print(f"   Sleep-pain correlation: {correlation:.2f}")
        print(f"   Recommendation: {sleep_analysis['recommendation']}")
    print()
    
    # 8. Create a research protocol
    print("8. Creating research protocol...")
    protocol_details = {
        "title": "Neuromodulation Efficacy Study",
        "objective": "Evaluate AI-optimized neuromodulation parameters",
        "design": "randomized_controlled_trial",
        "inclusion_criteria": ["chronic_pain", "age_18_65"],
        "exclusion_criteria": ["pregnancy", "pacemaker"]
    }
    protocol = research.create_protocol("PROTO-001", protocol_details)
    research.activate_protocol("PROTO-001")
    research.enroll_participant("PROTO-001", patient_id)
    print(f"   Protocol {protocol['protocol_id']} created and activated")
    print(f"   Patient enrolled in study")
    print()
    
    # 9. Generate dashboard overview
    print("9. Generating clinical dashboard...")
    overview = dashboard.get_patient_overview(patient_id)
    print(f"   Patient overview generated")
    
    population_metrics = dashboard.get_population_metrics()
    print(f"   Total patients: {population_metrics['total_patients']}")
    print()
    
    # 10. System status
    print("10. System Status:")
    status = pain_system.get_system_status()
    print(f"   System: {status['system']}")
    print(f"   Version: {status['version']}")
    print(f"   Status: {status['status']}")
    print(f"   Active modules: {len(status['modules'])}")
    print()
    
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
