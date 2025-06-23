"""
天氣預報系統包
提供完整的天氣預報功能
"""

from .models import WeatherForecast, WeatherEntry, WindInfo, WeatherError
from .weather_service import WeatherService

__version__ = "1.0.0"
__all__ = [
    "WeatherService",
    "WeatherForecast",
    "WeatherEntry",
    "WindInfo",
    "WeatherError",
]
