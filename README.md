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

### Step 1: Download & Extract
```bash
# Download the repository
git clone https://github.com/yourusername/nuke-mcp.git
# OR download ZIP and extract anywhere you want
```

### Step 2: Run Setup
```batch
# Double-click or run:
setup.bat
```

This will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Copy the Nuke addon to your `.nuke` folder
- ✅ Generate MCP configuration file
- ✅ Create menu integration

### Step 3: Configure Claude Desktop

1. **Open Claude Desktop** → Settings → MCP → Add Server
2. **Copy & paste** the content from `claude_mcp_config.json` (auto-opens after setup)
3. **Restart Claude Desktop**

### Step 4: Start Using

1. **Launch Nuke** - You'll see a new "MCP" menu
2. **Click "Start Server"** in the MCP menu
3. **Test in Claude**: *"Create a blur node in Nuke and set its size to 25"*

## 📁 What Gets Installed Where

```
📦 Your Download Folder/
├── 📁 nuke-mcp/                    # Main package
│   ├── 🔧 setup.bat                # One-click setup
│   ├── ▶️ start_nuke_mcp.bat       # Start MCP server
│   ├── ⚡ quick_start.bat          # Alternative launcher
│   ├── 🔍 install_check.py        # Verify installation
│   ├── ⚙️ claude_mcp_config.json  # Claude configuration (auto-generated)
│   └── 📁 venv/                    # Python virtual environment
│
📁 %USERPROFILE%/.nuke/             # Nuke user directory
├── 🔌 enhanced_nuke_addon.py       # Main Nuke addon (auto-copied)
└── 📋 menu.py                      # Menu integration (auto-created)
```

## 🛠️ Manual Installation (If Needed)

If the automatic setup doesn't work:

### 1. Install Dependencies
```bash
cd nuke-mcp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 2. Install Nuke Addon
Copy `enhanced_nuke_addon.py` to your Nuke plugins directory:
- **Windows**: `C:\Users\<username>\.nuke\`
- **macOS**: `~/.nuke/`
- **Linux**: `~/.nuke/`

### 3. Configure Claude
Add this to Claude Desktop MCP settings:
```json
{
  "mcpServers": {
    "nuke": {
      "command": "cmd",
      "args": ["/c", "C:\\path\\to\\your\\nuke-mcp\\start_nuke_mcp.bat"]
    }
  }
}
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
python install_check.py

# Manual server start
venv\Scripts\activate
python enhanced_nuke_mcp_server.py
```

### Nuke Can't Find Addon
1. Check if `enhanced_nuke_addon.py` is in `%USERPROFILE%\.nuke\`
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

## 🏗️ Development

### Project Structure
```
nuke-mcp/
├── __init__.py                      # Package initialization
├── enhanced_nuke_mcp_server.py      # MCP server (runs outside Nuke)
├── enhanced_nuke_addon.py           # Nuke plugin (runs inside Nuke)
├── setup.bat                        # Automated setup script
├── start_nuke_mcp.bat              # Server launcher
├── install_check.py                # Installation verifier
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Package configuration
└── README.md                       # This file
```

### Adding New Features
1. Add tool function to `enhanced_nuke_mcp_server.py`
2. Add handler method to `enhanced_nuke_addon.py`
3. Test with `install_check.py`

## 📋 Requirements

- **Python 3.10+**
- **Foundry Nuke 13.0+** (tested with 13.x, 14.x, 15.x)
- **Claude Desktop** with MCP support
- **Windows/macOS/Linux** (cross-platform)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `install_check.py`
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