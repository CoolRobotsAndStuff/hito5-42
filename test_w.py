import apis as apis
import os 
import csv

city = input("📍 Ingresá una ciudad: ")
success, data = apis.get_weather_openweathermap(city)

if success:
    def format_weather_report(weather_data: dict) -> str:
        name = weather_data.get("name", "Ubicación desconocida")
        main = weather_data["main"]
        weather = weather_data["weather"][0]
        wind = weather_data["wind"]

        temp = main["temp"]
        feels_like = main["feels_like"]
        description = weather["description"].capitalize()
        humidity = main["humidity"]
        pressure = main["pressure"]
        wind_speed = wind["speed"]
        wind_deg = wind.get("deg", 0)

        # Opcional: convertir grados del viento en texto
        directions = ["norte", "noreste", "este", "sureste", "sur", "suroeste", "oeste", "noroeste"]
        wind_dir = directions[round(wind_deg / 45) % 8]

        return (
            f"🌍 Clima actual en {name}:\n"
            f"🌡️ Temperatura: {temp} °C (se siente como {feels_like} °C)\n"
            f"🌤️ Cielo: {description}\n"
            f"💨 Viento: {wind_speed} km/h del {wind_dir}\n"
            f"💧 Humedad: {humidity}%\n"
            f"📈 Presión: {pressure} hPa"
        )

    print(format_weather_report(data))
else:
    print("❌ Error al obtener el clima:", data)




def save_weather_data(source: str, data: dict, city: str, filename="historial_global.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Si es la primera vez, escribimos los encabezados
        if not file_exists:
            writer.writerow([
                "Fuente",
                "Ciudad",
                "Temperatura (°C)",
                "Sensación térmica (°C)",
                "Descripción del clima",
                "Humedad (%)",
                "Presión (hPa)",
                "Viento (km/h)",
                "Dirección del viento / Día-Noche"
            ])

        if source == "openweathermap":
            main = data["main"]
            weather = data["weather"][0]
            wind = data["wind"]
            directions = ["norte", "noreste", "este", "sureste", "sur", "suroeste", "oeste", "noroeste"]
            wind_dir = directions[round(wind.get("deg", 0) / 45) % 8]

            writer.writerow([
                "openweathermap",
                data.get("name", city),
                main["temp"],
                main["feels_like"],
                weather["description"].capitalize(),
                main["humidity"],
                main["pressure"],
                wind["speed"],
                wind_dir
            ])

        elif source == "openmeteo":
            current = data.get("current", {})
            is_day = "Día" if current.get("is_day", 1) == 1 else "Noche"
            weather_code = current.get("weather_code", -1)

            # Mapa básico de códigos
            descriptions = {
                0: "Despejado",
                1: "Mayormente despejado",
                2: "Parcialmente nublado",
                3: "Nublado",
                45: "Niebla",
                61: "Lluvia ligera",
                80: "Chubascos",
                95: "Tormenta"
            }
            description = descriptions.get(weather_code, "Desconocido")

            writer.writerow([
                "openmeteo",
                city,
                current.get("temperature_2m", "N/A"),
                "",  # No hay "feels_like"
                description,
                "",  # No hay humedad
                "",  # No hay presión
                current.get("wind_speed_10m", "N/A"),
                is_day
            ])