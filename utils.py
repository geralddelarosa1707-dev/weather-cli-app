from datetime import datetime

def format_loc(geo):
  output = []
  
  output.append("\nWe found many results:")
  
  for index, info in enumerate(geo, start=1):
    output.append(f"""
    {index}. Name: {info.get('name')}
       Country: {info.get('country')}
       State: {info.get('state')}
       Latitude: {info.get('lat')}
       Longitude: {info.get('lon')}
      """)
      
  return "\n".join(output)

def format_sun(sun):
  return datetime.fromtimestamp(sun).strftime('%I:%M %p')
  
def format_datetime(dt):
  return datetime.fromtimestamp(dt).strftime('%B %d, %Y - %I:%M %p')
  
def humidity_message(humidity):
  if humidity < 40:
    return "Air feels dry."
  elif humidity < 70:
    return "Comfortable humidity."
  else:
    return "Humid weather."
    
def rain_message(pop):
  if pop < 20:
    return "Low chance of rain."
  elif pop < 50:
    return "Possible rain. Bring umbrella just in case."
  elif pop < 80:
    return "High chance of rain. Bring umbrella"
  else:
    return "Very likely to rain. Bring umbrella"

def format_weather(data: dict, symbol: str) -> str:
  name = data.get('name')
  sys = data.get('sys', {})
  country = sys.get('country')
    
  weather = data.get('weather', [])
  description = weather[0].get('description') if weather else "N/A"
  
  main = data.get('main', {})
  temp = main.get('temp')
  feels_like = main.get('feels_like')
  temp_min = main.get('temp_min')
  temp_max = main.get('temp_max')
  humidity = main.get('humidity')
  message = humidity_message(humidity)
  visibility = data.get('visibility')
  visibility_km = visibility / 1000 if visibility else "N/A"
  wind = data.get('wind', {})
  wind_speed = wind.get('speed')
  
  sunrise = sys.get('sunrise')
  sunrise_formatted = format_sun(sunrise)
  sunset= sys.get('sunset')
  sunset_formatted = format_sun(sunset)
    
  dt = data.get('dt')
  formatted_dt = format_datetime(dt)
  
  return f"""
  Weather from {name}, {country}
  
  Condition: {description}
  Temperature: {temp}{symbol}
  Feels like: {feels_like}{symbol}
  Temperature min: {temp_min}{symbol}
  Temperature max: {temp_max}{symbol}
  Humidity: {humidity}% - {message}
  Visibility: {visibility_km} km
  Wind Speed: {wind_speed} m/s
  
  Sunrise: {sunrise_formatted}
  Sunset: {sunset_formatted}
  DateTime: {formatted_dt}"""
  
def format_forecast(data: dict, days: int, symbol: str) -> str:
  forecasts = data.get('list', [])
  
  output = []
  
  shown_dates = set()
  
  for info in forecasts:
    dt = info.get('dt')
    formatted_dt = datetime.fromtimestamp(dt).strftime('%B %d, %Y')
    
    date = info.get('dt_txt').split()[0]
    time = datetime.fromtimestamp(dt).strftime('%I:%M %p')
    
    if date not in shown_dates:
      if len(shown_dates) == days:
        break
      
      shown_dates.add(date)
      
      output.append(f"\n=========== {formatted_dt} ==========")
      
    weather = info.get('weather', [])
    condition = weather[0].get('description') if weather else "N/A"
        
    main = info.get('main', {})
    temp = main.get('temp')
    feels_like = main.get('feels_like')
    
    humidity = main.get('humidity')
    message = humidity_message(humidity)
      
    wind = info.get('wind', {})
    wind_speed = wind.get('speed')
    
    pop = int(info.get('pop', 0) * 100)
    recommend = rain_message(pop)
    
    output.append(f"""
    Time: {time}
    Condition: {condition}
    Temperature: {temp}{symbol}
    Feels Like: {feels_like}{symbol}
    Humidity: {humidity}%
    Wind Speed: {wind_speed} m/s
    Rain Chance: {pop}%
    
    Recommendation:
    {recommend}
    {message}
    
-----------------------------""")

  return "\n".join(output)
  
def format_air(data: dict) -> str:
  air_list = data.get('list', [])
  
  if not air_list:
    return "Air quality data unavailable."
    
  air = air_list[0]
  
  aqi = air.get('main', {}).get('aqi')
  
  aqi_levels = {
    1: "Good - Air quality is clean",
    2: "Fair - Air is acceptable",
    3: "Moderate - Sensitive people should be careful",
    4: "Poor - Air may affect health",
    5: "Very Poor - Avoid outdoor activities"
  }
  
  status = aqi_levels.get(aqi)
  
  components = air.get('components')
  
  dt = air.get('dt')
  formatted_dt = format_datetime(dt)
  
  return f"""
  Air Quality: {status}
  
  PM2.5: {components['pm2_5']}
  PM10: {components['pm10']}
  CO: {components['co']}
  Ozone: {components['o3']}

  DateTime: {formatted_dt}"""
