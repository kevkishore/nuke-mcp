#!/usr/bin/env python3
"""
Enhanced Nuke MCP Server with comprehensive VFX workflow automation.
Incorporates camera tracking, deep compositing, template management, and ML capabilities.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types
from pydantic import BaseModel
import socket
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enhanced-nuke-mcp")

# Nuke connection configuration
NUKE_HOST = "localhost"
NUKE_PORT = 9876
CONNECTION_TIMEOUT = 5
RESPONSE_TIMEOUT = 30

class NukeConnection:
    """Enhanced connection handler for Nuke with better error handling"""
    
    def __init__(self, host: str = NUKE_HOST, port: int = NUKE_PORT):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """Establish connection to Nuke"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(CONNECTION_TIMEOUT)
            self.socket.connect((self.host, self.port))
            logger.info(f"Connected to Nuke at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Nuke: {str(e)}")
            return False
    
    def send_command(self, command: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send command to Nuke and return response"""
        if not self.socket:
            if not self.connect():
                raise ConnectionError("Could not connect to Nuke")
        
        try:
            message = {
                "command": command,
                "params": params or {}
            }
            
            # Send message
            message_str = json.dumps(message) + "\n"
            self.socket.send(message_str.encode())
            
            # Receive response
            self.socket.settimeout(RESPONSE_TIMEOUT)
            response_data = ""
            while True:
                chunk = self.socket.recv(4096).decode()
                if not chunk:
                    break
                response_data += chunk
                if '\n' in chunk:
                    break
            
            if response_data.strip():
                return json.loads(response_data.strip())
            else:
                return {"status": "success", "message": "Command executed"}
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Nuke: {str(e)}")
            return {"status": "error", "message": f"Invalid response format: {str(e)}"}
        except Exception as e:
            logger.error(f"Error communicating with Nuke: {str(e)}")
            self.disconnect()
            raise
    
    def disconnect(self):
        """Close connection to Nuke"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

# Global Nuke connection
_nuke_connection = None

def get_nuke_connection() -> NukeConnection:
    """Get or create Nuke connection"""
    global _nuke_connection
    if _nuke_connection is None:
        _nuke_connection = NukeConnection()
    return _nuke_connection

# Initialize the MCP server
app = Server("enhanced-nuke-mcp")

# ============================================================================
# BASIC NODE OPERATIONS (Enhanced versions of existing tools)
# ============================================================================

@app.tool()
async def create_node(
    node_type: str,
    name: Optional[str] = None,
    position: Optional[List[int]] = None,
    inputs: Optional[List[str]] = None,
    parameters: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a node in Nuke with enhanced parameter support.
    
    Args:
        node_type: Type of node to create (e.g., 'Blur', 'Grade', 'Read')
        name: Optional custom name for the node
        position: Optional [x, y] position in node graph
        inputs: Optional list of input node names to connect
        parameters: Optional dictionary of knob values to set
    """
    try:
        logger.info(f"Creating node: {node_type}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("create_node", {
            "node_type": node_type,
            "name": name,
            "position": position,
            "inputs": inputs,
            "parameters": parameters
        })
        
        if result.get("status") == "error":
            return f"Error creating node: {result.get('message', 'Unknown error')}"
        
        node_name = result.get("name", name or node_type)
        return f"Created {node_type} node named '{node_name}'"
        
    except Exception as e:
        logger.error(f"Error in create_node: {str(e)}")
        return f"Error creating node: {str(e)}"

@app.tool()
async def connect_nodes(
    output_node: str,
    input_node: str,
    input_index: int = 0
) -> str:
    """
    Connect two nodes in the node graph.
    
    Args:
        output_node: Name of the node providing output
        input_node: Name of the node receiving input
        input_index: Input socket index (default: 0)
    """
    try:
        logger.info(f"Connecting {output_node} to {input_node}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("connect_nodes", {
            "output_node": output_node,
            "input_node": input_node,
            "input_index": input_index
        })
        
        if result.get("status") == "error":
            return f"Error connecting nodes: {result.get('message', 'Unknown error')}"
            
        return f"Connected {output_node} to {input_node} at input {input_index}"
        
    except Exception as e:
        logger.error(f"Error in connect_nodes: {str(e)}")
        return f"Error connecting nodes: {str(e)}"

@app.tool()
async def set_knob_value(
    node_name: str,
    knob_name: str,
    value: Union[str, int, float, List[float]]
) -> str:
    """
    Set a knob value on a node.
    
    Args:
        node_name: Name of the node
        knob_name: Name of the knob/parameter
        value: Value to set (supports strings, numbers, and lists)
    """
    try:
        logger.info(f"Setting {knob_name} on {node_name} to {value}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("set_knob_value", {
            "node_name": node_name,
            "knob_name": knob_name,
            "value": value
        })
        
        if result.get("status") == "error":
            return f"Error setting knob: {result.get('message', 'Unknown error')}"
            
        return f"Set {knob_name} on {node_name} to {value}"
        
    except Exception as e:
        logger.error(f"Error in set_knob_value: {str(e)}")
        return f"Error setting knob value: {str(e)}"

# ============================================================================
# CAMERA TRACKING TOOLS
# ============================================================================

@app.tool()
async def create_camera_tracker(
    source_name: str,
    name: Optional[str] = None,
    tracking_features: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create and configure a CameraTracker node for camera tracking.
    
    Args:
        source_name: Name of the source Read node
        name: Optional name for the CameraTracker node
        tracking_features: Optional tracking configuration dict with keys:
            - number_features: Number of features to track (default: 200)
            - feature_size: Size of tracking features (default: 15)
            - feature_separation: Minimum separation between features (default: 20)
            - tracking_range: Frame range for tracking (default: full range)
    """
    try:
        logger.info(f"Creating CameraTracker for source: {source_name}")
        nuke = get_nuke_connection()
        
        # Set default tracking parameters
        default_features = {
            "number_features": 200,
            "feature_size": 15,
            "feature_separation": 20,
            "tracking_range": None  # Will use full range
        }
        
        if tracking_features:
            default_features.update(tracking_features)
        
        result = nuke.send_command("create_camera_tracker", {
            "source_name": source_name,
            "name": name,
            "tracking_features": default_features
        })
        
        if result.get("status") == "error":
            return f"Error creating CameraTracker: {result.get('message', 'Unknown error')}"
        
        tracker_name = result.get("name", name or "CameraTracker1")
        return f"Created CameraTracker '{tracker_name}' connected to {source_name} with {default_features['number_features']} features"
        
    except Exception as e:
        logger.error(f"Error in create_camera_tracker: {str(e)}")
        return f"Error creating camera tracker: {str(e)}"

@app.tool()
async def solve_camera_track(
    camera_tracker_node: str,
    solve_method: str = "Match-Moving",
    refine_intrinsics: bool = True,
    solve_focal_length: bool = True
) -> str:
    """
    Solve camera tracking using the specified CameraTracker node.
    
    Args:
        camera_tracker_node: Name of the CameraTracker node
        solve_method: Solving method ('Match-Moving', 'Stabilize', 'Modal Analysis')
        refine_intrinsics: Whether to refine camera intrinsics
        solve_focal_length: Whether to solve for focal length
    """
    try:
        logger.info(f"Solving camera track for: {camera_tracker_node}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("solve_camera_track", {
            "camera_tracker_node": camera_tracker_node,
            "solve_method": solve_method,
            "refine_intrinsics": refine_intrinsics,
            "solve_focal_length": solve_focal_length
        })
        
        if result.get("status") == "error":
            return f"Error solving camera track: {result.get('message', 'Unknown error')}"
        
        solve_error = result.get("solve_error", "Unknown")
        tracked_features = result.get("tracked_features", "Unknown")
        
        return f"Camera track solved for {camera_tracker_node}. Method: {solve_method}, Tracked features: {tracked_features}, Solve error: {solve_error}"
        
    except Exception as e:
        logger.error(f"Error in solve_camera_track: {str(e)}")
        return f"Error solving camera track: {str(e)}"

@app.tool()
async def create_3d_scene(
    camera_node: Optional[str] = None,
    geometry_nodes: Optional[List[str]] = None,
    scene_name: Optional[str] = None
) -> str:
    """
    Create a 3D scene setup with camera and geometry.
    
    Args:
        camera_node: Name of the camera node to use
        geometry_nodes: List of 3D geometry node names to include
        scene_name: Optional name for the scene setup
    """
    try:
        logger.info("Creating 3D scene setup")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("create_3d_scene", {
            "camera_node": camera_node,
            "geometry_nodes": geometry_nodes or [],
            "scene_name": scene_name
        })
        
        if result.get("status") == "error":
            return f"Error creating 3D scene: {result.get('message', 'Unknown error')}"
        
        created_nodes = result.get("created_nodes", [])
        scene_name = result.get("scene_name", "3D_Scene")
        
        return f"Created 3D scene '{scene_name}' with nodes: {', '.join(created_nodes)}"
        
    except Exception as e:
        logger.error(f"Error in create_3d_scene: {str(e)}")
        return f"Error creating 3D scene: {str(e)}"

# ============================================================================
# DEEP COMPOSITING TOOLS
# ============================================================================

@app.tool()
async def setup_deep_pipeline(
    input_nodes: List[str],
    merge_operation: str = "over",
    output_name: Optional[str] = None
) -> str:
    """
    Set up a Deep compositing pipeline with multiple inputs.
    
    Args:
        input_nodes: List of input node names (should be deep images)
        merge_operation: Deep merge operation ('over', 'under', 'plus', 'multiply')
        output_name: Optional name for the output DeepWrite node
    """
    try:
        logger.info(f"Setting up deep pipeline with {len(input_nodes)} inputs")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("setup_deep_pipeline", {
            "input_nodes": input_nodes,
            "merge_operation": merge_operation,
            "output_name": output_name
        })
        
        if result.get("status") == "error":
            return f"Error setting up deep pipeline: {result.get('message', 'Unknown error')}"
        
        created_nodes = result.get("created_nodes", [])
        return f"Created deep compositing pipeline with nodes: {', '.join(created_nodes)}"
        
    except Exception as e:
        logger.error(f"Error in setup_deep_pipeline: {str(e)}")
        return f"Error setting up deep pipeline: {str(e)}"

# ============================================================================
# TEMPLATE MANAGEMENT TOOLS
# ============================================================================

@app.tool()
async def load_template(
    template_name: str,
    position: Optional[Dict[str, int]] = None,
    parameters: Optional[Dict[str, Any]] = None
) -> str:
    """
    Load a Nuke template (Toolset) into the current script.
    
    Args:
        template_name: Name of the template to load
        position: Optional position dict with 'x' and 'y' keys
        parameters: Optional parameters to apply to loaded nodes
    """
    try:
        logger.info(f"Loading template: {template_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("load_template", {
            "template_name": template_name,
            "position": position or {"x": 0, "y": 0},
            "parameters": parameters
        })
        
        if result.get("status") == "error":
            return f"Error loading template: {result.get('message', 'Unknown error')}"
        
        loaded_nodes = result.get("loaded_nodes", [])
        return f"Loaded template '{template_name}' with nodes: {', '.join(loaded_nodes)}"
        
    except Exception as e:
        logger.error(f"Error in load_template: {str(e)}")
        return f"Error loading template: {str(e)}"

