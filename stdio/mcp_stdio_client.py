import os
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

# transport = StdioTransport(
#     command=r"D:\#OpenSourceContribute\net_course_mcp_demo\.venv\Scripts\python.exe",
#     args=[r"D:\#OpenSourceContribute\net_course_mcp_demo\stdio_mcp_server.py"],
# )

# 訪問第三方的 MCP 伺服器
transport = StdioTransport(
    command="cmd",
    args=["/c", "npx", "server-perplexity-ask"],
    env={"PERPLEXITY_API_KEY": "YOUR_API_KEY_HERE"},
)


async def main():
    async with Client(transport) as client:
        # 獲取 MCP 伺服器中可用的工具列表
        tools = await client.list_tools()
        return tools


if __name__ == "__main__":
    print(f"目前應用程式 PID: {os.getpid()}")
    input("按下 Enter 鍵開始 MCP 客戶端...")
    print(asyncio.run(main()))
