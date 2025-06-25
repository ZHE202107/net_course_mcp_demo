import httpx
import os

from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType
from dotenv import load_dotenv

load_dotenv()

# Initialize the proxy with your TDX credentials
TDX_ACCESS_TOKEN = os.getenv("TDX_ACCESS_TOKEN", default=None)
if not TDX_ACCESS_TOKEN:
    raise ValueError("TDX_ACCESS_TOKEN 必須在環境變數中設定")
api_client = httpx.AsyncClient(
    base_url="https://tdx.transportdata.tw/api/basic",
    headers={"Authorization": f"Bearer {TDX_ACCESS_TOKEN}"},
)

# Load your OpenAPI spec
openapi_spec = httpx.get(
    "https://tdx.transportdata.tw/webapi/File/Swagger/V3/2cc9b888-a592-496f-99de-9ab35b7fb70d"
).json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=api_client,
    name="TDX Bike MCP Server",
    route_maps=[RouteMap(mcp_type=MCPType.TOOL)],
)

if __name__ == "__main__":
    mcp.run()