@app.tool()
async def save_template(
    template_name: str,
    node_names: List[str],
    category: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """
    Save selected nodes as a template (Toolset).
    
    Args:
        template_name: Name for the new template
        node_names: List of node names to include in template
        category: Optional category for the template
        description: Optional description of the template
    """
    try:
        logger.info(f"Saving template: {template_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("save_template", {
            "template_name": template_name,
            "node_names": node_names,
            "category": category or "Custom",
            "description": description
        })
        
        if result.get("status") == "error":
            return f"Error saving template: {result.get('message', 'Unknown error')}"
        
        template_path = result.get("template_path", "Unknown")
        return f"Saved template '{template_name}' with {len(node_names)} nodes to: {template_path}"
        
    except Exception as e:
        logger.error(f"Error in save_template: {str(e)}")
        return f"Error saving template: {str(e)}"

# ============================================================================
# KEYING AND COMPOSITING TOOLS
# ============================================================================

@app.tool()
async def setup_keyer(
    input_node_name: str,
    keyer_type: str = "Primatte",
    screen_color: Optional[List[float]] = None,
    output_name: Optional[str] = None
) -> str:
    """
    Set up a keying pipeline for green/blue screen removal.
    
    Args:
        input_node_name: Name of the input node with the screen
        keyer_type: Type of keyer ('Primatte', 'Keyer', 'IBKColour', 'Difference')
        screen_color: Optional RGB values for screen color (default: [0, 0.7, 0])
        output_name: Optional name for the output node
    """
    try:
        logger.info(f"Setting up {keyer_type} keyer for: {input_node_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("setup_keyer", {
            "input_node_name": input_node_name,
            "keyer_type": keyer_type,
            "screen_color": screen_color or [0, 0.7, 0],
            "output_name": output_name
        })
        
        if result.get("status") == "error":
            return f"Error setting up keyer: {result.get('message', 'Unknown error')}"
        
        created_nodes = result.get("created_nodes", [])
        return f"Created {keyer_type} keying pipeline with nodes: {', '.join(created_nodes)}"
        
    except Exception as e:
        logger.error(f"Error in setup_keyer: {str(e)}")
        return f"Error setting up keyer: {str(e)}"

