
<img width="1536" height="1024" alt="ChatGPT Image Aug 10, 2025, 12_59_29 PM" src="https://github.com/user-attachments/assets/573fd1ff-7132-4128-bf05-0a9c88907568" />






# ​ Nuke MCP (Portable) with Claude
**Drop Claude into Nuke — portable AI-powered MCP for lightning-fast node edits, context automation, and smarter compositing.**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/YOURUSERNAME/nuke-mcp)](https://github.com/YOURUSERNAME/nuke-mcp/releases)
[![GitHub Stars](https://img.shields.io/github/stars/YOURUSERNAME/nuke-mcp?style=social)](https://github.com/YOURUSERNAME/nuke-mcp/stargazers)

---
# Enhanced Nuke MCP - Complete Setup Guide

This enhanced version incorporates comprehensive VFX workflow automation including camera tracking, deep compositing, template management, machine learning capabilities, and much more.

## 🚀 New Features Added

### Camera Tracking & 3D
- **Camera Tracking**: Automated CameraTracker setup and solving
- **3D Scene Creation**: Complete 3D pipeline setup with cameras and geometry
- **Motion Analysis**: Advanced motion tracking and analysis tools

### Deep Compositing
- **Deep Pipeline Setup**: Automated deep compositing workflows
- **Deep Merging**: Sophisticated deep image combining
- **Z-depth Processing**: Advanced depth-based operations

### Template Management
- **Template Loading**: Load predefined toolsets and templates
- **Template Saving**: Save custom node configurations
- **Category Organization**: Organized template library system

### Machine Learning
- **CopyCat Integration**: AI-powered image processing
- **Model Training**: Automated neural network training
- **Inference Pipeline**: Real-time ML inference integration

### Advanced Compositing
- **Smart Keying**: Automated green/blue screen workflows
- **Motion Blur**: Vector-based motion blur systems
- **Multi-layer Compositing**: Complex compositing pipelines

### Batch Processing
- **Directory Processing**: Batch process entire directories
- **Script Automation**: Run custom processing scripts
- **Pipeline Integration**: Asset management integration

## 📦 Installation

### 1. File Placement

```bash
# Copy the addon to your Nuke directory
cp enhanced_nuke_addon.py ~/.nuke/
cp enhanced_nuke_mcp_server.py /path/to/your/mcp/servers/

# Or for Windows
copy enhanced_nuke_addon.py %USERPROFILE%\.nuke\
copy enhanced_nuke_mcp_server.py C:\path\to\mcp\servers\
```

### 2. Nuke Initialization

Create or edit your `~/.nuke/init.py` file:

```python
# Enhanced Nuke MCP Auto-load
import nuke_enhanced_mcp_addon

# Optional: Auto-start server on Nuke launch
nuke.addOnScriptLoad(lambda: nuke_enhanced_mcp_addon.start_enhanced_server(9876))
```

### 3. MCP Server Configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "enhanced-nuke": {
      "command": "python",
      "args": [
        "/path/to/enhanced_nuke_mcp_server.py"
      ],
      "env": {
        "NUKE_HOST": "localhost",
        "NUKE_PORT": "9876"
      },
      "trusted": true
    }
  }
}
```

## 🎯 Usage Examples

### Camera Tracking Workflow

```python
# Claude instruction: "Set up camera tracking for my plate sequence"

# 1. Create read node for tracking plate
create_node(
    node_type="Read",
    name="TrackingPlate",
    parameters={"file": "/path/to/plate.####.exr"}
)

# 2. Set up camera tracker
create_camera_tracker(
    source_name="TrackingPlate",
    name="CameraTracker1",
    tracking_features={
        "number_features": 300,
        "feature_size": 12,
        "feature_separation": 25
    }
)

# 3. Solve the camera
solve_camera_track(
    camera_tracker_node="CameraTracker1",
    solve_method="Full",
    refine_intrinsics=True,
    solve_focal_length=True
)

# 4. Create 3D scene with solved camera
create_3d_scene(
    camera_node="Camera1",
    geometry_nodes=["Card1", "Sphere1"],
    scene_name="TrackedScene"
)
```

### Professional Keying Setup

```python
# Claude instruction: "Create a professional green screen keying setup"

# 1. Set up advanced keyer
setup_keyer(
    input_node_name="GreenScreenPlate",
    keyer_type="Primatte",
    screen_color=[0, 0.7, 0],
    output_name="KeyedForeground"
)

# 2. Set up basic composite
setup_basic_comp(
    plate_node="BackgroundPlate",
    fg_elements=["KeyedForeground"],
    bg_elements=["SkyReplacement"],
    comp_name="FinalComposite"
)

# 3. Add motion blur if needed
setup_motion_blur(
    input_node_name="KeyedForeground",
    vector_node_name="MotionVectors",
    motion_blur_samples=20,
    shutter_angle=180.0
)
```

### Deep Compositing Pipeline

```python
# Claude instruction: "Set up a deep compositing pipeline for multiple passes"

# Set up deep pipeline with multiple render passes
setup_deep_pipeline(
    input_nodes=[
        "DeepBeauty",
        "DeepReflections", 
        "DeepRefraction",
        "DeepGI"
    ],
    merge_operation="over",
    output_name="DeepFinalOutput"
)
```

### Machine Learning Workflow

```python
# Claude instruction: "Set up CopyCat for automated cleanup"

