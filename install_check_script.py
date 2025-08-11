#!/usr/bin/env python3
"""
Installation verification script for Nuke MCP.
Checks if all components are properly installed and configured.
"""

import os
import sys
import json
import socket
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        return False, f"Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import mcp
        mcp_version = getattr(mcp, '__version__', 'unknown')
    except ImportError:
        return False, "MCP not installed"
    
    try:
        import pydantic
        pydantic_version = getattr(pydantic, '__version__', 'unknown')
    except ImportError:
        return False, "Pydantic not installed"
    
    return True, f"MCP {mcp_version}, Pydantic {pydantic_version}"

def check_nuke_addon():
    """Check if Nuke addon is installed."""
    script_dir = Path(__file__).parent
    addon_source = script_dir / "enhanced_nuke_addon.py"
    
    if not addon_source.exists():
        return False, "Addon source file not found"
    
    # Check common Nuke plugin locations
    home = Path.home()
    nuke_dirs = [
        home / ".nuke",
        Path(os.environ.get('NUKE_PATH', '')) if 'NUKE_PATH' in os.environ else None
    ]
    
    for nuke_dir in nuke_dirs:
        if nuke_dir and nuke_dir.exists():
            addon_installed = nuke_dir / "enhanced_nuke_addon.py"
            if addon_installed.exists():
                return True, f"Installed in {nuke_dir}"
    
    return False, "Not found in Nuke plugin directories"

def check_mcp_config():
    """Check if MCP configuration file exists."""
    script_dir = Path(__file__).parent
    config_file = script_dir / "claude_mcp_config.json"
    
    if not config_file.exists():
        return False, "MCP config file not found"
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if 'mcpServers' in config and 'nuke' in config['mcpServers']:
            return True, "Valid MCP configuration found"
        else:
            return False, "Invalid MCP configuration format"
    except json.JSONDecodeError:
        return False, "Invalid JSON in MCP config"

def check_port_availability(port=9876):
    """Check if the MCP server port is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            return False, f"Port {port} is already in use"
        else:
            return True, f"Port {port} is available"
    except Exception as e:
        return False, f"Error checking port: {str(e)}"

def check_server_script():
    """Check if server script is available."""
    script_dir = Path(__file__).parent
    server_script = script_dir / "enhanced_nuke_mcp_server.py"
    
    if not server_script.exists():
        return False, "Server script not found"
    
    return True, f"Server script found: {server_script}"

def main():
    """Run all installation checks."""
    print("=" * 60)
    print("          NUKE MCP INSTALLATION CHECK")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Server Script", check_server_script),
        ("Nuke Addon", check_nuke_addon),
        ("MCP Config", check_mcp_config),
        ("Port Availability", check_port_availability),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            if check_func.__code__.co_argcount == 0:
                passed, message = check_func()
            else:
                passed, message = check_func(9876)
            
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{check_name:20} | {status:8} | {message}")
            
            if not passed:
                all_passed = False
                
        except Exception as e:
            print(f"{check_name:20} | ✗ ERROR  | {str(e)}")
            all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Your Nuke MCP installation is ready.")
        print()
        print("Next steps:")
        print("1. Copy claude_mcp_config.json content to Claude Desktop settings")
        print("2. Start Nuke and look for the 'MCP' menu")
        print("3. Click 'Start Server' in the MCP menu")
        print("4. Test with Claude: 'Create a blur node in Nuke'")
    else:
        print("❌ SOME CHECKS FAILED. Please resolve the issues above.")
        print()
        print("Common solutions:")
        print("- Run setup.bat if you haven't already")
        print("- Make sure Python 3.10+ is installed")
        print("- Check that Nuke is properly installed")
        print("- Ensure no other application is using port 9876")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)