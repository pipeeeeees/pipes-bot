import requests

if __name__ == '__main__':
    import creds
else:
    from pipesbot import creds

API_KEY = creds.OPEN_WEATHER_API_KEY
CITY_NAME = 'ATLANTA'
COUNTRY_CODE = 'US'
UNITS = 'imperial'  # For Fahrenheit

def real_time_weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME},{COUNTRY_CODE}&units={UNITS}&appid={API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        temp_max = weather_data['main']['temp_max']
        temp_min = weather_data['main']['temp_min']
        weather_description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        cloudiness = weather_data['clouds']['all']
        
        print(f"Temperature: {temperature} °F")
        print(f"Feels Like: {feels_like} °F")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"High Temperature: {temp_max} °F")
        print(f"Low Temperature: {temp_min} °F")
        print(f"Weather: {weather_description}")
        print(f"Wind Speed: {wind_speed} mph")
        print(f"Cloudiness: {cloudiness}%")

        return temperature, feels_like, humidity, pressure, temp_max, temp_min, weather_description, wind_speed, cloudiness
    else:
        print("Failed to retrieve weather data.")

def forecast_24hours():
    DAYS = 1 
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME},{COUNTRY_CODE}&units={UNITS}&cnt={DAYS * 8}&appid={API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()
        
        forecast_list = forecast_data['list']
        forecasted_temps = []
        
        for forecast in forecast_list:
            forecast_time = forecast['dt_txt']
            forecast_temp = forecast['main']['temp']
            forecasted_temps.append((forecast_time, forecast_temp))
        
        print("Forecasted Temperatures:")
        for time, temp in forecasted_temps:
            print(f"{time}: {temp} °F")
    else:
        print("Failed to retrieve forecast data.")

    return forecast_list

def rain():
    DAYS = 1 
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME},{COUNTRY_CODE}&units={UNITS}&cnt={DAYS * 8}&appid={API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()
        
        forecast_list = forecast_data['list']
        
        print("Forecasted Weather:")
        for forecast in forecast_list:
            forecast_time = forecast['dt_txt']
            forecast_temp = forecast['main']['temp']
            forecast_description = forecast['weather'][0]['description']
            
            chance_of_rain = 0
            if 'rain' in forecast:
                chance_of_rain = forecast['rain']['3h']
            
            print(f"{forecast_time}:")
            print(f"  Temperature: {forecast_temp} °F")
            print(f"  Weather: {forecast_description}")
            print(f"  Chance of Rain: {chance_of_rain} mm")
            print()
    else:
        print("Failed to retrieve forecast data.")

rain()