# 1. Set up CopyCat for training
setup_copycat(
    training_input_node="DirtyPlate",
    training_output_node="CleanPlate",
    network_type="UNet",
    model_name="CleanupModel"
)

# 2. Train the model
train_copycat_model(
    copycat_node_name="CleanupModel",
    epochs=500,
    batch_size=16,
    learning_rate=0.0001
)
```

### Template Management

```python
# Claude instruction: "Save my current keying setup as a template"

# Save current selection as template
save_template(
    template_name="AdvancedKeyer",
    node_names=["Primatte1", "EdgeBlur1", "Despill1", "Premult1"],
    category="Keying",
    description="Advanced green screen keying with edge cleanup"
)

# Later: Load the template
load_template(
    template_name="AdvancedKeyer",
    position={"x": 500, "y": 200},
    parameters={
        "Primatte1": {"screenColor": [0, 0.8, 0.1]}
    }
)
```

### Batch Processing

```python
# Claude instruction: "Batch process all EXR files in this directory"

batch_process(
    input_directory="/path/to/input/frames",
    output_directory="/path/to/output/frames",
    file_pattern="*.exr",
    process_script="/path/to/custom_process.py",
    frame_range="1001-1100"
)
```

## 🎛️ Advanced Features

### Project Settings Management

```python
# Set up project for film work
set_project_settings(
    frame_range={"first": 1001, "last": 1200},
    resolution={"width": 4096, "height": 2160},
    fps=24.0,
    color_management={
        "colorManagement": "ACES",
        "workingSpace": "ACEScg",
        "viewTransform": "ACES 1.0 SDR-video"
    }
)
```

### Smart Node Layout

```python
# Auto-organize the node graph
auto_layout_nodes(
    selected_only=False,
    layout_type="tree"  # Options: vertical, horizontal, grid, tree
)
```

### Group and LiveGroup Creation

```python
# Create organized groups
create_group(
    name="ColorGrading",
    node_names=["Grade1", "ColorCorrect1", "Saturation1"],
    color=0xff0000  # Red color
)

# Create collaborative LiveGroups
create_live_group(
    name="ShotTemplate",
    node_names=["Read1", "Grade1", "Write1"],
    file_path="/shared/templates/shot_template.nk",
    auto_publish=True
)
```

## 🔧 Natural Language Examples

Here are examples of how to instruct Claude using natural language:

### Camera Tracking
*"I need to track the camera in my shot. Set up a camera tracker with 250 features, solve it, and create a 3D scene."*

### Keying
*"Create a professional green screen setup with edge cleanup and despill for my footage."*

### Compositing
*"Build me a compositing tree with my hero element over the background, add some atmospheric elements, and include proper color grading."*

### Machine Learning
*"Set up CopyCat to automatically remove wire rigs from my action sequence."*

### Templates
*"Save my current node selection as a template called 'HeroGlow' in the Effects category."*

### Batch Processing
*"Process all the DPX files in /shots/seq01/ and apply color correction, then output as EXR."*

### Deep Compositing
*"Set up a deep compositing pipeline for my multi-pass render with separate beauty, reflection, and GI passes."*

## 🚨 Troubleshooting

### Connection Issues
- Ensure Nuke is running and the addon is loaded
- Check that port 9876 is not blocked by firewall
- Verify the MCP server is connecting to the correct host/port

### Feature Availability
- **CopyCat**: Requires Foundry's CopyCat plugin
- **Deep Tools**: Requires Nuke Studio or full Nuke license
- **3D Features**: Available in all Nuke versions

### Performance Tips
- Use proxy mode for large sequences during setup
- Enable GPU acceleration when available
- Close unnecessary viewers during batch processing

## 📚 API Reference

### Camera Tracking Tools
- `create_camera_tracker()` - Set up camera tracking
- `solve_camera_track()` - Solve camera motion  
- `create_3d_scene()` - Build 3D scene setup

### Deep Compositing Tools
- `setup_deep_pipeline()` - Create deep compositing workflow

### Template Tools
- `load_template()` - Load saved templates
- `save_template()` - Save node configurations

### ML Tools
- `setup_copycat()` - Configure machine learning
- `train_copycat_model()` - Train neural networks

### Compositing Tools
- `setup_keyer()` - Advanced keying workflows
- `setup_basic_comp()` - Multi-layer compositing
- `setup_motion_blur()` - Motion vector blur

### Utility Tools
- `batch_process()` - Directory processing
- `auto_layout_nodes()` - Smart node arrangement
- `set_project_settings()` - Project configuration

This enhanced version transforms your Nuke MCP into a comprehensive VFX automation system that can handle everything from simple node creation to complex multi-stage pipelines. The natural language interface makes it incredibly powerful for both artists and technical directors.
<img src="docs/banner_screenshot.png" alt="Nuke MCP Screenshot" width="100%">

---

**Why use Nuke MCP (Portable)?**
- ⚡ **No installs required** — unzip & run in seconds
- 🤖 **Claude-powered AI** — automate node graph edits & context tasks
- 🌐 **Offline-capable** — works with Claude Desktop portable
- 🛠 **Pipeline-friendly** — integrates seamlessly into studio workflows

📥 **[Download Latest Release](https://github.com/kevkshore/nuke-mcp/releases)** • 📚 **[Read the Docs](docs/README.md)**
