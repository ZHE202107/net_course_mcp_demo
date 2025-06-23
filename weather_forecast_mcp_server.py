import os
from typing import Dict, Any
from weather_service import WeatherService
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv(".env")

# 建立一個 FastMCP 伺服器實例
mcp = FastMCP(name="WeatherService")

weather_service = WeatherService(os.getenv("OPENWEATHER_API_KEY"))


# 定義一個 Tool
@mcp.tool
def get_current_weather(location: str, timezone_offset: int = 0) -> Dict[str, Any]:
    """
    獲取指定城市的當前天氣資訊。

    Parameters:
        location: 位置名稱，必須是英文，例如 "Taipei"、"New York"、"Tokyo"
        timezone_offset: 時區偏移量，以小時為單位，例如台北為 8，紐約為 -4。默認值為 0 (UTC 時間)
    Returns:
        包含今天和明天天氣預報的字典
    """
    # Call weather forecast function
    return weather_service.get_forecast(location, timezone_offset)


# 定義一個 Resource
@mcp.resource(
    uri="resource://supported-locations",
    name="SupportedLocations",
    description="提供可查詢天氣的城市列表。",
)
def get_supported_locations() -> list[str]:
    """返回支援的城市列表。"""
    return ["Taipei", "Taichung", "Kaohsiung"]


# 定義一個 Prompt
@mcp.prompt
def weather_assistant_role():
    """
    定義天氣助理的角色和行為，作為系統提示使用。

    你是一位親切且專業的天氣助理。你的主要任務是提供準確、即時的天氣預報，
    並根據天氣狀況給出有用的建議。當被詢問天氣時，請優先使用可用的工具來查詢資訊。
    你的回答應該簡潔明瞭，並帶有友善的語氣。
    """

    # content = """"""
    # # # 返回一個系統角色的訊息 (System Message)
    # # return PromptMessage(role="system", content=TextContent(type="text", text=content))
    # return content


# 5. 運行伺服器
if __name__ == "__main__":
    print("啟動天氣 SSE MCP 伺服器於 http://127.0.0.1:8001/sse")
    # 將伺服器以 SSE 模式運行
    mcp.run(transport="sse", port=8001)
