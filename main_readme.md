# 🎬 Nuke MCP - Portable Claude AI Integration

A plug-and-play integration between **Foundry Nuke** and **Claude AI** using the Model Context Protocol (MCP). No complex setup required - just download, extract, and run!

## ✨ Features

- 🎯 **Camera Tracking & 3D Scene Setup** - Automated camera tracking workflows
- 🌊 **Deep Compositing Pipelines** - Advanced deep image compositing
- 📋 **Template/Toolset Management** - Save and load custom node templates
- 🤖 **Machine Learning Integration** - CopyCat neural network support
- 🔑 **Advanced Keying & Compositing** - Professional keying workflows
- ⚡ **Batch Processing** - Process multiple files automatically
- 🎨 **Comprehensive VFX Workflows** - End-to-end production tools

## 🚀 Quick Start (3 Minutes Setup)

### Windows
```batch
# 1. Download and extract this repository
# 2. Double-click setup.bat
# 3. Follow the on-screen instructions
```

### Linux/macOS
```bash
# 1. Download and extract this repository
# 2. Make setup script executable and run it
chmod +x setup.sh
./setup.sh
# 3. Follow the on-screen instructions
```

### What the setup does:
- ✅ Creates a virtual environment
- ✅ Installs all dependencies
- ✅ Copies the Nuke addon to your `.nuke` folder
- ✅ Generates MCP configuration file
- ✅ Creates menu integration

### Configure Claude Desktop

1. **Open Claude Desktop** → Settings → MCP → Add Server
2. **Copy & paste** the content from `claude_mcp_config.json` (auto-opens after setup)
3. **Restart Claude Desktop**

### Start Using

1. **Launch Nuke** - You'll see a new "MCP" menu
2. **Click "Start Server"** in the MCP menu
3. **Test in Claude**: *"Create a blur node in Nuke and set its size to 25"*

## 📁 Project Structure

```
📦 nuke-mcp/
├── 🔧 setup.bat / setup.sh         # One-click setup scripts
├── ▶️ start_nuke_mcp.bat/.sh       # Start MCP server
├── ⚡ quick_start.bat/.sh          # Alternative launcher
├── 🔍 install_check_script.py      # Verify installation
├── ⚙️ claude_mcp_config.json       # Claude configuration (auto-generated)
├── 📄 requirements.txt             # Python dependencies
├── 🐍 enhanced_nuke_mcp_server.py  # MCP server
├── 🔌 enhanced_nuke_addon.py       # Nuke addon
├── 📋 portable_pyproject.toml      # Package configuration
├── 🏗️ portable_init.py            # Package initialization
└── 📁 venv/                        # Python virtual environment (auto-created)
```

## 🎭 Usage Examples

### Basic Operations
```
"Create a read node and load /path/to/my/footage.exr"
"Add a grade node and increase the gain to 1.2"
"Connect the read node to the grade node"
"Render the comp from frame 1 to 100"
```

### Camera Tracking
```
"Set up camera tracking on the main_plate node"
"Solve the camera track with 300 features"
"Create a 3D scene with the tracked camera"
```

### Deep Compositing
```
"Set up a deep compositing pipeline with fg_element and bg_plate"
"Create deep motion blur on the hero_element"
```

### Template Management
```
"Save the selected nodes as a template called 'my_setup'"
"Load the color_correction template at position 100,200"
```

### Machine Learning
```
"Set up CopyCat training with input_clean and target_beauty"
"Train the CopyCat model for 500 epochs"
```

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check installation
python install_check_script.py

# Manual server start (Windows)
venv\Scripts\activate
python enhanced_nuke_mcp_server.py

# Manual server start (Linux/macOS)
source venv/bin/activate
python enhanced_nuke_mcp_server.py
```

### Nuke Can't Find Addon
1. Check if `enhanced_nuke_addon.py` is in `~/.nuke/`
2. Restart Nuke
3. Look for "MCP" in the main menu

### Claude Can't Connect
1. Ensure MCP server is running (green status in Nuke MCP panel)
2. Check port 9876 isn't blocked by firewall
3. Verify Claude Desktop MCP configuration

### Port Already in Use
```python
# Change port in Nuke MCP panel or start with different port:
python enhanced_nuke_mcp_server.py --port 9877
```

## 📋 Requirements

- **Python 3.10+**
- **Foundry Nuke 13.0+** (tested with 13.x, 14.x, 15.x)
- **Claude Desktop** with MCP support
- **Windows/macOS/Linux** (cross-platform)

## 🏗️ Development

### Adding New Features
1. Add tool function to `enhanced_nuke_mcp_server.py`
2. Add handler method to `enhanced_nuke_addon.py`
3. Test with `install_check_script.py`

### Running Tests
```bash
python install_check_script.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `install_check_script.py`
5. Submit a pull request

## 📄 License

MIT License - feel free to use in personal and commercial projects.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/nuke-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/nuke-mcp/discussions)
- **Email**: mahit@example.com

## 🎯 Roadmap

- [ ] Houdini integration
- [ ] After Effects support  
- [ ] Blender connectivity
- [ ] Cloud rendering integration
- [ ] Advanced ML models
- [ ] Real-time collaboration features

---

**Made with ❤️ for the VFX community**

*If this project helps your workflow, please ⭐ star the repository!*