@app.tool()
async def setup_basic_comp(
    plate_node: str,
    fg_elements: Optional[List[str]] = None,
    bg_elements: Optional[List[str]] = None,
    comp_name: Optional[str] = None
) -> str:
    """
    Set up a basic compositing tree with foreground and background elements.
    
    Args:
        plate_node: Name of the main plate/background node
        fg_elements: List of foreground element node names
        bg_elements: List of background element node names
        comp_name: Optional name for the final composite
    """
    try:
        logger.info(f"Setting up basic comp with plate: {plate_node}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("setup_basic_comp", {
            "plate_node": plate_node,
            "fg_elements": fg_elements or [],
            "bg_elements": bg_elements or [],
            "comp_name": comp_name
        })
        
        if result.get("status") == "error":
            return f"Error setting up comp: {result.get('message', 'Unknown error')}"
        
        created_nodes = result.get("created_nodes", [])
        final_node = result.get("final_node", "Composite")
        
        return f"Created basic comp '{final_node}' with {len(created_nodes)} nodes"
        
    except Exception as e:
        logger.error(f"Error in setup_basic_comp: {str(e)}")
        return f"Error setting up basic comp: {str(e)}"

# ============================================================================
# MOTION BLUR AND EFFECTS TOOLS
# ============================================================================

