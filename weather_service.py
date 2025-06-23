"""
天氣預報系統 - 核心服務類
提供完整的天氣預報功能
"""

import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
import os

from models import WeatherForecast, WeatherEntry, WindInfo, WeatherError


class WeatherService:
    """天氣預報服務類"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化天氣服務

        Args:
            api_key: OpenWeatherMap API 金鑰，如未提供則從環境變量獲取
        """
        self.api_key = api_key or self._get_api_key()
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def _get_api_key(self) -> str:
        """從環境變量獲取API金鑰"""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise WeatherError(
                "API金鑰未找到。請設置環境變量 OPENWEATHER_API_KEY 或在初始化時提供api_key參數",
                "API_KEY_MISSING",
            )
        return api_key

    def _get_coordinates(self, location: str) -> tuple[float, float]:
        """
        獲取地理坐標

        Args:
            location: 地點名稱

        Returns:
            (緯度, 經度)
        """
        geocode_url = f"{self.base_url}/weather"
        params = {"q": location, "appid": self.api_key, "units": "metric"}

        try:
            response = requests.get(geocode_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return data["coord"]["lat"], data["coord"]["lon"]

        except requests.RequestException as e:
            raise WeatherError(f"網絡請求錯誤: {str(e)}", "NETWORK_ERROR")
        except KeyError as e:
            raise WeatherError(
                f"API回應數據結構錯誤: 缺少 {str(e)}", "DATA_STRUCTURE_ERROR"
            )

    def _get_current_weather(
        self, lat: float, lon: float, tz: timezone
    ) -> Dict[str, Any]:
        """
        獲取當前天氣

        Args:
            lat: 緯度
            lon: 經度
            tz: 時區

        Returns:
            當前天氣數據
        """
        current_url = f"{self.base_url}/weather"
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}

        response = requests.get(current_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "time": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": f"{data['main']['temp']} °C",
            "feels_like": f"{data['main']['feels_like']} °C",
            "temp_min": f"{data['main']['temp_min']} °C",
            "temp_max": f"{data['main']['temp_max']} °C",
            "weather_condition": data["weather"][0]["description"],
            "humidity": f"{data['main']['humidity']}%",
            "wind": {
                "speed": f"{data['wind']['speed']} m/s",
                "direction": f"{data['wind']['deg']} degrees",
            },
            "rain": f"{data.get('rain', {}).get('1h', 0)} mm/h"
            if "rain" in data
            else "No rain",
            "clouds": f"{data['clouds']['all']}%",
        }

    def _get_forecast_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        獲取預報數據

        Args:
            lat: 緯度
            lon: 經度

        Returns:
            預報數據
        """
        forecast_url = f"{self.base_url}/forecast"
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": "metric"}

        response = requests.get(forecast_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def _format_forecast_entry(
        self, entry: Dict[str, Any], dt: datetime, is_3h_forecast: bool = True
    ) -> Dict[str, Any]:
        """
        格式化預報條目

        Args:
            entry: 原始預報數據
            dt: 日期時間對象
            is_3h_forecast: 是否為3小時預報

        Returns:
            格式化的預報條目
        """
        rain_key = "3h" if is_3h_forecast else "1h"
        rain_unit = "mm/3h" if is_3h_forecast else "mm/h"

        return {
            "time": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": f"{entry['main']['temp']} °C",
            "feels_like": f"{entry['main']['feels_like']} °C",
            "temp_min": f"{entry['main']['temp_min']} °C",
            "temp_max": f"{entry['main']['temp_max']} °C",
            "weather_condition": entry["weather"][0]["description"],
            "humidity": f"{entry['main']['humidity']}%",
            "wind": {
                "speed": f"{entry['wind']['speed']} m/s",
                "direction": f"{entry['wind']['deg']} degrees",
            },
            "rain": f"{entry.get('rain', {}).get(rain_key, 0)} {rain_unit}"
            if "rain" in entry
            else "No rain",
            "clouds": f"{entry['clouds']['all']}%",
        }

    def get_forecast(self, location: str, timezone_offset: int) -> WeatherForecast:
        """
        獲取天氣預報

        Args:
            location: 地點名稱
            timezone_offset: 時區偏移（小時）

        Returns:
            天氣預報對象

        Raises:
            WeatherError: 當獲取天氣數據失敗時
        """
        try:
            # 獲取地理坐標
            lat, lon = self._get_coordinates(location)

            # 設置時區
            tz = timezone(timedelta(hours=timezone_offset))
            today = datetime.now(tz).date()
            tomorrow = today + timedelta(days=1)

            # 獲取當前天氣
            current_weather = self._get_current_weather(lat, lon, tz)
            today_forecast = [current_weather]
            tomorrow_forecast = []

            # 獲取預報數據
            forecast_data = self._get_forecast_data(lat, lon)

            # 處理預報數據
            for entry in forecast_data["list"]:
                dt = datetime.fromtimestamp(entry["dt"], tz)
                formatted_entry = self._format_forecast_entry(entry, dt)

                if dt.date() == today:
                    today_forecast.append(formatted_entry)
                elif dt.date() == tomorrow:
                    tomorrow_forecast.append(formatted_entry)

            return WeatherForecast(today=today_forecast, tomorrow=tomorrow_forecast)

        except requests.RequestException as e:
            raise WeatherError(f"網絡請求錯誤: {str(e)}", "NETWORK_ERROR")
        except ValueError as e:
            raise WeatherError(f"JSON解析錯誤: {str(e)}", "JSON_PARSE_ERROR")
        except KeyError as e:
            raise WeatherError(
                f"數據結構錯誤: 缺少關鍵字 {str(e)}", "DATA_STRUCTURE_ERROR"
            )
        except Exception as e:
            raise WeatherError(f"未預期錯誤: {str(e)}", "UNEXPECTED_ERROR")

    def get_forecast_dict(self, location: str, timezone_offset: int) -> Dict[str, Any]:
        """
        獲取天氣預報（字典格式）

        Args:
            location: 地點名稱
            timezone_offset: 時區偏移（小時）

        Returns:
            天氣預報字典
        """
        try:
            forecast = self.get_forecast(location, timezone_offset)
            return forecast.model_dump()
        except WeatherError:
            raise
        except Exception as e:
            raise WeatherError(
                f"轉換為字典格式時發生錯誤: {str(e)}", "CONVERSION_ERROR"
            )
