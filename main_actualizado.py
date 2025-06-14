# Integrar Api's necesarias
# AYUDA NO SE USAR APIS AAAAAAAAAA
# Importar las librerías necesarias
import hashlib
import pandas as pd
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
       | | |_ | | | |/ _` | '__/ _` | |/ _` | '_ \   / _` |/ _ \ | | |    | | | '_ ` _ \ / _` |
       | |__| | |_| | (_| | | | (_| | | (_| | | | | | (_| |  __/ | | |____| | | | | | | | | (_| |
        \_____|\__,_|\__,_|_|  \__,_|_|\__,_|_| |_|  \__,_|\___|_|  \_____|_|_|_| |_| |_|\__,_|                                                                                     
        Grupo 42: Patricio Aldasoro           Alejandro De Ugarriza Mohnblatt                    
                  Zoe María Perez Colman      Tomás Spurio
                  Bautista Andrés Peral                                                                                       
''')

# Función para cargar los usuarios desde el archivo ya existente o crear uno nuevo si no existe.
def cargar_usuarios():
    usuarios = {}
    try:
        with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                partes = linea.strip().split(',')
                if len(partes) == 2:
                    nombre_usuario, hash_contra = partes
                    usuarios[nombre_usuario] = hash_contra
    except FileNotFoundError:
        pass
    return usuarios

# Función para guardar los usuarios en el archivo.
def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as archivo:
        for nombre_usuario, hash_contra in usuarios.items():
            archivo.write(nombre_usuario + ',' + hash_contra + '\n')

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
    nombre_usuario = input('Nombre de usuario: ').strip()
    if nombre_usuario in usuarios:
        print('El usuario ya existe')
        return
    while True:
        contrasena = input('Contraseña: ')
        valido, mensajes = validar_contrasena(contrasena)
        if not valido:
            print('Contraseña insegura:')
            for msg in mensajes:
                print(msg)
            continue
        confirmacion = input('Confirme contraseña: ')
        if contrasena != confirmacion:
            print('Las contraseñas no coinciden')
            continue
        usuarios[nombre_usuario] = encriptar_contrasena(contrasena)
        guardar_usuarios(usuarios)
        print('Usuario registrado correctamente')
        break

nombre_usuario : str #hice "publica" la variable para poder usar el nombre del usuario en consult weather, ya q  se define en iniciar sesion  me es util
# Función para iniciar sesión con un usuario ya registrado.
def iniciar_sesion(usuarios):
    print('Inicio de sesión')
    nombre_usuario = input('Nombre de usuario: ').strip()
    if nombre_usuario not in usuarios:
        print('Usuario no registrado')
        return
    contrasena = input('Contraseña: ')
    if usuarios[nombre_usuario] == encriptar_contrasena(contrasena):
        print(f'Bienvenido, {nombre_usuario}!')
        menu_principal()  # Mostrar menú principal tras inicio de sesión correcto
    else:
        print('Contraseña incorrecta')
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



#Formatear  unificar los datos de las APIS de clima
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


def save_weather_summary(username,source: str, city: str, summary: str, filename="historial_global.csv"): #guardo los datos basicamente de las APIs
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        # Escribir encabezado si el archivo no existe
        if not file_exists:
            writer.writerow(["Usuario logueado: {username}"])
            writer.writerow(["Fuente", "Ciudad", "Resumen"])

        # Escribir los datos
        writer.writerow(["Usuario logueado: {username}"])
        writer.writerow([source, city, summary])

#Historial de consultas y consultar el clima
city_name : str
def Consult_weather(user):
    print(f"""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ Ingrese el nombre de una ciudad porfavor                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
            """)
    city_name = input()
    success, data = apis.get_weather_openweathermap(city_name.casefold())#weather options
    success_ow, data_ow = apis.get_weather_openweathermap(city_name.casefold())
    w1 = format_weather_openmeteo(data,city_name)
    w2 = {format_weather_report(data_ow,city_name)} 

    if(success and success_ow):
        print(f"""\n
        ╔════════════════════════════════════════════════════════════════╗
        ║                                                                ║   
        ║    {format_weather_openmeteo(data,city_name)}                  ║    
        ║    {format_weather_report(data_ow,city_name)}                  ║
        ╚════════════════════════════════════════════════════════════════╝
    """)
        save_weather_summary(user,"openmeteo",city_name, w1 )#guardo los datos obtenidos y formateados de openmeteo
        save_weather_summary(user,"openweathermap",city_name, w2 )#guardo los datos obtenidos y formateados de openweathermap xd
    else:
        print(" Error al obtener el clima:", data)
        print(" Error al obtener el clima:", data_ow)

            
   

    
def Consult_History():
    entrys = []
    print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ Ingrese el nombre de una ciudad porfavor                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """)
    city_name = input()
    file = pd.read("historial_global.csv")
    for row in file:
        if(row("Usuario logueado" ) == nombre_usuario and row("Ciudad")== city_name):
            entrys.append(row)
            entrys.sort(key= itemgetter("Fecha", "Hora"))

        if not entrys:
            print(f" No hay datos para {nombre_usuario} en {city_name}")
            return

    print(f"📊 Entradas para {nombre_usuario} en {city_name}:\n")
    for e in entrys:
        print(f" {e['Fecha']}  {e['Hora']}")
        print(f"{e['Resumen']}\n")


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
            Consult_weather()
        elif opcion == "2":
            Consult_History(nombre_usuario)
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