@app.tool()
async def setup_motion_blur(
    input_node_name: str,
    vector_node_name: Optional[str] = None,
    motion_blur_samples: int = 15,
    shutter_angle: float = 180.0
) -> str:
    """
    Set up motion blur using motion vectors.
    
    Args:
        input_node_name: Name of the input image node
        vector_node_name: Optional name of the motion vector node
        motion_blur_samples: Number of motion blur samples
        shutter_angle: Camera shutter angle in degrees
    """
    try:
        logger.info(f"Setting up motion blur for: {input_node_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("setup_motion_blur", {
            "input_node_name": input_node_name,
            "vector_node_name": vector_node_name,
            "motion_blur_samples": motion_blur_samples,
            "shutter_angle": shutter_angle
        })
        
        if result.get("status") == "error":
            return f"Error setting up motion blur: {result.get('message', 'Unknown error')}"
        
        created_nodes = result.get("created_nodes", [])
        return f"Created motion blur setup with nodes: {', '.join(created_nodes)}"
        
    except Exception as e:
        logger.error(f"Error in setup_motion_blur: {str(e)}")
        return f"Error setting up motion blur: {str(e)}"

# ============================================================================
# MACHINE LEARNING TOOLS (CopyCat)
# ============================================================================

@app.tool()
async def setup_copycat(
    training_input_node: str,
    training_output_node: str,
    network_type: str = "UNet",
    model_name: Optional[str] = None
) -> str:
    """
    Set up a CopyCat node for machine learning operations.
    
    Args:
        training_input_node: Name of the training input node
        training_output_node: Name of the training output/target node
        network_type: Type of neural network ('UNet', 'ResNet', 'DenseNet')
        model_name: Optional name for the model
    """
    try:
        logger.info(f"Setting up CopyCat with network type: {network_type}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("setup_copycat", {
            "training_input_node": training_input_node,
            "training_output_node": training_output_node,
            "network_type": network_type,
            "model_name": model_name
        })
        
        if result.get("status") == "error":
            return f"Error setting up CopyCat: {result.get('message', 'Unknown error')}"
        
        copycat_node = result.get("copycat_node", "CopyCat1")
        return f"Created CopyCat node '{copycat_node}' with {network_type} network"
        
    except Exception as e:
        logger.error(f"Error in setup_copycat: {str(e)}")
        return f"Error setting up CopyCat: {str(e)}"

