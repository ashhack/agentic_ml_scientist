from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv("../../.env")

mcp = FastMCP(
    name="FeatureEngineering",
    host="0.0.0.0",
    port=8050,
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Adds two integers together.
    """
    return a + b

# Running the MCP server
if __name__ == "__main__":
    transport = "stdio"
    
    match transport:
        case "stdio":
            print("Running server with stdio transport mode")
            mcp.run_sse()
        case "sse":
            print("Running server with SSE transport mode")
            mcp.run_http()
        case _:
            raise ValueError(f"Unsupported transport: {transport}")