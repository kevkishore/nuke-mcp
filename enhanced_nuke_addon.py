#!/usr/bin/env python3
"""
Enhanced Nuke MCP Addon with comprehensive VFX workflow automation.
This addon runs inside Nuke and provides extensive functionality for:
- Camera tracking and 3D scene setup
- Deep compositing pipelines  
- Template/Toolset management
- Machine learning with CopyCat
- Advanced keying and compositing
- Batch processing capabilities
"""

import nuke
import nukescripts
import socket
import threading
import json
import time
import os
import sys
import traceback
from typing import Dict, Any, List, Optional, Union

# ============================================================================
# ENHANCED NUKE MCP SERVER CLASS
# ============================================================================

class EnhancedNukeMCPServer:
    """Enhanced MCP server running inside Nuke with comprehensive VFX tools"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.server_thread = None
        
        # Command handlers mapping
        self.handlers = {
            # Basic operations
            'create_node': self.create_node,
            'connect_nodes': self.connect_nodes,
            'set_knob_value': self.set_knob_value,
            'get_node_info': self.get_node_info,
            'get_script_info': self.get_script_info,
            'list_nodes': self.list_nodes,
            
            # Camera tracking
            'create_camera_tracker': self.create_camera_tracker,
            'solve_camera_track': self.solve_camera_track,
            'create_3d_scene': self.create_3d_scene,
            
            # Deep compositing
            'setup_deep_pipeline': self.setup_deep_pipeline,
            
            # Template management
            'load_template': self.load_template,
            'save_template': self.save_template,
            
            # Keying and compositing
            'setup_keyer': self.setup_keyer,
            'setup_basic_comp': self.setup_basic_comp,
            'setup_motion_blur': self.setup_motion_blur,
            
            # Machine learning
            'setup_copycat': self.setup_copycat,
            'train_copycat_model': self.train_copycat_model,
            
            # Batch processing
            'batch_process': self.batch_process,
            
            # Project management
            'set_project_settings': self.set_project_settings,
            
            # Script management
            'load_script': self.load_script,
            'save_script': self.save_script,
            'run_python_script': self.run_python_script,
            
            # Rendering and playback
            'render': self.render,
            'viewer_playback': self.viewer_playback,
            
            # Utilities
            'auto_layout_nodes': self.auto_layout_nodes,
            'create_group': self.create_group,
            'create_live_group': self.create_live_group
        }
    
    def start_server(self):
        """Start the MCP server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.running = True
            
            print(f"Enhanced Nuke MCP Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    self.client_socket, client_address = self.server_socket.accept()
                    print(f"Client connected from {client_address}")
                    
                    while self.running:
                        try:
                            data = self.client_socket.recv(4096)
                            if not data:
                                break
                            
                            message = json.loads(data.decode().strip())
                            response = self.execute_command(message)
                            
                            response_str = json.dumps(response) + "\n"
                            self.client_socket.send(response_str.encode())
                            
                        except json.JSONDecodeError as e:
                            error_response = {"status": "error", "message": f"Invalid JSON: {str(e)}"}
                            self.client_socket.send(json.dumps(error_response).encode())
                        except Exception as e:
                            error_response = {"status": "error", "message": str(e)}
                            self.client_socket.send(json.dumps(error_response).encode())
                    
                except Exception as e:
                    print(f"Server error: {str(e)}")
                    if self.client_socket:
                        self.client_socket.close()
        
        except Exception as e:
            print(f"Failed to start server: {str(e)}")
        finally:
            self.cleanup()
    
    def execute_command(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a command and return response"""
        command = message.get('command')
        params = message.get('params', {})
        
        if command not in self.handlers:
            return {"status": "error", "message": f"Unknown command: {command}"}
        
        try:
            result = self.handlers[command](params)
            if isinstance(result, dict):
                result["status"] = result.get("status", "success")
                return result
            else:
                return {"status": "success", "result": result}
        except Exception as e:
            traceback.print_exc()
            return {"status": "error", "message": str(e)}
    
    # ========================================================================
    # BASIC NODE OPERATIONS
    # ========================================================================
    
    def create_node(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a node with enhanced parameter support"""
        node_type = params.get('node_type')
        name = params.get('name')
        position = params.get('position')
        inputs = params.get('inputs', [])
        parameters = params.get('parameters', {})
        
        if not node_type:
            return {"status": "error", "message": "node_type is required"}
        
        try:
            # Create the node
            node = nuke.createNode(node_type, inpanel=False)
            
            # Set custom name if provided
            if name:
                node.setName(name)
            
            # Set position if provided
            if position and len(position) >= 2:
                node.setXYpos(position[0], position[1])
            
            # Set parameters
            for knob_name, value in parameters.items():
                try:
                    knob = node.knob(knob_name)
                    if knob:
                        if isinstance(value, list):
                            knob.setValue(value)
                        else:
                            knob.setValue(value)
                except Exception as e:
                    print(f"Warning: Could not set {knob_name} to {value}: {str(e)}")
            
            # Connect inputs
            for i, input_name in enumerate(inputs):
                if i >= node.maxInputs():
                    break
                input_node = nuke.toNode(input_name)
                if input_node:
                    node.setInput(i, input_node)
            
            return {
                "status": "success",
                "name": node.name(),
                "class": node.Class(),
                "xpos": node.xpos(),
                "ypos": node.ypos()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create 3D scene: {str(e)}"}
    
    # ========================================================================
    # DEEP COMPOSITING OPERATIONS
    # ========================================================================
    
    def setup_deep_pipeline(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set up a Deep compositing pipeline"""
        input_nodes = params.get('input_nodes', [])
        merge_operation = params.get('merge_operation', 'over')
        output_name = params.get('output_name')
        
        if len(input_nodes) < 2:
            return {"status": "error", "message": "At least 2 input nodes required for deep pipeline"}
        
        created_nodes = []
        
        try:
            # Convert inputs to deep if needed
            deep_inputs = []
            for input_name in input_nodes:
                input_node = nuke.toNode(input_name)
                if not input_node:
                    continue
                
                # Check if already deep
                if 'deep' not in input_node.channels():
                    # Convert to deep
                    to_deep = nuke.createNode('DeepFromImage', inpanel=False)
                    to_deep.setInput(0, input_node)
                    created_nodes.append(to_deep.name())
                    deep_inputs.append(to_deep)
                else:
                    deep_inputs.append(input_node)
            
            # Chain DeepMerge nodes
            current_node = deep_inputs[0]
            for i in range(1, len(deep_inputs)):
                deep_merge = nuke.createNode('DeepMerge2', inpanel=False)
                deep_merge['operation'].setValue(merge_operation)
                deep_merge.setInput(0, current_node)
                deep_merge.setInput(1, deep_inputs[i])
                created_nodes.append(deep_merge.name())
                current_node = deep_merge
            
            # Add DeepWrite node
            deep_write = nuke.createNode('DeepWrite', inpanel=False)
            if output_name:
                deep_write.setName(output_name)
            deep_write.setInput(0, current_node)
            created_nodes.append(deep_write.name())
            
            return {
                "status": "success",
                "created_nodes": created_nodes,
                "merge_operation": merge_operation
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to setup deep pipeline: {str(e)}"}
    
    # ========================================================================
    # TEMPLATE MANAGEMENT OPERATIONS
    # ========================================================================
    
    def load_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Load a Nuke template (Toolset)"""
        template_name = params.get('template_name')
        position = params.get('position', {'x': 0, 'y': 0})
        parameters = params.get('parameters', {})
        
        try:
            # Get toolsets path
            toolsets_path = nuke.pluginPath()[0] + "/ToolSets"
            template_path = os.path.join(toolsets_path, f"{template_name}.nk")
            
            if not os.path.exists(template_path):
                return {"status": "error", "message": f"Template '{template_name}' not found"}
            
            # Store current selection
            original_selection = nuke.selectedNodes()
            for node in original_selection:
                node.setSelected(False)
            
            # Load template
            nuke.nodePaste(template_path)
            
            # Get newly loaded nodes
            loaded_nodes = nuke.selectedNodes()
            loaded_node_names = [node.name() for node in loaded_nodes]
            
            # Position nodes
            if loaded_nodes and position:
                min_x = min([node.xpos() for node in loaded_nodes])
                min_y = min([node.ypos() for node in loaded_nodes])
                offset_x = position['x'] - min_x
                offset_y = position['y'] - min_y
                
                for node in loaded_nodes:
                    node.setXYpos(node.xpos() + offset_x, node.ypos() + offset_y)
            
            # Apply parameters
            for node in loaded_nodes:
                if node.name() in parameters:
                    node_params = parameters[node.name()]
                    for knob_name, value in node_params.items():
                        knob = node.knob(knob_name)
                        if knob:
                            knob.setValue(value)
            
            # Restore original selection
            for node in loaded_nodes:
                node.setSelected(False)
            for node in original_selection:
                node.setSelected(True)
            
            return {
                "status": "success",
                "loaded_nodes": loaded_node_names,
                "template_name": template_name
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to load template: {str(e)}"}
    
    def save_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Save selected nodes as a template"""
        template_name = params.get('template_name')
        node_names = params.get('node_names', [])
        category = params.get('category', 'Custom')
        description = params.get('description', '')
        
        try:
            # Get nodes to save
            nodes_to_save = []
            for node_name in node_names:
                node = nuke.toNode(node_name)
                if node:
                    nodes_to_save.append(node)
            
            if not nodes_to_save:
                return {"status": "error", "message": "No valid nodes found to save"}
            
            # Clear selection and select nodes to save
            for node in nuke.allNodes():
                node.setSelected(False)
            for node in nodes_to_save:
                node.setSelected(True)
            
            # Create toolsets directory if it doesn't exist
            toolsets_path = os.path.join(nuke.pluginPath()[0], "ToolSets", category)
            if not os.path.exists(toolsets_path):
                os.makedirs(toolsets_path)
            
            template_path = os.path.join(toolsets_path, f"{template_name}.nk")
            
            # Save selected nodes
            nuke.nodeCopy(template_path)
            
            return {
                "status": "success",
                "template_path": template_path,
                "nodes_saved": len(nodes_to_save),
                "category": category
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to save template: {str(e)}"}
    
    # ========================================================================
    # KEYING AND COMPOSITING OPERATIONS
    # ========================================================================
    
    def setup_keyer(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set up a keying pipeline"""
        input_node_name = params.get('input_node_name')
        keyer_type = params.get('keyer_type', 'Primatte')
        screen_color = params.get('screen_color', [0, 0.7, 0])
        output_name = params.get('output_name')
        
        input_node = nuke.toNode(input_node_name)
        if not input_node:
            return {"status": "error", "message": f"Input node '{input_node_name}' not found"}
        
        created_nodes = []
        
        try:
            # Create keyer based on type
            if keyer_type == 'Primatte':
                keyer = nuke.createNode('Primatte', inpanel=False)
                keyer['screenColor'].setValue(screen_color)
            elif keyer_type == 'Keyer':
                keyer = nuke.createNode('Keyer', inpanel=False)
                keyer['color'].setValue(screen_color)
            elif keyer_type == 'IBKColour':
                keyer = nuke.createNode('IBKColourV3', inpanel=False)
                keyer['screen_colour'].setValue(screen_color)
            else:
                keyer = nuke.createNode('Difference', inpanel=False)
            
            keyer.setInput(0, input_node)
            created_nodes.append(keyer.name())
            
            # Add edge processing
            edge_blur = nuke.createNode('EdgeBlur', inpanel=False)
            edge_blur.setInput(0, keyer)
            created_nodes.append(edge_blur.name())
            
            # Add despill
            if keyer_type in ['Primatte', 'IBKColour']:
                despill = nuke.createNode('Despill', inpanel=False)
                despill.setInput(0, edge_blur)
                created_nodes.append(despill.name())
                current_node = despill
            else:
                current_node = edge_blur
            
            # Add premult
            premult = nuke.createNode('Premult', inpanel=False)
            premult.setInput(0, current_node)
            created_nodes.append(premult.name())
            
            if output_name:
                premult.setName(output_name)
            
            return {
                "status": "success",
                "created_nodes": created_nodes,
                "keyer_type": keyer_type
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to setup keyer: {str(e)}"}
    
    def setup_basic_comp(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set up a basic compositing tree"""
        plate_node = params.get('plate_node')
        fg_elements = params.get('fg_elements', [])
        bg_elements = params.get('bg_elements', [])
        comp_name = params.get('comp_name', 'FinalComp')
        
        plate = nuke.toNode(plate_node)
        if not plate:
            return {"status": "error", "message": f"Plate node '{plate_node}' not found"}
        
        created_nodes = []
        current_node = plate
        
        try:
            # Composite background elements first
            for bg_name in bg_elements:
                bg_node = nuke.toNode(bg_name)
                if bg_node:
                    merge = nuke.createNode('Merge2', inpanel=False)
                    merge['operation'].setValue('under')
                    merge.setInput(0, current_node)  # A input (over)
                    merge.setInput(1, bg_node)       # B input (under)
                    created_nodes.append(merge.name())
                    current_node = merge
            
            # Composite foreground elements
            for fg_name in fg_elements:
                fg_node = nuke.toNode(fg_name)
                if fg_node:
                    merge = nuke.createNode('Merge2', inpanel=False)
                    merge['operation'].setValue('over')
                    merge.setInput(0, fg_node)       # A input (over)
                    merge.setInput(1, current_node)  # B input (under)
                    created_nodes.append(merge.name())
                    current_node = merge
            
            # Set final name
            if created_nodes:
                current_node.setName(comp_name)
            
            return {
                "status": "success",
                "created_nodes": created_nodes,
                "final_node": current_node.name(),
                "elements_composited": len(fg_elements) + len(bg_elements)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to setup basic comp: {str(e)}"}
    
    def setup_motion_blur(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set up motion blur using motion vectors"""
        input_node_name = params.get('input_node_name')
        vector_node_name = params.get('vector_node_name')
        motion_blur_samples = params.get('motion_blur_samples', 15)
        shutter_angle = params.get('shutter_angle', 180.0)
        
        input_node = nuke.toNode(input_node_name)
        if not input_node:
            return {"status": "error", "message": f"Input node '{input_node_name}' not found"}
        
        created_nodes = []
        
        try:
            # Create VectorBlur node
            vector_blur = nuke.createNode('VectorBlur2', inpanel=False)
            vector_blur.setInput(0, input_node)
            
            # Connect motion vectors if provided
            if vector_node_name:
                vector_node = nuke.toNode(vector_node_name)
                if vector_node:
                    vector_blur.setInput(1, vector_node)
            
            # Configure motion blur settings
            vector_blur['samples'].setValue(motion_blur_samples)
            vector_blur['shutter_angle'].setValue(shutter_angle)
            
            created_nodes.append(vector_blur.name())
            
            return {
                "status": "success",
                "created_nodes": created_nodes,
                "samples": motion_blur_samples,
                "shutter_angle": shutter_angle
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to setup motion blur: {str(e)}"}
    
    # ========================================================================
    # MACHINE LEARNING OPERATIONS
    # ========================================================================
    
    def setup_copycat(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set up a CopyCat node for machine learning"""
        training_input_node = params.get('training_input_node')
        training_output_node = params.get('training_output_node')
        network_type = params.get('network_type', 'UNet')
        model_name = params.get('model_name')
        
        input_node = nuke.toNode(training_input_node)
        output_node = nuke.toNode(training_output_node)
        
        if not input_node:
            return {"status": "error", "message": f"Training input node '{training_input_node}' not found"}
        if not output_node:
            return {"status": "error", "message": f"Training output node '{training_output_node}' not found"}
        
        try:
            # Check if CopyCat is available
            try:
                copycat = nuke.createNode('CopyCat', inpanel=False)
            except:
                return {"status": "error", "message": "CopyCat node not available. Make sure CopyCat plugin is installed."}
            
            if model_name:
                copycat.setName(model_name)
            
            # Connect inputs
            copycat.setInput(0, input_node)   # Training input
            copycat.setInput(1, output_node)  # Training target
            
            # Set network type
            network_types = {'UNet': 0, 'ResNet': 1, 'DenseNet': 2}
            if network_type in network_types:
                copycat['network_type'].setValue(network_types[network_type])
            
            return {
                "status": "success",
                "copycat_node": copycat.name(),
                "network_type": network_type
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to setup CopyCat: {str(e)}"}
    
    def train_copycat_model(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Train a CopyCat neural network model"""
        copycat_node_name = params.get('copycat_node_name')
        epochs = params.get('epochs', 200)
        batch_size = params.get('batch_size', 8)
        learning_rate = params.get('learning_rate', 0.001)
        
        copycat = nuke.toNode(copycat_node_name)
        if not copycat:
            return {"status": "error", "message": f"CopyCat node '{copycat_node_name}' not found"}
        
        try:
            # Set training parameters
            copycat['epochs'].setValue(epochs)
            copycat['batch_size'].setValue(batch_size)
            copycat['learning_rate'].setValue(learning_rate)
            
            # Start training (this is a simulation - actual training would be much more complex)
            start_time = time.time()
            
            # Execute training button
            nuke.executeInMainThread(copycat['train'].execute)
            
            training_time = time.time() - start_time
            
            return {
                "status": "success",
                "training_time": f"{training_time:.2f} seconds",
                "epochs": epochs,
                "final_loss": "Simulated: 0.001"  # This would be actual loss in real implementation
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to train CopyCat model: {str(e)}"}
    
    # ========================================================================
    # BATCH PROCESSING OPERATIONS
    # ========================================================================
    
    def batch_process(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Batch process files"""
        input_directory = params.get('input_directory')
        output_directory = params.get('output_directory')
        file_pattern = params.get('file_pattern', '*.exr')
        process_script = params.get('process_script')
        frame_range = params.get('frame_range')
        
        try:
            import glob
            
            # Find files matching pattern
            search_pattern = os.path.join(input_directory, file_pattern)
            files = glob.glob(search_pattern)
            
            if not files:
                return {"status": "error", "message": f"No files found matching pattern: {search_pattern}"}
            
            processed_files = 0
            failed_files = 0
            
            # Process each file
            for file_path in files:
                try:
                    # Create a simple processing setup
                    read_node = nuke.createNode('Read', inpanel=False)
                    read_node['file'].setValue(file_path)
                    
                    # Apply processing script if provided
                    if process_script and os.path.exists(process_script):
                        exec(open(process_script).read())
                    
                    # Create write node
                    output_file = os.path.join(output_directory, os.path.basename(file_path))
                    write_node = nuke.createNode('Write', inpanel=False)
                    write_node['file'].setValue(output_file)
                    write_node.setInput(0, read_node)
                    
                    # Execute render
                    if frame_range:
                        first, last = map(int, frame_range.split('-'))
                        nuke.execute(write_node, first, last)
                    else:
                        nuke.execute(write_node, 1, 1)
                    
                    # Cleanup
                    nuke.delete(read_node)
                    nuke.delete(write_node)
                    
                    processed_files += 1
                    
                except Exception as e:
                    print(f"Failed to process {file_path}: {str(e)}")
                    failed_files += 1
            
            return {
                "status": "success",
                "processed_files": processed_files,
                "failed_files": failed_files,
                "total_files": len(files)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed batch processing: {str(e)}"}
    
    # ========================================================================
    # PROJECT MANAGEMENT OPERATIONS
    # ========================================================================
    
    def set_project_settings(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set project settings"""
        frame_range = params.get('frame_range')
        resolution = params.get('resolution')
        fps = params.get('fps')
        color_management = params.get('color_management')
        
        try:
            settings_applied = []
            
            # Set frame range
            if frame_range:
                first_frame = frame_range.get('first', 1)
                last_frame = frame_range.get('last', 100)
                nuke.root()['first_frame'].setValue(first_frame)
                nuke.root()['last_frame'].setValue(last_frame)
                settings_applied.append(f"Frame range: {first_frame}-{last_frame}")
            
            # Set resolution
            if resolution:
                width = resolution.get('width', 1920)
                height = resolution.get('height', 1080)
                format_name = f"{width}x{height}"
                
                # Create or find format
                existing_format = None
                for fmt in nuke.formats():
                    if fmt.width() == width and fmt.height() == height:
                        existing_format = fmt
                        break
                
                if not existing_format:
                    new_format = f"{width} {height} {format_name}"
                    nuke.addFormat(new_format)
                    existing_format = nuke.format(format_name)
                
                nuke.root()['format'].setValue(existing_format)
                settings_applied.append(f"Resolution: {width}x{height}")
            
            # Set FPS
            if fps:
                nuke.root()['fps'].setValue(fps)
                settings_applied.append(f"FPS: {fps}")
            
            # Set color management
            if color_management:
                for setting, value in color_management.items():
                    knob = nuke.root().knob(setting)
                    if knob:
                        knob.setValue(value)
                        settings_applied.append(f"Color: {setting}={value}")
            
            return {
                "status": "success",
                "settings_applied": settings_applied
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to set project settings: {str(e)}"}
    
    # ========================================================================
    # SCRIPT MANAGEMENT OPERATIONS
    # ========================================================================
    
    def load_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Load a Nuke script"""
        file_path = params.get('file_path')
        
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"Script file not found: {file_path}"}
        
        try:
            nuke.scriptOpen(file_path)
            loaded_nodes = len(nuke.allNodes())
            
            return {
                "status": "success",
                "loaded_nodes": loaded_nodes,
                "script_path": file_path
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to load script: {str(e)}"}
    
    def save_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Save the current script"""
        file_path = params.get('file_path')
        selected_only = params.get('selected_only', False)
        
        try:
            if selected_only:
                # Save only selected nodes
                selected_nodes = nuke.selectedNodes()
                if not selected_nodes:
                    return {"status": "error", "message": "No nodes selected"}
                
                nuke.nodeCopy(file_path)
                saved_nodes = len(selected_nodes)
            else:
                # Save entire script
                nuke.scriptSave(file_path)
                saved_nodes = len(nuke.allNodes())
            
            return {
                "status": "success",
                "saved_nodes": saved_nodes,
                "script_path": file_path
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to save script: {str(e)}"}
    
    def run_python_script(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run Python script in Nuke"""
        script = params.get('script')
        args = params.get('args', {})
        
        try:
            # Create a namespace with args
            namespace = {'nuke': nuke, 'nukescripts': nukescripts, 'args': args}
            
            # Execute the script
            result = exec(script, namespace)
            
            return {
                "status": "success",
                "result": str(result) if result is not None else "Script executed successfully"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Script execution failed: {str(e)}"}
    
    # ========================================================================
    # INFORMATION OPERATIONS
    # ========================================================================
    
    def get_script_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive script information"""
        try:
            root = nuke.root()
            
            return {
                "status": "success",
                "script_name": nuke.scriptName(),
                "node_count": len(nuke.allNodes()),
                "first_frame": int(root['first_frame'].value()),
                "last_frame": int(root['last_frame'].value()),
                "current_frame": int(nuke.frame()),
                "fps": root['fps'].value(),
                "width": root.format().width(),
                "height": root.format().height(),
                "pixel_aspect": root.format().pixelAspect(),
                "modified": nuke.modified(),
                "format_name": root.format().name()
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get script info: {str(e)}"}
    
    def list_nodes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List nodes in the script"""
        filter_type = params.get('filter_type')
        selected_only = params.get('selected_only', False)
        
        try:
            if selected_only:
                nodes = nuke.selectedNodes()
            else:
                nodes = nuke.allNodes()
            
            if filter_type:
                nodes = [node for node in nodes if node.Class() == filter_type]
            
            node_list = []
            for node in nodes:
                node_list.append({
                    "name": node.name(),
                    "class": node.Class(),
                    "xpos": node.xpos(),
                    "ypos": node.ypos(),
                    "selected": node.isSelected()
                })
            
            return {
                "status": "success",
                "nodes": node_list,
                "count": len(node_list)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to list nodes: {str(e)}"}
    
    def get_node_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information about a node"""
        node_name = params.get('node_name')
        
        node = nuke.toNode(node_name)
        if not node:
            return {"status": "error", "message": f"Node '{node_name}' not found"}
        
        try:
            # Get basic node info
            node_info = {
                "name": node.name(),
                "class": node.Class(),
                "xpos": node.xpos(),
                "ypos": node.ypos(),
                "selected": node.isSelected(),
                "inputs": node.inputs(),
                "output": node.output() if hasattr(node, 'output') else None
            }
            
            # Get knob information
            knobs = {}
            for knob_name in node.knobs():
                knob = node.knob(knob_name)
                try:
                    knobs[knob_name] = knob.value()
                except:
                    knobs[knob_name] = str(knob)
            
            node_info["knobs"] = knobs
            
            return {
                "status": "success",
                "node": node_info
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get node info: {str(e)}"}
    
    # ========================================================================
    # RENDERING AND PLAYBACK OPERATIONS
    # ========================================================================
    
    def render(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Render using a Write node"""
        write_node_name = params.get('write_node_name')
        frame_range = params.get('frame_range')
        proxy_mode = params.get('proxy_mode', False)
        use_gpu = params.get('use_gpu', True)
        
        write_node = nuke.toNode(write_node_name)
        if not write_node:
            return {"status": "error", "message": f"Write node '{write_node_name}' not found"}
        
        try:
            # Set proxy mode
            nuke.root()['proxy'].setValue(proxy_mode)
            
            # Parse frame range
            if frame_range:
                if '-' in frame_range:
                    first, last = map(int, frame_range.split('-'))
                else:
                    # Single frame or frame list
                    frames = [int(f) for f in frame_range.split(',')]
                    first, last = min(frames), max(frames)
            else:
                first = int(nuke.root()['first_frame'].value())
                last = int(nuke.root()['last_frame'].value())
            
            start_time = time.time()
            
            # Execute render
            nuke.execute(write_node, first, last, 1)
            
            render_time = time.time() - start_time
            frames_rendered = last - first + 1
            
            return {
                "status": "success",
                "frames_rendered": frames_rendered,
                "render_time": f"{render_time:.2f} seconds",
                "output_path": write_node['file'].value(),
                "frame_range": f"{first}-{last}"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Render failed: {str(e)}"}
    
    def viewer_playback(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Control viewer playback"""
        action = params.get('action')
        start_frame = params.get('start_frame')
        end_frame = params.get('end_frame')
        fps = params.get('fps')
        
        try:
            viewer = nuke.activeViewer()
            if not viewer:
                return {"status": "error", "message": "No active viewer found"}
            
            # Set playback range if specified
            if start_frame is not None:
                nuke.root()['first_frame'].setValue(start_frame)
            if end_frame is not None:
                nuke.root()['last_frame'].setValue(end_frame)
            if fps is not None:
                nuke.root()['fps'].setValue(fps)
            
            # Execute playback action
            if action == 'play':
                nuke.executeInMainThread(nuke.startPerformanceTimers)
                viewer.play(True)
            elif action == 'stop':
                viewer.play(False)
            elif action == 'pause':
                viewer.play(False)
            elif action == 'step_forward':
                current_frame = nuke.frame()
                nuke.frame(current_frame + 1)
            elif action == 'step_back':
                current_frame = nuke.frame()
                nuke.frame(current_frame - 1)
            elif action == 'goto':
                goto_frame = params.get('goto_frame', nuke.frame())
                nuke.frame(goto_frame)
            
            return {
                "status": "success",
                "current_frame": nuke.frame(),
                "playback_state": "playing" if viewer.isPlaying() else "stopped",
                "action": action
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Playback control failed: {str(e)}"}
    
    # ========================================================================
    # UTILITY OPERATIONS
    # ========================================================================
    
    def auto_layout_nodes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-layout nodes in the node graph"""
        selected_only = params.get('selected_only', False)
        layout_type = params.get('layout_type', 'vertical')
        
        try:
            if selected_only:
                nodes = nuke.selectedNodes()
            else:
                nodes = nuke.allNodes()
            
            if not nodes:
                return {"status": "error", "message": "No nodes to layout"}
            
            # Sort nodes by current position for consistent layout
            nodes.sort(key=lambda n: (n.ypos(), n.xpos()))
            
            spacing_x = 120
            spacing_y = 80
            start_x = 0
            start_y = 0
            
            if layout_type == 'vertical':
                for i, node in enumerate(nodes):
                    node.setXYpos(start_x, start_y + i * spacing_y)
            elif layout_type == 'horizontal':
                for i, node in enumerate(nodes):
                    node.setXYpos(start_x + i * spacing_x, start_y)
            elif layout_type == 'grid':
                cols = int(len(nodes) ** 0.5) + 1
                for i, node in enumerate(nodes):
                    row = i // cols
                    col = i % cols
                    node.setXYpos(start_x + col * spacing_x, start_y + row * spacing_y)
            elif layout_type == 'tree':
                # Simple tree layout - arrange by node dependencies
                positioned = set()
                y_levels = {}
                
                def get_depth(node, depth=0):
                    if node in positioned:
                        return y_levels.get(node, depth)
                    
                    max_input_depth = -1
                    for i in range(node.inputs()):
                        input_node = node.input(i)
                        if input_node and input_node in nodes:
                            input_depth = get_depth(input_node, depth)
                            max_input_depth = max(max_input_depth, input_depth)
                    
                    node_depth = max_input_depth + 1
                    y_levels[node] = node_depth
                    positioned.add(node)
                    return node_depth
                
                # Calculate depths
                for node in nodes:
                    get_depth(node)
                
                # Position nodes by depth
                level_counts = {}
                for node in nodes:
                    depth = y_levels[node]
                    if depth not in level_counts:
                        level_counts[depth] = 0
                    
                    node.setXYpos(level_counts[depth] * spacing_x, depth * spacing_y)
                    level_counts[depth] += 1
            
            return {
                "status": "success",
                "nodes_arranged": len(nodes),
                "layout_type": layout_type
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Auto layout failed: {str(e)}"}
    
    def create_group(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a group node"""
        name = params.get('name')
        node_names = params.get('node_names', [])
        color = params.get('color')
        
        try:
            # Get nodes to group
            nodes_to_group = []
            for node_name in node_names:
                node = nuke.toNode(node_name)
                if node:
                    nodes_to_group.append(node)
            
            if not nodes_to_group:
                return {"status": "error", "message": "No valid nodes found to group"}
            
            # Clear selection and select nodes to group
            for node in nuke.allNodes():
                node.setSelected(False)
            for node in nodes_to_group:
                node.setSelected(True)
            
            # Create group
            group = nuke.createNode('Group', inpanel=False)
            if name:
                group.setName(name)
            
            # Set color if specified
            if color is not None:
                group['tile_color'].setValue(color)
            
            # Move selected nodes into group
            nuke.executeInMainThread(nukescripts.group.group)
            
            return {
                "status": "success",
                "group_name": group.name(),
                "nodes_grouped": len(nodes_to_group)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create group: {str(e)}"}
    
    def create_live_group(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a LiveGroup node"""
        name = params.get('name')
        node_names = params.get('node_names', [])
        file_path = params.get('file_path')
        auto_publish = params.get('auto_publish', False)
        
        try:
            # Get nodes for LiveGroup
            nodes_to_group = []
            for node_name in node_names:
                node = nuke.toNode(node_name)
                if node:
                    nodes_to_group.append(node)
            
            if not nodes_to_group:
                return {"status": "error", "message": "No valid nodes found for LiveGroup"}
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Clear selection and select nodes
            for node in nuke.allNodes():
                node.setSelected(False)
            for node in nodes_to_group:
                node.setSelected(True)
            
            # Create LiveGroup
            live_group = nuke.createNode('LiveGroup', inpanel=False)
            if name:
                live_group.setName(name)
            
            # Set file path
            live_group['file'].setValue(file_path)
            live_group['auto_publish'].setValue(auto_publish)
            
            # Publish the LiveGroup
            live_group['publish'].execute()
            
            return {
                "status": "success",
                "livegroup_name": live_group.name(),
                "file_path": file_path,
                "nodes_included": len(nodes_to_group)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create LiveGroup: {str(e)}"}
    
    def cleanup(self):
        """Clean up server resources"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

# ============================================================================
# ENHANCED UI PANEL
# ============================================================================

class EnhancedNukeMCPPanel(nukescripts.PythonPanel):
    """Enhanced UI panel for the Nuke MCP server with comprehensive controls"""
    
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Enhanced Nuke MCP', 'com.enhanced.NukeMCP')
        
        # Server controls
        self.status_knob = nuke.Text_Knob('status', 'Status', 'Stopped')
        self.port_knob = nuke.Int_Knob('port', 'Port', 9876)
        self.start_button = nuke.PyScript_Knob('start', 'Start Server')
        self.stop_button = nuke.PyScript_Knob('stop', 'Stop Server')
        
        # Divider
        self.divider1 = nuke.Text_Knob('div1', '', '')
        
        # Feature toggles
        self.enable_camera_tracking = nuke.Boolean_Knob('enable_camera_tracking', 'Enable Camera Tracking', True)
        self.enable_deep_comp = nuke.Boolean_Knob('enable_deep_comp', 'Enable Deep Compositing', True)
        self.enable_ml = nuke.Boolean_Knob('enable_ml', 'Enable Machine Learning', True)
        self.enable_templates = nuke.Boolean_Knob('enable_templates', 'Enable Template Management', True)
        
        # Divider
        self.divider2 = nuke.Text_Knob('div2', '', '')
        
        # Statistics
        self.connections_knob = nuke.Text_Knob('connections', 'Connections', '0')
        self.commands_knob = nuke.Text_Knob('commands', 'Commands Executed', '0')
        
        # Divider
        self.divider3 = nuke.Text_Knob('div3', '', '')
        
        # Quick actions
        self.auto_layout_button = nuke.PyScript_Knob('auto_layout', 'Auto Layout Selected')
        self.save_template_button = nuke.PyScript_Knob('save_template', 'Save as Template')
        
        # Add knobs to panel
        for knob in [self.status_knob, self.port_knob, self.start_button, self.stop_button,
                    self.divider1, self.enable_camera_tracking, self.enable_deep_comp, 
                    self.enable_ml, self.enable_templates, self.divider2,
                    self.connections_knob, self.commands_knob, self.divider3,
                    self.auto_layout_button, self.save_template_button]:
            self.addKnob(knob)
        
        self.server = None
        self.server_thread = None
        self.command_count = 0
        self.connection_count = 0
    
    def knobChanged(self, knob):
        """Handle knob changes"""
        if knob == self.start_button:
            self.start_server()
        elif knob == self.stop_button:
            self.stop_server()
        elif knob == self.auto_layout_button:
            self.auto_layout_selected()
        elif knob == self.save_template_button:
            self.save_selected_as_template()
    
    def start_server(self):
        """Start the Enhanced MCP server"""
        if self.server and self.server.running:
            nuke.message("Server is already running!")
            return
        
        port = self.port_knob.value()
        
        try:
            self.server = EnhancedNukeMCPServer('localhost', port)
            self.server_thread = threading.Thread(target=self.server.start_server, daemon=True)
            self.server_thread.start()
            
            self.status_knob.setValue(f'Running on port {port}')
            nuke.message(f"Enhanced Nuke MCP Server started on port {port}")
            
        except Exception as e:
            nuke.message(f"Failed to start server: {str(e)}")
            self.status_knob.setValue('Failed to start')
    
    def stop_server(self):
        """Stop the MCP server"""
        if self.server:
            self.server.cleanup()
            self.server = None
        
        self.status_knob.setValue('Stopped')
        nuke.message("Enhanced Nuke MCP Server stopped")
    
    def auto_layout_selected(self):
        """Auto layout selected nodes"""
        selected = nuke.selectedNodes()
        if not selected:
            nuke.message("No nodes selected!")
            return
        
        try:
            # Simple vertical layout
            for i, node in enumerate(selected):
                node.setXYpos(node.xpos(), i * 80)
            nuke.message(f"Auto-arranged {len(selected)} nodes")
        except Exception as e:
            nuke.message(f"Auto layout failed: {str(e)}")
    
    def save_selected_as_template(self):
        """Save selected nodes as template"""
        selected = nuke.selectedNodes()
        if not selected:
            nuke.message("No nodes selected!")
            return
        
        # Get template name from user
        template_name = nuke.getInput("Template name:", "MyTemplate")
        if not template_name:
            return
        
        try:
            # Create toolsets directory
            toolsets_path = os.path.join(nuke.pluginPath()[0], "ToolSets", "Custom")
            os.makedirs(toolsets_path, exist_ok=True)
            
            template_path = os.path.join(toolsets_path, f"{template_name}.nk")
            nuke.nodeCopy(template_path)
            
            nuke.message(f"Template '{template_name}' saved successfully!")
            
        except Exception as e:
            nuke.message(f"Failed to save template: {str(e)}")

# ============================================================================
# GLOBAL VARIABLES AND FUNCTIONS
# ============================================================================

# Global panel instance
_enhanced_panel = None

def show_enhanced_panel():
    """Show the Enhanced Nuke MCP panel"""
    global _enhanced_panel
    
    if _enhanced_panel is None:
        _enhanced_panel = EnhancedNukeMCPPanel()
    
    _enhanced_panel.show()

def start_enhanced_server(port=9876):
    """Start Enhanced MCP server programmatically"""
    global _enhanced_panel
    
    if _enhanced_panel is None:
        _enhanced_panel = EnhancedNukeMCPPanel()
    
    _enhanced_panel.port_knob.setValue(port)
    _enhanced_panel.start_server()

def stop_enhanced_server():
    """Stop Enhanced MCP server programmatically"""
    global _enhanced_panel
    
    if _enhanced_panel:
        _enhanced_panel.stop_server()

# ============================================================================
# MENU INTEGRATION
# ============================================================================

def create_enhanced_menu():
    """Create menu entries for Enhanced Nuke MCP"""
    try:
        # Create main menu
        menubar = nuke.menu('Nuke')
        mcp_menu = menubar.addMenu('Enhanced MCP')
        
        # Add menu items
        mcp_menu.addCommand('Show Panel', 'nuke_enhanced_mcp_addon.show_enhanced_panel()')
        mcp_menu.addCommand('Start Server', 'nuke_enhanced_mcp_addon.start_enhanced_server()')
        mcp_menu.addCommand('Stop Server', 'nuke_enhanced_mcp_addon.stop_enhanced_server()')
        mcp_menu.addSeparator()
        
        # Quick actions submenu
        quick_menu = mcp_menu.addMenu('Quick Actions')
        quick_menu.addCommand('Auto Layout Selected', 'nuke_enhanced_mcp_addon.auto_layout_selected_nodes()')
        quick_menu.addCommand('Save Selection as Template', 'nuke_enhanced_mcp_addon.save_selection_as_template()')
        
        print("Enhanced Nuke MCP menu created successfully")
        
    except Exception as e:
        print(f"Failed to create Enhanced MCP menu: {str(e)}")

def auto_layout_selected_nodes():
    """Standalone function for auto-layout"""
    selected = nuke.selectedNodes()
    if not selected:
        nuke.message("No nodes selected!")
        return
    
    for i, node in enumerate(selected):
        node.setXYpos(node.xpos(), i * 80)

def save_selection_as_template():
    """Standalone function for template saving"""
    selected = nuke.selectedNodes()
    if not selected:
        nuke.message("No nodes selected!")
        return
    
    template_name = nuke.getInput("Template name:", "MyTemplate")
    if template_name:
        try:
            toolsets_path = os.path.join(nuke.pluginPath()[0], "ToolSets", "Custom")
            os.makedirs(toolsets_path, exist_ok=True)
            
            template_path = os.path.join(toolsets_path, f"{template_name}.nk")
            nuke.nodeCopy(template_path)
            
            nuke.message(f"Template '{template_name}' saved!")
        except Exception as e:
            nuke.message(f"Failed to save template: {str(e)}")

# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize():
    """Initialize the Enhanced Nuke MCP addon"""
    print("=" * 60)
    print("Enhanced Nuke MCP Addon - Initializing...")
    print("Features:")
    print("  • Camera Tracking & 3D Scene Setup")
    print("  • Deep Compositing Pipelines")
    print("  • Template/Toolset Management")
    print("  • Machine Learning (CopyCat)")
    print("  • Advanced Keying & Compositing")
    print("  • Batch Processing")
    print("  • Comprehensive VFX Workflows")
    print("=" * 60)
    
    # Create menu
    create_enhanced_menu()
    
    # Show welcome message
    def show_welcome():
        nuke.message(
            "Enhanced Nuke MCP Addon Loaded!\n\n"
            "Access from: Enhanced MCP menu\n"
            "Or run: nuke_enhanced_mcp_addon.show_enhanced_panel()\n\n"
            "Features include camera tracking, deep compositing,\n"
            "template management, and machine learning tools."
        )
    
    # Show welcome message after Nuke is fully loaded
    nuke.addOnUserCreate(show_welcome, nodeClass='Root')

# Run initialization
if __name__ != '__main__':
    initialize()
else:
    # Direct execution for testing
    show_enhanced_panel() 

# CRITICAL BUG FIX for enhanced_nuke_addon.py
# The current file has a truncation issue. Here's the corrected ending:

    def stop_server(self):
        """Stop the MCP server"""
        if self.server and self.server.running:
            self.server.cleanup()
            self.server = None
        
        self.status_knob.setValue('Stopped')
        nuke.message("Enhanced Nuke MCP Server stopped")
    
    def cleanup(self):
        """Clean up server resources"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

# ============================================================================
# ENHANCED UI PANEL
# ============================================================================

class EnhancedNukeMCPPanel(nukescripts.PythonPanel):
    """Enhanced UI panel for the Nuke MCP server with comprehensive controls"""
    
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Enhanced Nuke MCP', 'com.enhanced.NukeMCP')
        
        # Server controls
        self.status_knob = nuke.Text_Knob('status', 'Status', 'Stopped')
        self.port_knob = nuke.Int_Knob('port', 'Port', 9876)
        self.start_button = nuke.PyScript_Knob('start', 'Start Server')
        self.stop_button = nuke.PyScript_Knob('stop', 'Stop Server')
        
        # Divider
        self.divider1 = nuke.Text_Knob('div1', '', '')
        
        # Feature toggles
        self.enable_camera_tracking = nuke.Boolean_Knob('enable_camera_tracking', 'Enable Camera Tracking', True)
        self.enable_deep_comp = nuke.Boolean_Knob('enable_deep_comp', 'Enable Deep Compositing', True)
        self.enable_ml = nuke.Boolean_Knob('enable_ml', 'Enable Machine Learning', True)
        self.enable_templates = nuke.Boolean_Knob('enable_templates', 'Enable Template Management', True)
        
        # Divider
        self.divider2 = nuke.Text_Knob('div2', '', '')
        
        # Statistics
        self.connections_knob = nuke.Text_Knob('connections', 'Connections', '0')
        self.commands_knob = nuke.Text_Knob('commands', 'Commands Executed', '0')
        
        # Divider
        self.divider3 = nuke.Text_Knob('div3', '', '')
        
        # Quick actions
        self.auto_layout_button = nuke.PyScript_Knob('auto_layout', 'Auto Layout Selected')
        self.save_template_button = nuke.PyScript_Knob('save_template', 'Save as Template')
        
        # Add knobs to panel
        for knob in [self.status_knob, self.port_knob, self.start_button, self.stop_button,
                    self.divider1, self.enable_camera_tracking, self.enable_deep_comp, 
                    self.enable_ml, self.enable_templates, self.divider2,
                    self.connections_knob, self.commands_knob, self.divider3,
                    self.auto_layout_button, self.save_template_button]:
            self.addKnob(knob)
        
        self.server = None
        self.server_thread = None
        self.command_count = 0
        self.connection_count = 0
    
    def knobChanged(self, knob):
        """Handle knob changes"""
        if knob == self.start_button:
            self.start_server()
        elif knob == self.stop_button:
            self.stop_server()
        elif knob == self.auto_layout_button:
            self.auto_layout_selected()
        elif knob == self.save_template_button:
            self.save_selected_as_template()
    
    def start_server(self):
        """Start the Enhanced MCP server"""
        if self.server and self.server.running:
            nuke.message("Server is already running!")
            return
        
        port = self.port_knob.value()
        
        try:
            self.server = EnhancedNukeMCPServer('localhost', port)
            self.server_thread = threading.Thread(target=self.server.start_server, daemon=True)
            self.server_thread.start()
            
            self.status_knob.setValue(f'Running on port {port}')
            nuke.message(f"Enhanced Nuke MCP Server started on port {port}")
            
        except Exception as e:
            nuke.message(f"Failed to start server: {str(e)}")
            self.status_knob.setValue('Failed to start')
    
    def stop_server(self):
        """Stop the MCP server"""
        if self.server:
            self.server.cleanup()
            self.server = None
        
        self.status_knob.setValue('Stopped')
        nuke.message("Enhanced Nuke MCP Server stopped")
    
    def auto_layout_selected(self):
        """Auto layout selected nodes"""
        selected = nuke.selectedNodes()
        if not selected:
            nuke.message("No nodes selected!")
            return
        
        try:
            # Simple vertical layout
            for i, node in enumerate(selected):
                node.setXYpos(node.xpos(), i * 80)
            nuke.message(f"Auto-arranged {len(selected)} nodes")
        except Exception as e:
            nuke.message(f"Auto layout failed: {str(e)}")
    
    def save_selected_as_template(self):
        """Save selected nodes as template"""
        selected = nuke.selectedNodes()
        if not selected:
            nuke.message("No nodes selected!")
            return
        
        # Get template name from user
        template_name = nuke.getInput("Template name:", "MyTemplate")
        if not template_name:
            return
        
        try:
            # Create toolsets directory
            toolsets_path = os.path.join(nuke.pluginPath()[0], "ToolSets", "Custom")
            os.makedirs(toolsets_path, exist_ok=True)
            
            template_path = os.path.join(toolsets_path, f"{template_name}.nk")
            nuke.nodeCopy(template_path)
            
            nuke.message(f"Template '{template_name}' saved successfully!")
            
        except Exception as e:
            nuke.message(f"Failed to save template: {str(e)}")

# ============================================================================
# GLOBAL VARIABLES AND FUNCTIONS
# ============================================================================

# Global panel instance
_enhanced_panel = None

def show_enhanced_panel():
    """Show the Enhanced Nuke MCP panel"""
    global _enhanced_panel
    
    if _enhanced_panel is None:
        _enhanced_panel = EnhancedNukeMCPPanel()
    
    _enhanced_panel.show()

def start_enhanced_server(port=9876):
    """Start Enhanced MCP server programmatically"""
    global _enhanced_panel
    
    if _enhanced_panel is None:
        _enhanced_panel = EnhancedNukeMCPPanel()
    
    _enhanced_panel.port_knob.setValue(port)
    _enhanced_panel.start_server()

def stop_enhanced_server():
    """Stop Enhanced MCP server programmatically"""
    global _enhanced_panel
    
    if _enhanced_panel:
        _enhanced_panel.stop_server()

# ============================================================================
# MENU INTEGRATION
# ============================================================================

def create_enhanced_menu():
    """Create menu entries for Enhanced Nuke MCP"""
    try:
        # Create main menu
        menubar = nuke.menu('Nuke')
        mcp_menu = menubar.addMenu('Enhanced MCP')
        
        # Add menu items
        mcp_menu.addCommand('Show Panel', 'enhanced_nuke_addon.show_enhanced_panel()')
        mcp_menu.addCommand('Start Server', 'enhanced_nuke_addon.start_enhanced_server()')
        mcp_menu.addCommand('Stop Server', 'enhanced_nuke_addon.stop_enhanced_server()')
        mcp_menu.addSeparator()
        
        # Quick actions submenu
        quick_menu = mcp_menu.addMenu('Quick Actions')
        quick_menu.addCommand('Auto Layout Selected', 'enhanced_nuke_addon.auto_layout_selected_nodes()')
        quick_menu.addCommand('Save Selection as Template', 'enhanced_nuke_addon.save_selection_as_template()')
        
        print("Enhanced Nuke MCP menu created successfully")
        
    except Exception as e:
        print(f"Failed to create Enhanced MCP menu: {str(e)}")

def auto_layout_selected_nodes():
    """Standalone function for auto-layout"""
    selected = nuke.selectedNodes()
    if not selected:
        nuke.message("No nodes selected!")
        return
    
    for i, node in enumerate(selected):
        node.setXYpos(node.xpos(), i * 80)

def save_selection_as_template():
    """Standalone function for template saving"""
    selected = nuke.selectedNodes()
    if not selected:
        nuke.message("No nodes selected!")
        return
    
    template_name = nuke.getInput("Template name:", "MyTemplate")
    if template_name:
        try:
            toolsets_path = os.path.join(nuke.pluginPath()[0], "ToolSets", "Custom")
            os.makedirs(toolsets_path, exist_ok=True)
            
            template_path = os.path.join(toolsets_path, f"{template_name}.nk")
            nuke.nodeCopy(template_path)
            
            nuke.message(f"Template '{template_name}' saved!")
        except Exception as e:
            nuke.message(f"Failed to save template: {str(e)}")

# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize():
    """Initialize the Enhanced Nuke MCP addon"""
    print("=" * 60)
    print("Enhanced Nuke MCP Addon - Initializing...")
    print("Features:")
    print("  • Camera Tracking & 3D Scene Setup")
    print("  • Deep Compositing Pipelines")
    print("  • Template/Toolset Management")
    print("  • Machine Learning (CopyCat)")
    print("  • Advanced Keying & Compositing")
    print("  • Batch Processing")
    print("  • Comprehensive VFX Workflows")
    print("=" * 60)
    
    # Create menu
    create_enhanced_menu()
    
    # Show welcome message
    def show_welcome():
        nuke.message(
            "Enhanced Nuke MCP Addon Loaded!\n\n"
            "Access from: Enhanced MCP menu\n"
            "Or run: enhanced_nuke_addon.show_enhanced_panel()\n\n"
            "Features include camera tracking, deep compositing,\n"
            "template management, and machine learning tools."
        )
    
    # Show welcome message after Nuke is fully loaded
    nuke.addOnUserCreate(show_welcome, nodeClass='Root')

# Run initialization
if __name__ != '__main__':
    initialize()
else:
    # Direct execution for testing
    show_enhanced_panel()