@app.tool()
async def train_copycat_model(
    copycat_node_name: str,
    epochs: int = 200,
    batch_size: int = 8,
    learning_rate: float = 0.001
) -> str:
    """
    Train a CopyCat neural network model.
    
    Args:
        copycat_node_name: Name of the CopyCat node to train
        epochs: Number of training epochs
        batch_size: Training batch size
        learning_rate: Learning rate for training
    """
    try:
        logger.info(f"Training CopyCat model: {copycat_node_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("train_copycat_model", {
            "copycat_node_name": copycat_node_name,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate
        })
        
        if result.get("status") == "error":
            return f"Error training CopyCat: {result.get('message', 'Unknown error')}"
        
        training_loss = result.get("final_loss", "Unknown")
        training_time = result.get("training_time", "Unknown")
        
        return f"Training completed for {copycat_node_name}. Final loss: {training_loss}, Training time: {training_time}"
        
    except Exception as e:
        logger.error(f"Error in train_copycat_model: {str(e)}")
        return f"Error training CopyCat model: {str(e)}"

# ============================================================================
# BATCH PROCESSING TOOLS
# ============================================================================

@app.tool()
async def batch_process(
    input_directory: str,
    output_directory: str,
    file_pattern: str = "*.exr",
    process_script: Optional[str] = None,
    frame_range: Optional[str] = None
) -> str:
    """
    Batch process a directory of files using Nuke.
    
    Args:
        input_directory: Path to input directory
        output_directory: Path to output directory
        file_pattern: File pattern to match (e.g., '*.exr', '*.dpx')
        process_script: Optional path to processing script
        frame_range: Optional frame range (e.g., '1-100')
    """
    try:
        logger.info(f"Batch processing files from: {input_directory}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("batch_process", {
            "input_directory": input_directory,
            "output_directory": output_directory,
            "file_pattern": file_pattern,
            "process_script": process_script,
            "frame_range": frame_range
        })
        
        if result.get("status") == "error":
            return f"Error in batch processing: {result.get('message', 'Unknown error')}"
        
        processed_files = result.get("processed_files", 0)
        failed_files = result.get("failed_files", 0)
        
        return f"Batch processing completed. Processed: {processed_files}, Failed: {failed_files}"
        
    except Exception as e:
        logger.error(f"Error in batch_process: {str(e)}")
        return f"Error in batch processing: {str(e)}"

# ============================================================================
# PROJECT MANAGEMENT TOOLS
# ============================================================================

@app.tool()
async def set_project_settings(
    frame_range: Optional[Dict[str, int]] = None,
    resolution: Optional[Dict[str, int]] = None,
    fps: Optional[float] = None,
    color_management: Optional[Dict[str, str]] = None
) -> str:
    """
    Set project settings like frame range, resolution, FPS, and color management.
    
    Args:
        frame_range: Dict with 'first' and 'last' frame numbers
        resolution: Dict with 'width' and 'height' values
        fps: Frames per second
        color_management: Dict with color space settings
    """
    try:
        logger.info("Setting project settings")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("set_project_settings", {
            "frame_range": frame_range,
            "resolution": resolution,
            "fps": fps,
            "color_management": color_management
        })
        
        if result.get("status") == "error":
            return f"Error setting project settings: {result.get('message', 'Unknown error')}"
        
        settings_applied = []
        if frame_range:
            settings_applied.append(f"Frame range: {frame_range['first']}-{frame_range['last']}")
        if resolution:
            settings_applied.append(f"Resolution: {resolution['width']}x{resolution['height']}")
        if fps:
            settings_applied.append(f"FPS: {fps}")
        
        return f"Applied project settings: {'; '.join(settings_applied)}"
        
    except Exception as e:
        logger.error(f"Error in set_project_settings: {str(e)}")
        return f"Error setting project settings: {str(e)}"

