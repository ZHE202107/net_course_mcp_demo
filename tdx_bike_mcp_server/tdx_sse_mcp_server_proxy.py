from fastmcp import FastMCP, Client
from fastmcp.client.transports import PythonStdioTransport

# 建立一個客戶端連接到原始的 STDIO 伺服器
proxy_client = Client(
    transport=PythonStdioTransport(
        "./tdx_bike_mcp_server/tdx_bike_openapi_to_mcp_server.py"
    ),
)

proxy = FastMCP.as_proxy(proxy_client, name="TDX Bike MCP Server")

if __name__ == "__main__":
    proxy.run(transport="sse", port=8002, host="0.0.0.0")
