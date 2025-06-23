"""
天氣預報系統 - 數據模型
包含所有相關的數據結構定義
"""

from pydantic import BaseModel, Field
from typing import List


class WindInfo(BaseModel):
    """風力數據"""

    speed: str = Field(..., description="風速 (米/秒)")
    direction: str = Field(..., description="風向 (度數)")


class WeatherEntry(BaseModel):
    """天氣數據"""

    time: str = Field(..., description="天氣數據時間")
    temperature: str = Field(..., description="溫度 (攝氏度)")
    feels_like: str = Field(..., description="體感溫度 (攝氏度)")
    temp_min: str = Field(..., description="最低溫度 (攝氏度)")
    temp_max: str = Field(..., description="最高溫度 (攝氏度)")
    weather_condition: str = Field(..., description="天氣狀況描述")
    humidity: str = Field(..., description="濕度百分比")
    wind: WindInfo = Field(..., description="風速和風向信息")
    rain: str = Field(..., description="降雨量")
    clouds: str = Field(..., description="雲層覆蓋百分比")


class WeatherForecast(BaseModel):
    """天氣預報模型"""

    today: List[WeatherEntry] = Field(..., description="今日天氣預報，包含當前天氣")
    tomorrow: List[WeatherEntry] = Field(..., description="明日天氣預報")


class WeatherError(Exception):
    """天氣服務自定義異常"""

    def __init__(self, message: str, error_type: str = "UNKNOWN"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)