# ============================================================================
# SCRIPT MANAGEMENT TOOLS
# ============================================================================

@app.tool()
async def load_script(file_path: str) -> str:
    """
    Load a Nuke script file.
    
    Args:
        file_path: Path to the Nuke script file (.nk)
    """
    try:
        logger.info(f"Loading script: {file_path}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("load_script", {
            "file_path": file_path
        })
        
        if result.get("status") == "error":
            return f"Error loading script: {result.get('message', 'Unknown error')}"
        
        loaded_nodes = result.get("loaded_nodes", 0)
        return f"Loaded script from {file_path} with {loaded_nodes} nodes"
        
    except Exception as e:
        logger.error(f"Error in load_script: {str(e)}")
        return f"Error loading script: {str(e)}"

@app.tool()
async def save_script(file_path: str, selected_only: bool = False) -> str:
    """
    Save the current Nuke script to a file.
    
    Args:
        file_path: Path where to save the script (.nk)
        selected_only: Whether to save only selected nodes
    """
    try:
        logger.info(f"Saving script to: {file_path}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("save_script", {
            "file_path": file_path,
            "selected_only": selected_only
        })
        
        if result.get("status") == "error":
            return f"Error saving script: {result.get('message', 'Unknown error')}"
        
        saved_nodes = result.get("saved_nodes", 0)
        return f"Saved script to {file_path} with {saved_nodes} nodes"
        
    except Exception as e:
        logger.error(f"Error in save_script: {str(e)}")
        return f"Error saving script: {str(e)}"

@app.tool()
async def run_python_script(
    script: str,
    args: Optional[Dict[str, Any]] = None
) -> str:
    """
    Run a Python script in Nuke.
    
    Args:
        script: Python code to execute
        args: Optional dictionary of arguments to pass to the script
    """
    try:
        logger.info("Running Python script in Nuke")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("run_python_script", {
            "script": script,
            "args": args or {}
        })
        
        if result.get("status") == "error":
            return f"Error running script: {result.get('message', 'Unknown error')}"
        
        script_result = result.get("result", "Script executed successfully")
        return f"Python script result: {script_result}"
        
    except Exception as e:
        logger.error(f"Error in run_python_script: {str(e)}")
        return f"Error running Python script: {str(e)}"

# ============================================================================
# ENHANCED INFORMATION TOOLS
# ============================================================================

@app.tool()
async def get_script_info() -> str:
    """
    Get comprehensive information about the current Nuke script.
    """
    try:
        logger.info("Getting script information")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("get_script_info", {})
        
        if result.get("status") == "error":
            return f"Error getting script info: {result.get('message', 'Unknown error')}"
        
        info = []
        info.append(f"Script: {result.get('script_name', 'Untitled')}")
        info.append(f"Nodes: {result.get('node_count', 0)}")
        info.append(f"Frame range: {result.get('first_frame', 1)}-{result.get('last_frame', 100)}")
        info.append(f"Current frame: {result.get('current_frame', 1)}")
        info.append(f"FPS: {result.get('fps', 24)}")
        info.append(f"Resolution: {result.get('width', 1920)}x{result.get('height', 1080)}")
        info.append(f"Pixel aspect: {result.get('pixel_aspect', 1.0)}")
        info.append(f"Modified: {'Yes' if result.get('modified', False) else 'No'}")
        
        return "\n".join(info)
        
    except Exception as e:
        logger.error(f"Error in get_script_info: {str(e)}")
        return f"Error getting script info: {str(e)}"

