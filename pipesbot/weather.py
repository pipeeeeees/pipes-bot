import requests

if __name__ == '__main__':
    import creds
else:
    from pipesbot import creds

API_KEY = creds.OPEN_WEATHER_API_KEY
CITY_NAME = 'ATLANTA'
COUNTRY_CODE = 'US'
UNITS = 'imperial'  # For Fahrenheit

def real_time_weather(verbose = False):
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
        
        if verbose:
            print(f"Temperature: {temperature} °F")
            print(f"Feels Like: {feels_like} °F")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure} hPa")
            print(f"High Temperature: {temp_max} °F")
            print(f"Low Temperature: {temp_min} °F")
            print(f"Weather: {weather_description}")
            print(f"Wind Speed: {wind_speed} mph")
            print(f"Cloudiness: {cloudiness}%")

        """
        Example output:

        Temperature: 48.99 °F
        Feels Like: 43.97 °F
        Humidity: 57%
        Pressure: 1018 hPa
        High Temperature: 51.75 °F
        Low Temperature: 44.15 °F
        Weather: clear sky
        Wind Speed: 12.66 mph
        Cloudiness: 0%
        """

        return temperature, feels_like, humidity, pressure, temp_max, temp_min, weather_description, wind_speed, cloudiness
    else:
        print("Failed to retrieve weather data.")

def real_time_weather_report(verbose = False, plot = False):
    # get real time weather information
    temperature, feels_like, humidity, pressure, temp_max, temp_min, weather_description, wind_speed, cloudiness = real_time_weather()

    # compose the message
    message_string = f''
    if temperature <= 32.0:
        message_string = message_string + f'\n- It is cold as ice outside with a temp of {int(temperature)}°F \U0001F9CA\U0001F976'
        message_string = message_string + f'\n- The high for today is {int(temp_max)} °F and the low is {int(temp_min)}°F'
        message_string = message_string + f'\n- With windchill it feels like {int(feels_like)}°F ' + chr(0x1F976)
    elif temperature >= 90.0:
        message_string = message_string + f'\n- It is hot as balls outside with a temp of {int(temperature)}°F \U0001F975\U0001F525'
        message_string = message_string + f'\n- The high for today is {int(temp_max)} °F and the low is {int(temp_min)}°F'
        message_string = message_string + f'\n- With heat index it feels like {int(feels_like)}°F ' + chr(0x1F525)
    else:
        message_string = message_string + f'\n- It is {int(temperature)}°F outside with a high of {int(temp_max)}°F and a low of {int(temp_min)} °F'
    #message_string = message_string + f'\n- You can expect {weather_description} today'
    message_string = message_string + daily_rain_report()
    if humidity >= 80:
        message_string = message_string + f'\n- The humidity is {humidity}%. It is very humid! ' + chr(0x1F4A7)
    elif humidity <= 20:
        message_string = message_string + f'\n- The humidity is {humidity}%. It is very dry! ' + chr(0x1F3DC)

    if wind_speed >= 21:
        message_string = message_string + f'\n- The wind speed is {wind_speed} mph. It is very windy today! ' + chr(0x1F4A8)

    if cloudiness >= 80:
        message_string = message_string + f'\n- The sky is {cloudiness}% cloudy today ' + chr(0x2601)
    
    if verbose:
        print(message_string)
    return message_string
    

