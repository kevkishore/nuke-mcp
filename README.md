# 🎬 Nuke MCP - Enhanced Claude AI Integration

A comprehensive integration between **Foundry Nuke** and **Claude AI** using the Model Context Protocol (MCP), featuring advanced VFX workflows, camera tracking, deep compositing, and machine learning capabilities.

## 📁 Project Structure

```
nuke_mcp/
├── 📄 .gitignore                    # Git ignore patterns
├── 📄 README.md                     # This file
│
├── 📁 src/                          # Core source code
│   ├── 🎯 enhanced_nuke_mcp_server.py    # MCP server (runs outside Nuke)
│   ├── 🔌 enhanced_nuke_addon.py         # Nuke plugin (runs inside Nuke)  
│   └── 🔧 portable_init.py               # Package initialization
│
├── 📁 setup/                        # Installation & setup scripts
│   ├── ⚙️ setup_script.bat              # Windows setup script
│   ├── 🐧 linux_setup.sh                # Unix/Linux setup script
│   ├── 🚀 portable_start_script.bat     # Windows launcher
│   ├── ✅ install_check_script.py       # Installation verification
│   └── 🐳 docker_support.dockerfile     # Docker support
│
├── 📁 config/                       # Configuration files
│   ├── 📋 requirements.txt              # Python dependencies
│   ├── ⚙️ pyproject.toml               # Package configuration
│   └── 📦 manifest.in                   # Package manifest
│
└── 📁 docs/                         # Documentation
    ├── 📖 README.md                     # Main user documentation
    ├── 📄 main_readme.md                # Additional documentation
    └── 📜 LICENSE.md                    # License information
```

## ✨ Features

- 🎯 **Camera Tracking & 3D Scene Setup** - Automated camera tracking workflows
- 🌊 **Deep Compositing Pipelines** - Advanced deep image compositing
- 📋 **Template/Toolset Management** - Save and load custom node templates
- 🤖 **Machine Learning Integration** - CopyCat neural network support
- 🔑 **Advanced Keying & Compositing** - Professional keying workflows
- ⚡ **Batch Processing** - Process multiple files automatically
- 🎨 **Comprehensive VFX Workflows** - End-to-end production tools

## 🚀 Quick Start

### Windows
```batch
cd setup/
setup_script.bat
```

### Linux/macOS
```bash
cd setup/
chmod +x linux_setup.sh
./linux_setup.sh
```

## 📖 Documentation

- **Main Documentation**: [docs/README.md](docs/README.md)
- **Additional Info**: [docs/main_readme.md](docs/main_readme.md)
- **License**: [docs/LICENSE.md](docs/LICENSE.md)

## 🔧 Development

### File Organization
- **`src/`** - Core application code and Nuke integration
- **`setup/`** - All installation, setup, and deployment scripts
- **`config/`** - Configuration files and dependencies
- **`docs/`** - User and developer documentation

### Key Components
1. **Enhanced MCP Server** (`src/enhanced_nuke_mcp_server.py`)
   - Runs outside Nuke as Claude MCP server
   - Handles communication with Claude Desktop
   - Provides 40+ advanced VFX tools

2. **Nuke Addon** (`src/enhanced_nuke_addon.py`)
   - Runs inside Nuke as Python plugin
   - Provides UI panel and menu integration
   - Executes actual node operations

3. **Setup Scripts** (`setup/`)
   - Automated installation for Windows and Unix
   - Dependency management and environment setup
   - Integration with Nuke plugin directory

## 📋 Requirements

- **Python 3.10+**
- **Foundry Nuke 13.0+** (tested with 13.x, 14.x, 15.x)
- **Claude Desktop** with MCP support
- **Windows/macOS/Linux** (cross-platform)

## 🤝 Contributing

The project is now well-organized for development:

1. **Add features** to `src/enhanced_nuke_mcp_server.py`
2. **Update Nuke integration** in `src/enhanced_nuke_addon.py`
3. **Modify setup** in `setup/` scripts
4. **Update docs** in `docs/` directory
5. **Configure dependencies** in `config/`

## 📄 License

See [docs/LICENSE.md](docs/LICENSE.md) for license information.

---

**Made with ❤️ for the VFX community**

*Professional-grade Nuke + Claude AI integration for modern VFX workflows*
