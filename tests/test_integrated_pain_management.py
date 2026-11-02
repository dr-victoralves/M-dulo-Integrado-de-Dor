"""
Tests for Integrated Pain Management core module
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from integrated_pain_management import PainManagementSystem


def test_system_initialization():
    """Test that the system initializes correctly."""
    system = PainManagementSystem()
    assert system is not None
    assert system.modules == {}


def test_system_with_config():
    """Test system initialization with configuration."""
    config = {"log_level": "DEBUG"}
    system = PainManagementSystem(config)
    assert system.config == config


def test_module_registration():
    """Test module registration."""
    system = PainManagementSystem()
    
    class DummyModule:
        pass
    
    module = DummyModule()
    system.register_module("test_module", module)
    
    assert "test_module" in system.modules
    assert system.get_module("test_module") == module


def test_get_nonexistent_module():
    """Test getting a module that doesn't exist."""
    system = PainManagementSystem()
    assert system.get_module("nonexistent") is None


def test_system_status():
    """Test getting system status."""
    system = PainManagementSystem()
    status = system.get_system_status()
    
    assert "system" in status
    assert "version" in status
    assert status["version"] == "1.0.0"
    assert status["status"] == "operational"
