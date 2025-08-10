# Claude-Nuke MCP (Model Context Protocol)

This is a working Claude Desktop integration for Nuke using the MCP protocol, just like Blender-MCP.

## 🚀 How to Use

1. Place `uvx-tools/` in your home directory
2. Add `uvx.cmd` to your PATH (Windows):
   - Path: `C:\Users\<you>\AppData\Roaming\Python\Python310\Scripts\`
3. Inside Claude Desktop:
   - Go to Settings > MCP > Add Server
   - Paste the content from `.cursor/mcp.json`
4. Run this command to test:
   ```
   uvx nuke-mcp
   ```
5. Open Claude and ask:
   > "Add a blur node and set its size to 25"

## 🔧 Notes

- Claude will now send real-time code instructions to Nuke via stdin
- No clipboard needed
- Real-time Claude connector supported

Enjoy.