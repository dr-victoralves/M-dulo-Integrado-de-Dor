# Módulo Integrado de Dor (Integrated Pain Management System)

An experimental modular prototype for exploring pain-management software contracts with synthetic examples.

> **Draft prototype, not validated for clinical or production use.** State is stored in memory, and several modules use illustrative heuristics or placeholder outputs. Local tests verify selected software behavior; they do not establish treatment efficacy, calibrated confidence, security certification, or production readiness.

## Overview

The Integrated Pain Management System is a Python-based prototype of eight modules and their APIs. It demonstrates in-memory assessment records, data processing, study bookkeeping, and analytics using synthetic examples. Clinical validation, durable storage, access controls, and deployment validation are outside the implementation demonstrated here.

## System Architecture

The system consists of 8 integrated modules:

### 1. **Integrated Pain Management** (`integrated_pain_management`)
Core coordination module that orchestrates all subsystems and provides the main API for the platform.

**Key Features:**
- Central system coordination
- Module registration and management
- System-wide configuration
- Status monitoring

### 2. **Clinical Assessment System** (`clinical_assessment_system`)
Comprehensive pain assessment and patient evaluation tools.

**Key Features:**
- Pain scale assessments (VAS, NRS, etc.)
- Functional evaluations
- Patient-reported outcomes
- Pain score calculations
- Assessment history tracking

### 3. **Omic Integration Pipeline** (`omic_integration_pipeline`)
Multi-omic data processing and integration for personalized pain medicine.

**Key Features:**
- Genomic data ingestion
- Proteomic analysis
- Metabolomic profiling
- Biomarker identification
- Multi-omic data integration

### 4. **Neuromodulation AI** (`neuromodulation_ai`)
Illustrative neuromodulation heuristics; no trained or clinically validated model is included.

**Key Features:**
- Treatment parameter prediction
- Outcome forecasting
- Treatment efficacy analysis
- Parameter adjustment recommendations
- Placeholder for future machine learning model integration

### 5. **Lifestyle & Biomarker Analytics** (`lifestyle_biomarker_analytics`)
Analysis of lifestyle factors and their relationship to pain patterns.

**Key Features:**
- Pearson correlation over recorded sleep-pain pairs (`None` for a constant series)
- Exercise impact assessment
- Stress level monitoring
- Pain trigger identification
- Personalized lifestyle recommendations

### 6. **Pain Data Warehouse** (`pain_data_warehouse`)
Centralized repository for all pain-related clinical and research data.

**Key Features:**
- Patient registration
- Clinical data storage
- Treatment data management
- Advanced querying capabilities
- Research dataset export
- Data anonymization

### 7. **Clinical Dashboard** (`clinical_dashboard`)
Visualization and monitoring interface for clinical data.

**Key Features:**
- Patient overview dashboards
- Population-level metrics
- Pain trend visualizations
- Treatment efficacy charts
- Alert management
- Report generation

### 8. **Research Protocols** (`research_protocols`)
Management system for clinical research studies and protocols.

**Key Features:**
- Protocol creation and management
- Participant enrollment
- Study data collection
- Protocol status tracking
- Data analysis
- Results export

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/drvictoratalves-del/M-dulo-Integrado-de-Dor.git
cd M-dulo-Integrado-de-Dor
```

2. Install the package:
```bash
pip install -e .
```

3. Install development dependencies (optional):
```bash
pip install -r requirements.txt
```

## Quick Start

```python
from integrated_pain_management import PainManagementSystem
from clinical_assessment_system import ClinicalAssessment
from pain_data_warehouse import PainDataWarehouse

# Initialize the system
pain_system = PainManagementSystem()

# Create and register modules
assessment = ClinicalAssessment()
warehouse = PainDataWarehouse()

pain_system.register_module("clinical_assessment", assessment)
pain_system.register_module("data_warehouse", warehouse)

# Create a patient assessment
patient_id = "PAT-001"
assessment_data = {
    "intensity": 7,
    "duration_hours": 48,
    "life_interference": 8
}

assessment_result = assessment.create_assessment(patient_id, assessment_data)
print(f"Pain score: {assessment.calculate_pain_score(assessment_data)}")

# Check system status
status = pain_system.get_system_status()
print(f"System status: {status}")
```

## Module Usage Examples

### Clinical Assessment
```python
from clinical_assessment_system import ClinicalAssessment

assessment = ClinicalAssessment()
result = assessment.create_assessment("PAT-001", {
    "intensity": 6,
    "duration_hours": 24,
    "life_interference": 5
})
summary = assessment.get_assessment_summary("PAT-001")
```

### Omic Integration
```python
from omic_integration_pipeline import OmicPipeline

pipeline = OmicPipeline()
pipeline.ingest_genomic_data("PAT-001", {"SNPs": ["rs123", "rs456"]})
pipeline.ingest_proteomic_data("PAT-001", {"proteins": ["CRP", "IL-6"]})
biomarkers = pipeline.identify_pain_biomarkers("PAT-001")
```

### Neuromodulation AI
```python
from neuromodulation_ai import NeuromodulationAI

ai_system = NeuromodulationAI()
patient_profile = {"pain_level": 7, "pain_type": "chronic"}
parameters = ai_system.predict_optimal_parameters(patient_profile)
```

### Lifestyle Analytics
```python
from lifestyle_biomarker_analytics import LifestyleBiomarkerAnalytics

analytics = LifestyleBiomarkerAnalytics()
analytics.record_lifestyle_data("PAT-001", "2025-11-24", {
    "sleep_hours": 6,
    "exercise_minutes": 30,
    "stress_level": 7,
    "pain_level": 6
})
recommendations = analytics.generate_lifestyle_recommendations("PAT-001")
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

Latest local verification: 33 tests passed on Windows/Python 3.13. The example
`python examples/basic_usage.py` and Python compilation also passed. No CI or
security-scan result was available for this PR. Regression tests cover required
cohort fields, study membership, duplicate protocol IDs, and paired correlation.
These checks do not establish clinical validity or readiness to deploy.

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Project Structure
```
M-dulo-Integrado-de-Dor/
├── src/
│   ├── integrated_pain_management/    # Core system
│   ├── clinical_assessment_system/    # Assessment tools
│   ├── omic_integration_pipeline/     # Omic data processing
│   ├── neuromodulation_ai/            # AI treatment optimization
│   ├── lifestyle_biomarker_analytics/ # Lifestyle analysis
│   ├── pain_data_warehouse/           # Data storage
│   ├── clinical_dashboard/            # Visualization
│   └── research_protocols/            # Research management
├── tests/                             # Test suite
├── docs/                              # Documentation
├── examples/                          # Usage examples
├── config/                            # Configuration files
├── setup.py                           # Package setup
├── requirements.txt                   # Dependencies
└── README.md                          # This file
```

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Dr. Victor Atalves** - Initial work

## Acknowledgments

- Pain research community
- Healthcare professionals providing feedback
- Open source contributors

## Contact

For questions and support, please open an issue on GitHub.

## Version History

- **1.0.0** (2025-11-24) - Initial release with all 8 core modules
