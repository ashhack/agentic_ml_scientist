from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# Create an MCP server
mcp = FastMCP(
    name="calculator",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
)


# Add a simple calculator tool
@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
async def mul(a: int, b: int) -> int:
    """Multiply two numbers together"""
    return a * b

@mcp.tool()
async def divide(a: int, b: int) -> int:
    """Divide two numbers together"""
    return a / b

@mcp.tool()
async def sub(a: int, b: int) -> int:
    """Subtract two numbers together"""
    return a - b

# Run the server
if __name__ == "__main__":
    transport = "streamable-http"
    match transport:
        case "stdio":
            print("Running server with stdio transport")
            mcp.run(transport="stdio")
        case "sse":
            print("Running server with SSE transport")
            mcp.run(transport="sse")
        case "streamable-http":
            print("Running server with Streamable HTTP transport")
            mcp.run(transport="streamable-http")
        case _:
            raise ValueError(f"Unknown transport: {transport}")