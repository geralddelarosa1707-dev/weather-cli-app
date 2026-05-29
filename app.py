from datetime import datetime
import json
import os

from client import weather
from logger import logger
import utils

menu = {
  "WEATHER": "Look for weather",
  "FORECAST": "Look for forecast",
  "AIR": "Look for air pollution",
  "HISTORY": "View search history",
  "SEARCH-W": "Search weather history",
  "SEARCH-F": "Search forecast history",
  "SEARCH-A": "Search air history"
}

def show_menu(menu):
  print("\n------------MENU------------")
  for key, info in menu.items():
    print(f"{key}: {info}")
  print("----------------------------")
  
def validate_geo(geo):
  if isinstance(geo, str):
    print(geo)
    return False
      
  if not geo:
    print("\nCity not found.")
    return False
    
  return True
  
def get_loc(geo):
  try:
    get_location = int(input("\nEnter number: "))
          
    if get_location < 1 or get_location > len(geo):
      print("Invalid selection.")
      return None
            
  except ValueError:
    print("Please enter a valid number.")
    logger.error("FAILED_GETTING_LOCATION | REASON=INVALID_NUMBER")
    return None
    
  return get_location
  
def choose_location(geo, choice_loc):
  if len(geo) > 1:
    location = geo[choice_loc - 1]
    
  else:
    location = geo[0]
    
  return location
  
def get_unit(unit):
  if not unit:
    print("\nPlease choose a valid unit.")
    return None
      
  if unit == "C":
    units = "metric"
    symbol = "°C"
  elif unit == "F":
    units = "imperial"
    symbol = "°F"
  else:
    print("\nPlease choose a valid unit.")
    return None
    
  return {
    "api_unit": units,
    "symbol": symbol
  }
  
def format_history(list_data, history):
  for index, info in enumerate(list_data, start=1):
    print(f"\n============= {history} {index} =============")
    for key, detail in info.items():
      if key == 'data':
        print(f"\n{key.upper()}:\n{detail}")
      else:
        print(f"{key.capitalize()}: {detail}")
  
def get_info(option, city, country, format_response):
  info = {
    "type": option,
    "city": city,
    "country": country,
    "timestamp": datetime.now().strftime("%B %m, %d - %I:%M %p"),
    "data": format_response
  }
  
  return info
  
def load_searches():
  try:
    with open("search_history.json", "r") as file:
      data = json.load(file)
      
      if not isinstance(data, list):
        return []
      
      return data
      
  except FileNotFoundError:
    return []
    
  except json.JSONDecodeError:
    print("\nInvalid file format.")
    logger.error("FAILED_LOADING_FILE | REASON=JSONDecodeError")
    return []
  
def save_searches(searches):
  temp_file = "search_history.json.tmp"
  main_file = "search_history.json"
  
  try:
    with open(temp_file, "w") as file:
      json.dump(searches, file, indent=4)
      
      file.flush()
      os.fsync(file.fileno())
      
    os.replace(temp_file, main_file)
  except Exception as e:
    print("\nError saving data:", e)
    logger.error(f"FAILED_SAVING_FILE | REASON={e}")

