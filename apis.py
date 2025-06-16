import urllib.parse
import http.client
import json
from dataclasses import dataclass

def read_env_file(file_path):
    env_vars = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        return {}
    return env_vars


@dataclass
class WeatherData:
    name: str
    value: 10
    unit: str

    def __str__(self):
        return f"{self.name}: {self.value}{self.unit}"
    def __repr__(self):
        return str(self)

@dataclass
class Weather:
    description: str
    temp:          WeatherData
    apparent_temp: WeatherData
    min_temp:      WeatherData
    max_temp:      WeatherData
    wind_speed:    WeatherData
    pressure:      WeatherData
    cloud_cover:   WeatherData
    humidity:      WeatherData
    precipitation: WeatherData
    rain:          WeatherData
    snowfall:      WeatherData

    def __repr__(self):
        ret = self.description + "\n\n"
        for field in list(self.__dataclass_fields__.values())[1:]:
            ret +="\n" + str(getattr(self, field.name))
        return ret

def get_weather_openweathermap(place_name: str, api_key: str) -> (bool, Weather):
    conn = http.client.HTTPSConnection("api.openweathermap.org")
    url = f"/geo/1.0/direct?q={urllib.parse.quote_plus(place_name)}&appid={api_key}"

    #print("url: ", url)
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode()

    if response.status != 200:
        conn.close()
        print(f"error on geo endpoint, status: {response.status}")
        return False, data

    decoded_data = json.loads(data)[0]
    lat = decoded_data["lat"]
    lon = decoded_data["lon"]

    url = f"/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=es&appid={env_vars['WEATHER_KEY']}"
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode()

    if response.status != 200:
        print(f"error on weather endpoint, status: {response.status}")
        conn.close()
        return False, data

    conn.close() 
    wdict = json.loads(data)
    #print("wdict:", wdict)
    rain = 0
    if "rain" in wdict["main"].keys():
        rain = wdict["main"]["rain"]["1h"]
    snow = 0
    if "snow" in wdict["main"].keys():
        snow = wdict["main"]["snow"]["1h"]
    weather = Weather(
        description   = wdict["weather"][0]["description"],
        temp          = WeatherData(name="Temperatura",          unit="°C", value = wdict["main"]["temp"]),
        apparent_temp = WeatherData(name="Temperatura aparente", unit="°C", value = wdict["main"]["feels_like"]),
        min_temp      = WeatherData(name="Mínima",               unit="°C", value = wdict["main"]["temp_min"]),
        max_temp      = WeatherData(name="Máxima",               unit="°C", value = wdict["main"]["temp_max"]),
        wind_speed    = WeatherData(name="Viento",               unit="km/h",value= wdict["wind"]["speed"]),
        pressure      = WeatherData(name="Presión",              unit="hPa", value= wdict["main"]["pressure"]),
        cloud_cover   = WeatherData(name="Cobertura",            unit="%", value  = wdict["clouds"]["all"]),
        humidity      = WeatherData(name="Humedad",              unit="%", value  = wdict["main"]["humidity"]),
        precipitation = WeatherData(name="Precipitación",        unit="mm/h", value = rain),
        rain          = WeatherData(name="Lluvia",               unit="mm/h", value = rain),
        snowfall      = WeatherData(name="Nieve",                unit="mm/h", value = snow)
    )
    return True, weather


