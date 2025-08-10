
"""
Nuke MCP Addon (Portable Version) - Run in Nuke's Script Editor
Path-independent and works on any OS.
"""

import nuke
import socket
import threading
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class NukeMCPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def start_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True
            print(f"🚀 Nuke MCP Server started on {self.host}:{self.port}")

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
        node_type = command.get('node_type', 'NoOp')
        params = command.get('params', {})

        try:
            node = nuke.createNode(node_type)
            for param, value in params.items():
                if node.knob(param):
                    node[param].setValue(value)
            return {"status": "success", "message": f"Created {node_type} node: {node.name()}"}
        except Exception as e:
            return {"error": f"Failed to create node: {str(e)}"}

    def get_scene_info(self):
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
                    "nodes": nodes[:10]
                }
            }
        except Exception as e:
            return {"error": f"Failed to get scene info: {str(e)}"}

    def execute_code(self, command):
        code = command.get('code', '')
        try:
            exec(code)
            return {"status": "success", "message": "Code executed successfully"}
        except Exception as e:
            return {"error": f"Code execution failed: {str(e)}"}

    def stop_server(self):
        self.running = False
        if self.socket:
            self.socket.close()
        print("🛑 Nuke MCP Server stopped")

nuke_mcp_server = None

def start_nuke_mcp():
    global nuke_mcp_server
    if nuke_mcp_server is None:
        nuke_mcp_server = NukeMCPServer()
        thread = threading.Thread(target=nuke_mcp_server.start_server)
        thread.daemon = True
        thread.start()
    else:
        print("⚠️  Server already running!")

def stop_nuke_mcp():
    global nuke_mcp_server
    if nuke_mcp_server:
        nuke_mcp_server.stop_server()
        nuke_mcp_server = None
    else:
        print("⚠️  Server not running!")

print("🎬 NUKE MCP PORTABLE ADDON LOADED! Run start_nuke_mcp() to begin.")