def main(searches):
  while True:
    show_menu(menu)
    
    option = input("\nWhat would you like to do: ").strip().upper()
    
    if option == "WEATHER":
      city = input("\nEnter city: ").strip()
      
      if not city:
        print("\nPlease enter a city.")
        continue
      
      geo = weather.geocoding_direct(city)
      
      if not validate_geo(geo):
        continue
      
      choice_loc = None
        
      if len(geo) > 1:
        print(utils.format_loc(geo))
        
        choice_loc = get_loc(geo)
      
        if choice_loc is None:
          continue
      
      location = choose_location(geo, choice_loc)
      
      lat = location.get('lat')
      lon = location.get('lon')
      
      city = location.get('name')
      country = location.get('country')
      
      unit = input("\nChoose unit (C/F): ").strip().upper()
      
      units = get_unit(unit)
      
      if units is None:
        continue
      
      api_unit = units['api_unit']
      symbol = units['symbol']
      
      response = weather.get_weather(lat, lon, api_unit)
      
      if isinstance(response, str):
        print(f"\n{response}")
      else:
        weather_response_f = utils.format_weather(response, symbol)
        
        print(weather_response_f)
        logger.info(f"SEARCH_WEATHER_SUCCESS | CITY={city} | COUNTRY={country}")
        
        info = get_info(option, city, country, weather_response_f)
        searches.append(info)
        save_searches(searches)
        
        input("\nPress Enter to continue...")
        
    elif option == "FORECAST":
      city = input("\nEnter city: ").strip()
      
      if not city:
        print("\nPlease enter a city.")
        continue
      
      geo = weather.geocoding_direct(city)
      
      if not validate_geo(geo):
        continue
      
      choice_loc = None
        
      if len(geo) > 1:
        print(utils.format_loc(geo))
        
        choice_loc = get_loc(geo)
      
        if choice_loc is None:
          continue
      
      location = choose_location(geo, choice_loc)
      
      lat = location.get('lat')
      lon = location.get('lon')
      
      city = location.get('name')
      country = location.get('country')
      
      try:
        days = int(input("\nEnter forecast days (1-5): "))
        
        if days < 1 or days > 5:
          print("\nPlease enter a valid number.")
          continue
        
      except ValueError:
        print("\nPlease enter a valid number.")
        logger.warning(f"FAILED_SEARCHING_FORECAST | CITY={city} | REASON=INVALID_NUMBER_OF_DAYS")
        continue
      
      unit = input("\nChoose unit (C/F): ").strip().upper()
      
      units = get_unit(unit)
      
      if units is None:
        continue
      
      api_unit = units['api_unit']
      symbol = units['symbol']
      
      response = weather.get_forecast(lat, lon, api_unit)
      
      if isinstance(response, str):
        print(f"\n{response}")
      else:
        forecast_response_f = utils.format_forecast(response, days, symbol)
        
        print(forecast_response_f)
        logger.info(f"SEARCHING_FORECAST_SUCCESS | CITY={city} | COUNTRY={country}")
        
        info = get_info(option, city, country, forecast_response_f)
        searches.append(info)
        save_searches(searches)
        
        input("\nPress Enter to continue...")
        
    elif option == "AIR":
      city = input("\nEnter city: ").strip()
      
      if not city:
        print("\nPlease enter a city.")
        continue
      
      geo = weather.geocoding_direct(city)
      
      if not validate_geo(geo):
        continue
      
      choice_loc = None
        
      if len(geo) > 1:
        print(utils.format_loc(geo))
        
        choice_loc = get_loc(geo)
      
        if choice_loc is None:
          continue
      
      location = choose_location(geo, choice_loc)
      
      lat = location.get('lat')
      lon = location.get('lon')
      
      city = location.get('name')
      country = location.get('country')
      
      response = weather.get_air(lat, lon)
      
      if isinstance(response, str):
        print(f"\n{response}")
      else:
        air_response_f = utils.format_air(response)
        
        print(air_response_f)
        logger.info(f"SEARCHING_AIR_SUCCESS | CITY={city} | COUNTRY={country}")
        
        info = get_info(option, city, country, air_response_f)
        searches.append(info)
        save_searches(searches)
        
        input("\nPress Enter to continue...")
        
    elif option == "HISTORY":
      if not searches:
        print("\nNo search history found.")
        continue
      
      format_history(searches, "Search")
      
      input("\nPress Enter to continue...")
            
    elif option == "SEARCH-W":
      output = [info for info in searches if info.get('type', "").upper() == 'WEATHER']
      
      if not output:
        print("\nNo weather history yet.")
        continue
          
      format_history(output, "Weather")
      
      input("\nPress Enter to continue...")
      
    elif option == "SEARCH-F":
      output = [info for info in searches if info.get('type', "").upper() == 'FORECAST']
      
      if not output:
        print("\nThere's no forecast history yet.")
        continue
      
      format_history(output, "Forecast")
      
      input("\nPress Enter to continue...")
      
    elif option == "SEARCH-A":
      output = [info for info in searches if info.get('type', "").upper() == 'AIR']
      
      if not output:
        print("\nThere's no air history yet.")
        continue
      
      format_history(output, "Air")
      
      input("\nPress Enter to continue...")
      
    else:
      print("\nPlease enter a valid option")
      
if __name__ == "__main__":
  print("Weather")
  
  searches = load_searches()
  main(searches)