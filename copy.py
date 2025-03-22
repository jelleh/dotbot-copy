"""
Main plugin module for dotbot copy plugin.
"""

import os
import shutil
from typing import Dict, Any, Union
from dotbot import Plugin, Context


class Plugin(Plugin):
    """Plugin class for dotbot copy functionality."""

    def __init__(self, context: Context):
        """Initialize the plugin."""
        super().__init__(context)
        self.defaults = {}

    def can_handle(self, directive: str) -> bool:
        """Check if this plugin can handle the given directive."""
        return directive in ["copy", "defaults"]

    def handle(self, directive: str, data: Dict[str, Any]) -> bool:
        """Handle the copy directive."""
        if directive == "defaults":
            self.defaults = data.get("copy", {})
            return True
            
        if directive != "copy":
            raise ValueError(f"Plugin cannot handle directive {directive}")

        success = True
        
        # Get global defaults
        default_overwrite = self.defaults.get("overwrite", False)
        
        for destination, source in data.items():
            # Handle both string and dict formats
            if isinstance(source, str):
                source_path = source
                options = {}
            else:
                source_path = source.get("path", "") if source else ""
                options = source if source else {}
            
            # If source is empty or null, use the basename of the destination
            if not source_path:
                # Get basename and remove leading dot if present
                source_path = os.path.basename(destination)
                if source_path.startswith('.'):
                    source_path = source_path[1:]
            
            # Get overwrite option from options or defaults
            overwrite = options.get("overwrite", default_overwrite)
            
            # Convert paths to absolute
            source_path = os.path.expanduser(source_path)
            destination_path = os.path.expanduser(destination)
            
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Check if destination exists
            if os.path.exists(destination_path) and not overwrite:
                self._log.lowinfo(f"Skipping {destination_path} (file exists)")
                continue
                
            try:
                if os.path.isdir(source_path):
                    if os.path.exists(destination_path):
                        shutil.rmtree(destination_path)
                    shutil.copytree(source_path, destination_path)
                else:
                    shutil.copy2(source_path, destination_path)
                self._log.lowinfo(f"Copied {source_path} -> {destination_path}")
            except Exception as e:
                self._log.error(f"Error copying {source_path} -> {destination_path}: {str(e)}")
                success = False
                
        return success 