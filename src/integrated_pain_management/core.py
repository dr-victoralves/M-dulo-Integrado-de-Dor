"""
Core Pain Management System
Coordinates all subsystems and provides main API
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PainManagementSystem:
    """
    Main system class that integrates all pain management modules.
    Coordinates clinical assessment, omic data, neuromodulation, lifestyle analytics,
    data warehousing, dashboard, and research protocols.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Integrated Pain Management System.

        Args:
            config: Configuration dictionary for the system
        """
        self.config = config or {}
        self.modules = {}
        logger.info("Initializing Integrated Pain Management System v1.0.0")

    def initialize_modules(self) -> None:
        """Initialize all subsystem modules."""
        logger.info("Initializing all pain management modules")
        # Module initialization will be done when subsystems are registered
        pass

    def register_module(self, name: str, module: Any) -> None:
        """
        Register a subsystem module.

        Args:
            name: Name of the module
            module: Module instance
        """
        self.modules[name] = module
        logger.info(f"Registered module: {name}")

    def get_module(self, name: str) -> Optional[Any]:
        """
        Get a registered module by name.

        Args:
            name: Name of the module

        Returns:
            Module instance or None if not found
        """
        return self.modules.get(name)

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get the current status of all system modules.

        Returns:
            Dictionary with status information
        """
        return {
            "system": "Integrated Pain Management System",
            "version": "1.0.0",
            "modules": list(self.modules.keys()),
            "status": "operational"
        }
