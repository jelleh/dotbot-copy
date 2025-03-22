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
        self.home = os.path.expanduser("~")

    def _is_safe_path(self, path: str) -> bool:
        """Check if the path is within the user's home directory."""
        try:
            return os.path.realpath(path).startswith(self.home)
        except (OSError, ValueError):
            return False

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
        default_create = self.defaults.get("create", False)
        
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
            
            # Get options from options or defaults
            overwrite = options.get("overwrite", default_overwrite)
            create = options.get("create", default_create)
            
            # Convert paths to absolute
            source_path = os.path.expanduser(source_path)
            destination_path = os.path.expanduser(destination)
            
            # Safety check: ensure both paths are within home directory
            if not self._is_safe_path(destination_path):
                self._log.error(f"Destination path {destination_path} is outside home directory")
                success = False
                continue
                
            if not self._is_safe_path(source_path):
                self._log.error(f"Source path {source_path} is outside home directory")
                success = False
                continue
            
            # Create destination directory if create is true
            if create:
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            elif not os.path.exists(os.path.dirname(destination_path)):
                self._log.error(f"Parent directory does not exist: {os.path.dirname(destination_path)}")
                success = False
                continue
            
            # Check if destination exists
            if os.path.exists(destination_path) and not overwrite:
                self._log.lowinfo(f"Skipping {destination_path} (file exists)")
                continue
                
            try:
                if os.path.isdir(source_path):
                    # For directories, we need to check if any files would be overwritten
                    if os.path.exists(destination_path):
                        if not overwrite:
                            # Check if any files would be overwritten
                            for root, _, files in os.walk(source_path):
                                for file in files:
                                    src_file = os.path.join(root, file)
                                    rel_path = os.path.relpath(src_file, source_path)
                                    dst_file = os.path.join(destination_path, rel_path)
                                    if os.path.exists(dst_file):
                                        self._log.lowinfo(f"Skipping {destination_path} (contains existing files)")
                                        continue
                        if overwrite:
                            shutil.rmtree(destination_path)
                    shutil.copytree(source_path, destination_path)
                else:
                    shutil.copy2(source_path, destination_path)
                self._log.lowinfo(f"Copied {source_path} -> {destination_path}")
            except Exception as e:
                self._log.error(f"Error copying {source_path} -> {destination_path}: {str(e)}")
                success = False
                
        return success 