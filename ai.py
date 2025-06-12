import urllib.parse
import http.client
import json

def read_env_file(file_path):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def get_advice_gemini(climate_status: str, tmp_celcius: float) -> (bool, str):
    env_vars = read_env_file(".env")
    if "GEMINI_KEY" not in env_vars.keys():
        return (False, "")

    geminy_key = env_vars["GEMINI_KEY"]
    conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
    headers = { 'Content-type': 'application/json' }

    prompt = f"El estado del clima es '{climate_status}' y hacen {tmp_celcius} grados celcius. Que ropa debería usar? dame un consejo breve y al punto, sin comentarios extra. Utiliza texto plano, no uses markdown."

    body = '{"contents":[{"parts":[{"text": "' + prompt + '"}]}]}'

    conn.request("POST", "/v1beta/models/gemini-2.0-flash:generateContent?key=" + geminy_key, body, headers)
    response = conn.getresponse()

    if response.status == 200:
        data = json.loads(response.read().decode())
        result = data['candidates'][0]['content']['parts'][0]['text']
        conn.close()
        return True, result
    else:
        conn.close()
        return False, response.read().decode()

def get_weather_openweathermap(place_name: str) -> (bool, str):
    env_vars = read_env_file(".env")
    if "WEATHER_KEY" not in env_vars.keys():
        return (False, "Key not in env")

    conn = http.client.HTTPSConnection("api.openweathermap.org")
    url = f"/geo/1.0/direct?q={urllib.parse.quote_plus(place_name)}&appid={env_vars['WEATHER_KEY']}"

    print("url: ", url)
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
    return True, json.loads(data)

def get_weather_openmeteo(place_name: str) -> (bool, str):
    conn = http.client.HTTPSConnection("geocoding-api.open-meteo.com")
    url = f"/v1/search?name={urllib.parse.quote_plus(place_name)}&count=1&language=es&format=json"
    print("url: ", url)
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    if response.status != 200:
        print(f"Error on geo endpoint, status: {response.status}")
        return False, data

    decoded_data = json.loads(data)["results"][0]
    print("decoded_data: ", decoded_data)
    lat = decoded_data["latitude"]
    lon = decoded_data["longitude"]

    conn = http.client.HTTPSConnection("api.open-meteo.com")
    url = f"/v1/forecast?latitude={urllib.parse.quote(str(lat))}&longitude={urllib.parse.quote(str(lon))}&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,wind_direction_10m,wind_gusts_10m,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,surface_pressure,pressure_msl"

    print("weather url", url)
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read().decode()

    if response.status != 200:
        print(f"Error on weather endpoint, status: {response.status}")
        conn.close()
        return False, data

    conn.close() 
    return True, json.loads(data)

if __name__ == "__main__":
    place = input("Name of place: ")

    ok, clima = get_weather_openmeteo(place)
    if not ok:
        print(f"Hubo un error: {clima}")
        exit(1)

    print(f"Clima en {place} según openmeteo:", clima)


    ok, clima  = get_weather_openweathermap(place)
    if not ok:
        print(f"Hubo un error: {clima}")
        exit(1)
    print(f"Clima en {place} según openweathermap:", clima)

    ok, advice = get_advice_gemini(
        climate_status=clima["weather"][0]["description"],
        tmp_celcius=clima["main"]["feels_like"]
    )
    if not ok:
        print(f"Hubo un error: {advice}")
        exit(1)

    print(f"Concejo de IA:\n{advice}")