@app.tool()
async def list_nodes(
    filter_type: Optional[str] = None,
    selected_only: bool = False
) -> str:
    """
    List all nodes in the current script, optionally filtered by type.
    
    Args:
        filter_type: Optional node type to filter by (e.g., 'Read', 'Write')
        selected_only: Whether to list only selected nodes
    """
    try:
        logger.info("Listing nodes")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("list_nodes", {
            "filter_type": filter_type,
            "selected_only": selected_only
        })
        
        if result.get("status") == "error":
            return f"Error listing nodes: {result.get('message', 'Unknown error')}"
        
        nodes = result.get("nodes", [])
        if not nodes:
            return "No nodes found in the script"
        
        node_info = []
        for node in nodes:
            node_info.append(f"- {node['name']} ({node['class']}) at ({node['xpos']}, {node['ypos']})")
        
        filter_text = f" (filtered by {filter_type})" if filter_type else ""
        selected_text = " (selected only)" if selected_only else ""
        
        return f"Nodes in script{filter_text}{selected_text}:\n" + "\n".join(node_info)
        
    except Exception as e:
        logger.error(f"Error in list_nodes: {str(e)}")
        return f"Error listing nodes: {str(e)}"

@app.tool()
async def get_node_info(node_name: str) -> str:
    """
    Get detailed information about a specific node.
    
    Args:
        node_name: Name of the node to inspect
    """
    try:
        logger.info(f"Getting info for node: {node_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("get_node_info", {
            "node_name": node_name
        })
        
        if result.get("status") == "error":
            return f"Error getting node info: {result.get('message', 'Unknown error')}"
        
        node = result.get("node", {})
        if not node:
            return f"Node '{node_name}' not found"
        
        info = []
        info.append(f"Name: {node.get('name', 'Unknown')}")
        info.append(f"Class: {node.get('class', 'Unknown')}")
        info.append(f"Position: ({node.get('xpos', 0)}, {node.get('ypos', 0)})")
        info.append(f"Selected: {'Yes' if node.get('selected', False) else 'No'}")
        info.append(f"Inputs: {node.get('inputs', 0)}")
        info.append(f"Output: {node.get('output', 'Unknown')}")
        
        # Add knob information if available
        knobs = node.get("knobs", {})
        if knobs:
            info.append("Key Knobs:")
            for knob_name, knob_value in list(knobs.items())[:10]:  # Show first 10 knobs
                info.append(f"  {knob_name}: {knob_value}")
            if len(knobs) > 10:
                info.append(f"  ... and {len(knobs) - 10} more knobs")
        
        return "\n".join(info)
        
    except Exception as e:
        logger.error(f"Error in get_node_info: {str(e)}")
        return f"Error getting node info: {str(e)}"

# ============================================================================
# RENDERING AND EXECUTION TOOLS
# ============================================================================

@app.tool()
async def render(
    write_node_name: str,
    frame_range: Optional[str] = None,
    proxy_mode: bool = False,
    use_gpu: bool = True
) -> str:
    """
    Render frames using a Write node with enhanced options.
    
    Args:
        write_node_name: Name of the Write node to render
        frame_range: Frame range to render (e.g., '1-100', '1,10,20-30')
        proxy_mode: Whether to render in proxy mode
        use_gpu: Whether to use GPU acceleration if available
    """
    try:
        logger.info(f"Starting render for Write node: {write_node_name}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("render", {
            "write_node_name": write_node_name,
            "frame_range": frame_range,
            "proxy_mode": proxy_mode,
            "use_gpu": use_gpu
        })
        
        if result.get("status") == "error":
            return f"Error during render: {result.get('message', 'Unknown error')}"
        
        frames_rendered = result.get("frames_rendered", 0)
        render_time = result.get("render_time", "Unknown")
        output_path = result.get("output_path", "Unknown")
        
        return f"Render completed. Frames: {frames_rendered}, Time: {render_time}, Output: {output_path}"
        
    except Exception as e:
        logger.error(f"Error in render: {str(e)}")
        return f"Error during render: {str(e)}"

