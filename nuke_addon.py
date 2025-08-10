"""
Nuke MCP Addon - Run this script in Nuke's Script Editor
This creates a server that listens for commands from Claude
"""

import nuke
import socket
import threading
import json

class NukeMCPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
    def start_server(self):
        """Start the TCP server to listen for Claude commands"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True
            
            print(f"🚀 Nuke MCP Server started on {self.host}:{self.port}")
            print("Claude can now control Nuke!")
            
            while self.running:
                try:
                    client, addr = self.socket.accept()
                    data = client.recv(4096).decode('utf-8')
                    
                    if data:
                        command = json.loads(data)
                        response = self.handle_command(command)
                        client.send(json.dumps(response).encode('utf-8'))
                    
                    client.close()
                except Exception as e:
                    if self.running:
                        print(f"Server error: {e}")
                        
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
    
    def handle_command(self, command):
        """Handle commands from Claude"""
        try:
            cmd_type = command.get('type')
            
            if cmd_type == 'create_node':
                return self.create_node(command)
            elif cmd_type == 'get_scene_info':
                return self.get_scene_info()
            elif cmd_type == 'execute_code':
                return self.execute_code(command)
            else:
                return {"error": f"Unknown command: {cmd_type}"}
                
        except Exception as e:
            return {"error": f"Command failed: {str(e)}"}
    
    def create_node(self, command):
        """Create a node in Nuke"""
        node_type = command.get('node_type', 'NoOp')
        params = command.get('params', {})
        
        try:
            node = nuke.createNode(node_type)
            
            # Set node parameters
            for param, value in params.items():
                if node.knob(param):
                    node[param].setValue(value)
            
            return {"status": "success", "message": f"Created {node_type} node: {node.name()}"}
        except Exception as e:
            return {"error": f"Failed to create node: {str(e)}"}
    
    def get_scene_info(self):
        """Get information about current Nuke scene"""
        try:
            nodes = []
            for node in nuke.allNodes():
                nodes.append({
                    "name": node.name(),
                    "type": node.Class(),
                    "selected": node.isSelected()
                })
            
            return {
                "status": "success",
                "scene_info": {
                    "script_name": nuke.root().name(),
                    "total_nodes": len(nodes),
                    "nodes": nodes[:10]  # First 10 nodes
                }
            }
        except Exception as e:
            return {"error": f"Failed to get scene info: {str(e)}"}
    
    def execute_code(self, command):
        """Execute Python code in Nuke"""
        code = command.get('code', '')
        
        try:
            exec(code)
            return {"status": "success", "message": "Code executed successfully"}
        except Exception as e:
            return {"error": f"Code execution failed: {str(e)}"}
    
    def stop_server(self):
        """Stop the server"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("🛑 Nuke MCP Server stopped")

# Global server instance
nuke_mcp_server = None

def start_nuke_mcp():
    """Start the Nuke MCP server - Call this function"""
    global nuke_mcp_server
    
    if nuke_mcp_server is None:
        nuke_mcp_server = NukeMCPServer()
        thread = threading.Thread(target=nuke_mcp_server.start_server)
        thread.daemon = True
        thread.start()
        
        # Create a simple UI panel
        try:
            panel = nuke.Panel("Nuke MCP")
            panel.addSingleLineInput("Status:", "Server Running on localhost:8080")
            panel.addButton("Stop Server")
            panel.show()
        except:
            pass  # UI creation failed, but server still works
            
    else:
        print("⚠️  Server already running!")

def stop_nuke_mcp():
    """Stop the Nuke MCP server"""
    global nuke_mcp_server
    
    if nuke_mcp_server:
        nuke_mcp_server.stop_server()
        nuke_mcp_server = None
    else:
        print("⚠️  Server not running!")

# Instructions for users
print("""
🎬 NUKE MCP ADDON LOADED!

To start the server, run this in Nuke's Script Editor:
    start_nuke_mcp()

To stop the server:
    stop_nuke_mcp()

Once running, Claude can control your Nuke session!
""")

# Uncomment the next line to auto-start the server
# start_nuke_mcp()