import os

import dotenv
import requests

from config import URL
from logger import logger

dotenv.load_dotenv(".env")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def handle_exceptions(error):
  if isinstance(error, requests.HTTPError):
    logger.error(f"FAILED_REQUEST | REASON={error}")
    return f"Bad response from server: {error}"
    
  elif isinstance(error, requests.Timeout):
    logger.error(f"FAILED_REQUEST | REASON={error}")
    return "The request timed out."
    
  elif isinstance(error, requests.ConnectionError):
    logger.error(f"FAILED_REQUEST | REASON={error}")
    return "Connection failed."
    
  elif isinstance(error, requests.RequestException):
    logger.error(f"FAILED_REQUEST | REASON={error}")
    return f"Network error: {error}"
    
  return None
  
class WeatherClient:
  def __init__(self, URL, API_KEY):
    self.URL = URL
    self.API_KEY = API_KEY
    
  def geocoding_direct(self, city):
    params = {
      "q": city,
      "limit": 10,
      "appid": self.API_KEY
    }
    
    try:
      response = requests.get(
        f"{self.URL}/geo/1.0/direct",
        params=params,
        timeout=5
        )
      response.raise_for_status()
    
    except requests.RequestException as error:
      return handle_exceptions(error)
    
    else:
      return response.json()
  
  def get_weather(self, lat, lon, units):
    params = {
      "lat": lat,
      "lon": lon,
      "units": units,
      "appid": self.API_KEY
    }
    
    try:
      response = requests.get(
        f"{self.URL}/data/2.5/weather",
        params=params,
        timeout=5)
      response.raise_for_status()
      
    except requests.RequestException as error:
      return handle_exceptions(error)
    
    else:
      return response.json()
      
  def get_forecast(self, lat, lon, units):
    params = {
      "lat": lat,
      "lon": lon,
      "units": units,
      "appid": self.API_KEY
    }
    
    try:
      response = requests.get(
        f"{self.URL}/data/2.5/forecast",
        params=params,
        timeout=5)
      response.raise_for_status()
      
    except requests.RequestException as error:
      return handle_exceptions(error)
      
    else:
      return response.json()
    
  def get_air(self, lat, lon):
    params = {
      "lat": lat,
      "lon": lon,
      "appid": self.API_KEY
    }
    
    try:
      response = requests.get(
        f"{self.URL}/data/2.5/air_pollution",
        params=params,
        timeout=5
        )
      response.raise_for_status()
      
    except requests.RequestException as error:
      return handle_exceptions(error)
    
    else:
      return response.json()
      
weather = WeatherClient(URL, API_KEY)