@app.tool()
async def viewer_playback(
    action: str,
    start_frame: Optional[int] = None,
    end_frame: Optional[int] = None,
    fps: Optional[float] = None
) -> str:
    """
    Control Viewer playback with enhanced options.
    
    Args:
        action: Playback action ('play', 'stop', 'pause', 'step_forward', 'step_back', 'goto')
        start_frame: Optional start frame for playback range
        end_frame: Optional end frame for playback range
        fps: Optional playback FPS override
    """
    try:
        logger.info(f"Viewer playback action: {action}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("viewer_playback", {
            "action": action,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "fps": fps
        })
        
        if result.get("status") == "error":
            return f"Error in playback: {result.get('message', 'Unknown error')}"
        
        current_frame = result.get("current_frame", "Unknown")
        playback_state = result.get("playback_state", "Unknown")
        
        return f"Playback {action} executed. Current frame: {current_frame}, State: {playback_state}"
        
    except Exception as e:
        logger.error(f"Error in viewer_playback: {str(e)}")
        return f"Error controlling playback: {str(e)}"

# ============================================================================
# UTILITY TOOLS
# ============================================================================

@app.tool()
async def auto_layout_nodes(
    selected_only: bool = False,
    layout_type: str = "vertical"
) -> str:
    """
    Automatically arrange nodes in the node graph.
    
    Args:
        selected_only: Whether to layout only selected nodes
        layout_type: Layout type ('vertical', 'horizontal', 'tree', 'grid')
    """
    try:
        logger.info(f"Auto-laying out nodes: {layout_type}")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("auto_layout_nodes", {
            "selected_only": selected_only,
            "layout_type": layout_type
        })
        
        if result.get("status") == "error":
            return f"Error in auto layout: {result.get('message', 'Unknown error')}"
        
        nodes_arranged = result.get("nodes_arranged", 0)
        return f"Auto-arranged {nodes_arranged} nodes using {layout_type} layout"
        
    except Exception as e:
        logger.error(f"Error in auto_layout_nodes: {str(e)}")
        return f"Error in auto layout: {str(e)}"

@app.tool()
async def create_group(
    name: str,
    node_names: List[str],
    color: Optional[int] = None
) -> str:
    """
    Create a group node containing the specified nodes.
    
    Args:
        name: Name for the group node
        node_names: List of node names to include in the group
        color: Optional color index for the group node
    """
    try:
        logger.info(f"Creating group '{name}' with {len(node_names)} nodes")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("create_group", {
            "name": name,
            "node_names": node_names,
            "color": color
        })
        
        if result.get("status") == "error":
            return f"Error creating group: {result.get('message', 'Unknown error')}"
        
        group_name = result.get("group_name", name)
        return f"Created group '{group_name}' containing {len(node_names)} nodes"
        
    except Exception as e:
        logger.error(f"Error in create_group: {str(e)}")
        return f"Error creating group: {str(e)}"

@app.tool()
async def create_live_group(
    name: str,
    node_names: List[str],
    file_path: str,
    auto_publish: bool = False
) -> str:
    """
    Create a LiveGroup node for collaborative work.
    
    Args:
        name: Name for the LiveGroup node
        node_names: List of node names to include
        file_path: Path where to save the LiveGroup file
        auto_publish: Whether to automatically publish changes
    """
    try:
        logger.info(f"Creating LiveGroup '{name}' with {len(node_names)} nodes")
        nuke = get_nuke_connection()
        
        result = nuke.send_command("create_live_group", {
            "name": name,
            "node_names": node_names,
            "file_path": file_path,
            "auto_publish": auto_publish
        })
        
        if result.get("status") == "error":
            return f"Error creating LiveGroup: {result.get('message', 'Unknown error')}"
        
        livegroup_name = result.get("livegroup_name", name)
        return f"Created LiveGroup '{livegroup_name}' saved to {file_path}"
        
    except Exception as e:
        logger.error(f"Error in create_live_group: {str(e)}")
        return f"Error creating LiveGroup: {str(e)}"

# ============================================================================
# SERVER INITIALIZATION
# ============================================================================

async def main():
    """Main function to run the enhanced MCP server."""
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream, 
            InitializationOptions(
                server_name="enhanced-nuke-mcp",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())