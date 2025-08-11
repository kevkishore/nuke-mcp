"""
Nuke MCP - Portable Model Context Protocol integration for Nuke.

This package provides a plug-and-play integration between Foundry Nuke
and Claude AI through the Model Context Protocol (MCP).

Features:
- Camera tracking and 3D scene setup
- Deep compositing pipelines  
- Template/Toolset management
- Machine learning with CopyCat
- Advanced keying & compositing
- Batch processing capabilities
- Comprehensive VFX workflows

Installation:
1. Extract this package anywhere
2. Run setup.bat to install dependencies and configure
3. Place enhanced_nuke_addon.py in your Nuke plugins directory
4. Start the MCP server with start_nuke_mcp.bat
5. Configure Claude Desktop with the generated MCP settings

Author: Mahit
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Mahit"
__description__ = "Portable Nuke MCP integration for Claude AI"

import os
import sys
from pathlib import Path

# Get the package root directory
PACKAGE_ROOT = Path(__file__).parent.absolute()

# Add package to Python path if not already there
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

def get_package_info():
    """Get package information and paths."""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "package_root": PACKAGE_ROOT,
        "server_script": PACKAGE_ROOT / "enhanced_nuke_mcp_server.py",
        "addon_script": PACKAGE_ROOT / "enhanced_nuke_addon.py",
        "config_file": PACKAGE_ROOT / "mcp_config.json",
        "requirements": PACKAGE_ROOT / "requirements.txt"
    }

def get_nuke_plugin_paths():
    """Get common Nuke plugin directory paths for different OS."""
    home = Path.home()
    
    if os.name == 'nt':  # Windows
        return [
            home / ".nuke",
            Path(os.environ.get('NUKE_PATH', '')) / "plugins" if 'NUKE_PATH' in os.environ else None,
            Path("C:/Program Files/Nuke*/plugins"),
            Path("C:/Users") / os.environ.get('USERNAME', '') / ".nuke"
        ]
    elif sys.platform == 'darwin':  # macOS
        return [
            home / ".nuke",
            Path("/Applications/Nuke*/Contents/MacOS/plugins"),
            home / "Library/Application Support/Nuke/plugins"
        ]
    else:  # Linux
        return [
            home / ".nuke",
            Path("/usr/local/Nuke*/plugins"),
            home / ".local/share/nuke/plugins"
        ]

def find_nuke_plugin_directory():
    """Find the first available Nuke plugin directory."""
    for path in get_nuke_plugin_paths():
        if path and path.exists():
            return path
    
    # Return default .nuke directory
    return Path.home() / ".nuke"

# Export key functions and constants
__all__ = [
    "__version__",
    "__author__", 
    "__description__",
    "PACKAGE_ROOT",
    "get_package_info",
    "get_nuke_plugin_paths",
    "find_nuke_plugin_directory"
]