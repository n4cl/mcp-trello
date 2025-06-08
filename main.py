from fastmcp import FastMCP

mcp = FastMCP("Trello MCP Server")

@mcp.tool()
def get_health_status() -> str:
    """サーバーのヘルスステータスを返します。"""
    return "OK"

if __name__ == "__main__":
    mcp.run()
