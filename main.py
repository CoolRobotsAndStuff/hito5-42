# Integrar Api's necesarias
# AYUDA NO SE USAR APIS AAAAAAAAAA
# Importar las librerías necesarias
import hashlib
import apis as apis
import charts as charts
import csv
import os
from datetime import datetime
from operator import itemgetter
# Declarar Constantes
OPENWEATHERMAP_API_KEY = 'key' # Clave de la API de OpenWeatherMap
GEMINI_API_KEY = 'key' # Clave de la API de Gemini
ARCHIVO_USUARIOS = 'usuarios_simulados.csv' # Nombre del archivo para almacenar usuarios y contraseñas
ARCHIVO_HISTORIAL_GLOBAL = 'historial_global.csv'
usuario_logueado = None

# Banner del programa
print ('''
       ######% #################     ################%              %#####
       ######% ###################    %################%             ######
         ####% #####################    ################%             #####%
           ##%        ######             ##       #######        ##    #####%
                      ######         ##           ######%       ####   ######
       ###            ######         ###%   %##########%       ######   ######
       #####%         ######         #####   ########         #######    ######
       ######%        ######         ######%   #########      ######     #######
       ######%        ######         ######%    %########    ###########  %######
       ######%          %###         ######        #######  ############## ######
       ######%        ##%  #         ######        ######% ###############% ######
       ######%        #####          #############% #####%%######%           ######
       ######%        ######         ############### #### #######            %#####%
       ######%        ######         ################    #######              #######
         _____                     _ _   __              _      _    _____ _ _
        / ____|                   | (_) /_/             | |    | |  / ____| (_)
       | |  __ _   _  __ _ _ __ __| |_  __ _ _ __     __| | ___| | | |    | |_ _ __ ___   __ _
       | | |_ | | | |/ _` | '__/ _` | |/ _` | '_ \\   / _` |/ _ \\ | | |    | | | '_ ` _ \\ / _` |
       | |__| | |_| | (_| | | | (_| | | (_| | | | | | (_| |  __/ | | |____| | | | | | | | (_| |
        \\_____|\\__,_|\\__,_|_|  \\__,_|_|\\__,_|_| |_|  \\__,_|\\___|_|  \\_____|_|_|_| |_| |_|\\__,_|
        Grupo 42: Patricio Aldasoro           Alejandro De Ugarriza Mohnblatt
                  Zoe María Perez Colman      Tomás Spurio
                  Bautista Andrés Peral
''')

# Función para cargar los usuarios desde el archivo ya existente o crear uno nuevo si no existe.
def cargar_usuarios():
    usuarios = {}
    try:
        with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)

            for row in reader:
                usuario = row["username"]
                contraseña = row["password_simulada"]
                usuarios[usuario] = contraseña
    except FileNotFoundError:
        pass
    return usuarios

# Función para guardar los usuarios en el archivo.
def guardar_usuarios(username, password):
    file_exists = os.path.isfile(ARCHIVO_USUARIOS)
    with open(ARCHIVO_USUARIOS, 'a', encoding='utf-8') as archivo:

        writer = csv.DictWriter(archivo, ["username", "password_simulada"])

        if not file_exists:
            writer.writeheader()

        writer.writerow({"username": username, "password_simulada": password})

# Función para encriptar la contraseña usando SHA-256. (no se si lo veran pero suma)
def encriptar_contrasena(contrasena):
    # Usar un salt fijo para el hash
    salt = 'grupo42_salt2024'
    return hashlib.sha256((salt + contrasena).encode()).hexdigest()

# Función para validar la contraseña según los criterios establecidos.
def validar_contrasena(contrasena):
    caracteres_especiales = "!@#$%^&*(),.?\":{}|<>"
    errores = []
    if len(contrasena) < 8:
        errores.append('- Mínimo 8 caracteres')
    if not any(caracter.isupper() for caracter in contrasena):
        errores.append('- Al menos una mayúscula')
    if not any(caracter.islower() for caracter in contrasena):
        errores.append('- Al menos una minúscula')
    if not any(caracter.isdigit() for caracter in contrasena):
        errores.append('- Al menos un dígito')
    if not any(caracter in caracteres_especiales for caracter in contrasena):
        errores.append('- Al menos un carácter especial')
    return len(errores) == 0, errores

