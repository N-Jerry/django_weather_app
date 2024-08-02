from django.shortcuts import render
import requests

# Create your views here.
def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "ece881f91f4c37a140b95a9706a203e5"
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None



def home(request):
    weather_data_results = {}
    if request.method == 'POST':
        cities = request.POST.get('city')
        icon_url = 'https://openweathermap.org/img/wn/10d@2x.png'
        cities = cities.split(',')
        for city in cities:
            weather_data_results[city] = get_weather(city)

        final_results = []
        for result in weather_data_results.values():
            if result is not None:
                print(type(result))
                icon_id = result['weather'][0]['icon']
                icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
                weather = result['weather'][0]['main']
                weather_description = result['weather'][0]['description']
                city = result['name']
                country = result['sys']['country']
                wind_speed = result['wind']['speed']
                pressure = result['main']['pressure']
                humidity = result['main']['humidity']
                temperature = result['main']['temp']

                final_results.append({
                'icon_url': icon_url,
                'weather': weather,
                'weather_description': weather_description,
                'city': city,
                'country': country,
                'wind_speed': wind_speed,
                'pressure': pressure,
                'humidity': humidity,
                'temperature': temperature})
        
            else:
                continue
    else:
        return render(request, 'base/index.html')
    return render(request, 'base/index.html', {'results': final_results})