def get_weather_openmeteo(place_name: str) -> (bool, Weather):
    weather_code2str = {
        0: "Cielo despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        56: "Llovizna helada ligera",
        57: "Llovizna helada intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        66: "Lluvia helada ligera",
        67: "Lluvia helada intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        77: "Granitos de nieve",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos violentos",
        85: "Chubascos de nieve ligeros",
        86: "Chubascos de nieve intensos",
        95: "Tormenta: ligera o moderada",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo intenso"
    }
    conn = http.client.HTTPSConnection("geocoding-api.open-meteo.com")
    url = f"/v1/search?name={urllib.parse.quote_plus(place_name)}&count=1&language=es&format=json"
    #print("url: ", url)
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    if response.status != 200:
        print(f"Error on geo endpoint, status: {response.status}")
        return False, data

    decoded_data = json.loads(data)["results"][0]
    #print("decoded_data: ", decoded_data)
    lat = decoded_data["latitude"]
    lon = decoded_data["longitude"]

    conn = http.client.HTTPSConnection("api.open-meteo.com")
    url = f"/v1/forecast?latitude={urllib.parse.quote(str(lat))}&longitude={urllib.parse.quote(str(lon))}&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,wind_direction_10m,wind_gusts_10m,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,surface_pressure,pressure_msl&daily=temperature_2m_max,temperature_2m_min&timezone=auto"

    #print("weather url", url)
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode()

    if response.status != 200:
        print(f"Error on weather endpoint, status: {response.status}")
        conn.close()
        return False, data

    conn.close() 
    
    data = json.loads(data)
    wdict = data["current"]
    wdict_daily = data["daily"]
    weather = Weather(
        description   = weather_code2str[wdict["weather_code"]],
        temp          = WeatherData(name="🌡️  Temperatura",          unit="°C", value = wdict["temperature_2m"],),
        apparent_temp = WeatherData(name="🌡️  Temperatura aparente", unit="°C", value = wdict["apparent_temperature"],),
        min_temp      = WeatherData(name="-  Mínima",               unit="°C", value = wdict_daily["temperature_2m_min"][0],),
        max_temp      = WeatherData(name="+  Máxima",               unit="°C", value = wdict_daily["temperature_2m_max"][0],),
        wind_speed    = WeatherData(name="💨 Viento",               unit="km/h", value = wdict["wind_speed_10m"],),
        pressure      = WeatherData(name="📈 Presión",              unit="hPa", value = wdict["surface_pressure"],),
        cloud_cover   = WeatherData(name="☁️  Cobertura",            unit="%", value = wdict['cloud_cover'],),
        humidity      = WeatherData(name="💧 Humedad",              unit="%", value = wdict["relative_humidity_2m"],),
        precipitation = WeatherData(name="💧 Precipitación",        unit="mm", value = wdict["precipitation"],),
        rain          = WeatherData(name="💧 Lluvia",               unit="mm", value = wdict["rain"],),
        snowfall      = WeatherData(name="🌨️  Nieve",                unit="cm", value = wdict["snowfall"],)
    )
    return True, weather

def get_advice_gemini(weather: Weather, api_key: str) -> (bool, str):
    conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
    headers = { 'Content-type': 'application/json' }

    prompt = f"El estado del clima es '{weather.description}' y hacen {weather.apparent_temp.value}{weather.apparent_temp.unit}. Que ropa debería usar? dame un consejo breve y al punto, sin comentarios extra. Utiliza texto plano, no uses markdown."

    body = '{"contents":[{"parts":[{"text": "' + prompt + '"}]}]}'

    conn.request("POST", "/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key, body, headers)
    response = conn.getresponse()

    if response.status == 200:
        data = json.loads(response.read().decode())
        result = data['candidates'][0]['content']['parts'][0]['text']
        conn.close()
        return True, result
    else:
        conn.close()
        return False, response.read().decode()

def get_weather(place, openweathermap_api_key: str = None) -> Weather:
    ok, clima = get_weather_openmeteo(place)
    if ok:
        return clima

    print(f"El servicio Open Meteo falló: {clima}, probando con Open Weather Map")

    if openweathermap_api_key is None:
        print(f"El servicio Open Weather falló: por favor proveer api key. No se pudo obtener el clima.")
        raise TypeError()

    ok, clima  = get_weather_openweathermap(place, api_key)
    if ok:
        return clima

    print(f"El servicio Open Weather falló: {clima}. No se pudo obtener el clima.")
    return ConnectionError()

if __name__ == "__main__":
    env_vars = read_env_file(".env")

    place = input("Name of place: ")
    clima = get_weather(place, env_vars.get("WEATHER_KEY", None))
    
    print(f"Clima en {place}:")
    print(clima)

    if "GEMINI_KEY" not in env_vars.keys():
        print("Error: llave de gemini. No se pudo generar concejo.")
        exit(1)


    ok, advice = get_advice_gemini(clima, api_key=env_vars["GEMINI_KEY"])
    if not ok:
        print(f"Error: {advice}")
        exit(1)

    print(f"Concejo de IA:\n{advice}")