def forecast_24hours(days = 1, verbose = False):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME},{COUNTRY_CODE}&units={UNITS}&cnt={days * 8}&appid={API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()
        
        forecast_list = forecast_data['list']
        forecasted_temps = []
        
        for forecast in forecast_list:
            forecast_time = forecast['dt_txt']
            forecast_temp = forecast['main']['temp']
            forecasted_temps.append((forecast_time, forecast_temp))
        if verbose:
            print("Forecasted Temperatures:")
        for time, temp in forecasted_temps:
            if verbose:
                print(f"{time}: {temp} °F")

        """
        Example output:

        Forecasted Temperatures:
        2023-12-05 06:00:00: 48.85 °F
        2023-12-05 09:00:00: 47.03 °F
        2023-12-05 12:00:00: 44.17 °F
        2023-12-05 15:00:00: 49.23 °F
        2023-12-05 18:00:00: 57 °F
        2023-12-05 21:00:00: 58.28 °F
        2023-12-06 00:00:00: 53.47 °F
        2023-12-06 03:00:00: 50.74 °F
        """
    else:
        print("Failed to retrieve forecast data.")

    return forecast_list

def rain(days = 1):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME},{COUNTRY_CODE}&units={UNITS}&cnt={days * 8}&appid={API_KEY}'

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

        """
        Example output:

        Forecasted Weather:
        2023-12-05 06:00:00:
        Temperature: 48.85 °F
        Weather: clear sky
        Chance of Rain: 0 mm

        2023-12-05 09:00:00:
        Temperature: 47.03 °F
        Weather: clear sky
        Chance of Rain: 0 mm

        2023-12-05 12:00:00:
        Temperature: 44.17 °F
        Weather: clear sky
        Chance of Rain: 0 mm

        2023-12-05 15:00:00:
        Temperature: 49.23 °F
        Weather: clear sky
        Chance of Rain: 0 mm

        2023-12-05 18:00:00:
        Temperature: 57 °F
        Weather: clear sky
        Chance of Rain: 0 mm

        2023-12-05 21:00:00:
        Temperature: 58.28 °F
        Weather: clear sky
        Chance of Rain: 0 mm

        2023-12-06 00:00:00:
        Temperature: 53.47 °F
        Weather: clear sky
        Chance of Rain: 0 mm
  """
    else:
        print("Failed to retrieve forecast data.")

def daily_rain_report(verbose = False, plot = False):
    forecast_list = forecast_24hours()

    # compose the message to share if it will rain today or not, and if so when it will start and the highest probability of rain. if the probability is 100% for more than 3 hours of the day, then print 'It gone rain.'

    message_string = ''
    rain_flag = False
    for forecast in forecast_list:
        forecast_time = forecast['dt_txt']
        forecast_temp = forecast['main']['temp']
        forecast_description = forecast['weather'][0]['description']
        
        chance_of_rain = 0
        if 'rain' in forecast:
            chance_of_rain = forecast['rain']['3h']
            # convert mm to inches
            chance_of_rain = chance_of_rain * 0.0393701
        
        if chance_of_rain > 0:
            rain_flag = True
            message_string = message_string + f'\n- It will rain today \U0001F327'
            break
    if not rain_flag:
        message_string = message_string + f'\n- It will not rain today \U00002600'

    if rain_flag or verbose:
        # plot the forecasted rain for the day 
        plot_rain()
        
    
    return message_string

def plot_rain(verbose = False):
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime
    from matplotlib.dates import date2num

    # get the forecasted rain for the day
    forecast_list = forecast_24hours()
    forecasted_rain = []
    forecasted_times = []
    for forecast in forecast_list:
        forecast_time = forecast['dt_txt']
        forecast_temp = forecast['main']['temp']
        forecast_description = forecast['weather'][0]['description']
        
        chance_of_rain = 0
        if 'rain' in forecast:
            chance_of_rain = forecast['rain']['3h']
        
        forecasted_rain.append(chance_of_rain)
        forecasted_times.append(forecast_time)

    # convert the forecasted times to datetime objects
    forecasted_times = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in forecasted_times]

    # convert to hours only
    forecasted_times = [time.strftime('%H:%M') for time in forecasted_times]

    # convert mm to inches
    forecasted_rain = [rain * 0.0393701 for rain in forecasted_rain]

    # plot the forecasted rain for the day
    fig, ax = plt.subplots()
    ax.plot(forecasted_times, forecasted_rain)
    ax.set(xlabel='Time', ylabel='Rain (inches)', title=f'Forecasted Rain for {datetime.date.today().strftime("%m-%d-%Y")} (Beta Feature)')
    ax.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    # limit y axis to be greater than 0
    plt.ylim(bottom=0)
    plt.savefig(r'pipesbot\plots\forecasted_rain.png')
    if verbose:
        plt.show()
    plt.close()


if __name__ == '__main__':
    #real_time_weather()
    #forecast_24hours()
    #print(daily_rain_report(verbose=True))
    #print(real_time_weather_report(plot=True))
    #print('\U0001F975\U0001F525')
    print('\U0001F327')
    print('\U0001F64C')
    # sun unicode: \U00002600
    print('\U00002600')