# Funcion para registrar un nuevo usuario.
def registrar_usuario(usuarios):
    print('Registro de usuario')
    nombre_usuario = ""
    nombre_usuario = input('Nombre de usuario: ').strip()
    if not nombre_usuario.isalpha():
        print("El nombre de usuario contiene caracteres inválidos, intente nuevamente.")
        return
    if nombre_usuario in usuarios:
        print('El usuario ya existe, ingrese otro.')
        return
    while True:
        contraseña = input('Contraseña: ')
        valido, mensajes = validar_contrasena(contraseña)
        if not valido:
            print('Contraseña insegura:')
            for msg in mensajes:
                print(msg)
            continue
        confirmacion = input('Confirme contraseña: ')
        if contraseña != confirmacion:
            print('Las contraseñas no coinciden, intente nuevamente.')
            continue
        usuarios[nombre_usuario] = contraseña
        guardar_usuarios(nombre_usuario, contraseña)
        usuario_logueado = nombre_usuario
        print(f'Usuario registrado correctamente. Bienvenido, {usuario_logueado}')
        menu_principal()
        break

# Función para iniciar sesión con un usuario ya registrado.
def iniciar_sesion(usuarios):
    print('Inicio de sesión')
    nombre_usuario = input('Nombre de usuario: ').strip()
    if nombre_usuario not in usuarios:
        print('Usuario no registrado.')
        return
    contraseña = input('Contraseña: ')
    if usuarios[nombre_usuario] == contraseña:
        usuario_logueado = nombre_usuario
        print(f'Bienvenido, {usuario_logueado}!')
        menu_principal()  # Mostrar menú principal tras inicio de sesión correcto
    else:
        print('Contraseña incorrecta.')
        while True:
            print("¿Desea intentar de nuevo (1) o volver al menú de inicio (2)?")
            opcion = input("> ").strip()
            if opcion == '1':
                return iniciar_sesion(usuarios)
            elif opcion == '2':
                return  # Vuelve al menú de acceso (menu_de_acceso)
            else:
                print("Opción no válida. Ingrese 1 para reintentar o 2 para volver al menú de acceso.")

# Menu de inicio pre-registro.
# De aca se va al menu principal
def menu_de_acceso():
    usuarios = cargar_usuarios()
    while True:
        print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║                           MENÚ DE INICIO                                   ║
        ╠════════════════════════════════════════════════════════════════════════════╣
        ║   1. Iniciar sesión                                                        ║
        ║   2. Registrar usuario                                                     ║
        ║   3. Salir                                                                 ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """)
        print("\n{:^80}\n".format("Ingrese la opción deseada:"))
        opcion = input("> ").strip()
        if opcion == '1':
            iniciar_sesion(usuarios)
        elif opcion == '2':
            registrar_usuario(usuarios)
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        else:
            print("{:^80}".format('Opción no válida'))

#Formatear unificar los datos de las APIS de clima
def format_weather_openmeteo(data: dict, place: str) -> str: #formateo los datos de open meteo
    current = data.get("current", {})
    temp = current.get("temperature_2m", "N/A")
    wind_speed = current.get("wind_speed_10m", "N/A")
    weather_code = current.get("weather_code", -1)
    is_day = current.get("is_day", 1)

    # Diccionario básico de códigos del clima
    weather_descriptions = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        61: "Lluvia ligera",
        71: "Nieve ligera",
        80: "Chubascos",
        95: "Tormenta"
    }

    description = weather_descriptions.get(weather_code, "Condición desconocida")
    sun = "☀️" if is_day else "🌙"

    return (
        f"{sun} Clima actual en {place}:\n"
        f"🌡️ Temperatura: {temp} °C\n"
        f"🌤️ Cielo: {description}\n"
        f"💨 Viento: {wind_speed} km/h"
    )

def format_weather_report(weather_data: dict) -> str:  #formateo los datos de open weather map
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


def save_weather_summary(source: str, city: str, summary: str): #guardo los datos basicamente de las APIs
    file_exists = os.path.isfile(ARCHIVO_HISTORIAL_GLOBAL)

    with open(ARCHIVO_HISTORIAL_GLOBAL, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, ["usuario", "ciudad", "fechahora", "temperatura_c", "condicion_clima", "humedad_porcentaje", "viento_kmh"])

        # Escribir encabezado si el archivo no existe
        if not file_exists:
            writer.writeheader()

        # Escribir los datos
        pass
        #writer.writerow({"usuario": usuario_logueado #resto de campos })

#Historial de consultas y consultar el clima
def consult_weather():
    print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ Ingrese el nombre de una ciudad porfavor                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
            """)
    city_name = input()
    success, data = apis.get_weather_openweathermap(city_name.casefold())#weather options
    success_ow, data_ow = apis.get_weather_openweathermap(city_name.casefold())
    w1 = format_weather_openmeteo(data,city_name)
    w2 = format_weather_report(data_ow)

    if(success and success_ow):
        print(f"""\n
        ╔════════════════════════════════════════════════════════════════╗
        ║                                                                ║
        ║    {format_weather_openmeteo(data,city_name)}                  ║
        ║    {format_weather_report(data_ow)}                            ║
        ╚════════════════════════════════════════════════════════════════╝
    """)
        save_weather_summary(usuario_logueado,"openmeteo",city_name, w1 ) #guardo los datos obtenidos y formateados de openmeteo
        save_weather_summary(usuario_logueado,"openweathermap",city_name, w2 ) #guardo los datos obtenidos y formateados de openweathermap
    else:
        print(" Error al obtener el clima:", data)
        print(" Error al obtener el clima:", data_ow)

def consult_history():
    entrys = []
    print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ Ingrese el nombre de una ciudad porfavor                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """)
    city_name = input()
    try:
        with open("historial_global.csv", mode="w", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["usuario"] == usuario_logueado and row["ciudad"] == city_name:
                    entrys.append(row)
    except FileNotFoundError:
        print(f" No hay datos para {usuario_logueado} en {city_name}")
        return

    if not entrys:
        print(f" No hay datos para {usuario_logueado} en {city_name}")
        return

    print(f"📊 Entradas para {usuario_logueado} en {city_name}:\n")
    entrys.sort(key=itemgetter("fechahora"))

    for e in entrys:
        # Printear las filas con los datos
        pass


# aca arme el Menú principal para :
# consultar el clima,
# guardar un historial global de consultas,
# generar estadísticas globales
# ofrecer consejos de vestimenta mediante IA.
def menu_principal():
    while True:
        print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║                           MENÚ PRINCIPAL                                   ║
        ╠════════════════════════════════════════════════════════════════════════════╣
        ║ 1. Consultar Clima Actual y Guardar en Historial Global                    ║
        ║ 2. Ver Mi Historial Personal de Consultas por Ciudad                       ║
        ║ 3. Estadísticas Globales de Uso y Exportar Historial Completo              ║
        ║ 4. Consejo IA: ¿Cómo Me Visto Hoy?                                         ║
        ║ 5. Acerca De...                                                            ║
        ║ 6. Salir                                                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """)
        print("\n{:^80}\n".format("Ingrese la opción deseada:"))
        opcion = input("> ").strip()
        if opcion == "1":
            pass  # Consultar Clima Actual y Guardar en Historial Global
            consult_weather()
        elif opcion == "2":
            consult_history()
            pass  # Ver Mi Historial Personal de Consultas por Ciudad
        elif opcion == "3":
            pass  # Estadísticas Globales de Uso y Exportar Historial Completo
        elif opcion == "4":
            pass  # Consejo IA: ¿Cómo Me Visto Hoy?
        elif opcion == "5":
            pass  # Acerca De...
        elif opcion == "6":
            print("Saliendo del programa...")
            exit()
        else:
            print("{:^80}".format('Opción no válida. Intente de nuevo.'))

# Iniciar el programa mostrando el menú de acceso
menu_de_acceso()
