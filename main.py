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
ARCHIVO_USUARIOS = 'usuarios_simulados.csv' # Nombre del archivo para almacenar usuarios y contraseñas
ARCHIVO_HISTORIAL_GLOBAL = 'historial_global.csv'
ENV_FILE='.env'
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
    with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as archivo:

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
    global usuario_logueado
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
    global usuario_logueado
    print('Inicio de sesión')
    nombre_usuario = input('Nombre de usuario: ').strip()
    if nombre_usuario not in usuarios:
        print('Usuario no registrado.')
        return
    contraseña = input('Contraseña: ')
    if usuarios[nombre_usuario] == contraseña:
        usuario_logueado = nombre_usuario
        print("usuario_logueado", usuario_logueado)
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
            exit(0)
        else:
            print("{:^80}".format('Opción no válida'))

def save_weather_summary(city: str, weather: apis.Weather): #guardo los datos basicamente de las APIs
    global usuario_logueado
    file_exists = os.path.isfile(ARCHIVO_HISTORIAL_GLOBAL)

    with open(ARCHIVO_HISTORIAL_GLOBAL, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, ["usuario", "ciudad", "fechahora", "temperatura_c", "condicion_clima", "humedad_porcentaje", "viento_kmh"])

        # Escribir encabezado si el archivo no existe
        if not file_exists:
            writer.writeheader()

        date_time_string = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        assert(usuario_logueado is not None)
        writer.writerow({
            "usuario": usuario_logueado,
            "ciudad": city,
            "fechahora": date_time_string,
            "temperatura_c": weather.temp.value,
            "condicion_clima": weather.description,
            "humedad_porcentaje": weather.humidity.value,
            "viento_kmh": weather.wind_speed.value
        })

def mostrar_en_recuadro(texto):
    lineas = texto.strip().split('\n')
    largo = max(len(linea) for linea in lineas)
    borde_superior = '╔' + '═' * (largo + 2) + '╗'
    borde_medio    = '║ {:<' + str(largo) + '} ║'
    borde_inferior = '╚' + '═' * (largo + 2) + '╝'

    print(borde_superior)
    for linea in lineas:
        print(borde_medio.format(linea))
    print(borde_inferior)

#Historial de consultas y consultar el clima
last_request = None
last_city = None
def consult_weather():
    global last_request
    global last_city
    print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ Ingrese el nombre de una ciudad porfavor                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
            """)
    city_name = input("Ciudad: ").strip()

    try:
      weather = apis.get_weather(city_name)
      

    #Si la API devuelve None o datos vacíos
      if not weather or isinstance(weather, str):
        print("No se pudo obtener el clima para esa ciudad. Revise el nombre.")
        return

    except Exception as e:
     print("Error al consultar el clima: Asegurese de introducir el nombre de la ciudad correctamente")
     return


    print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ Clima Actual de {city_name}                                               ║ 
╚════════════════════════════════════════════════════════════════════════════╝
            """) #esa parte del cuadro desfasada hace que se printee bien nose porque si no se imprime un espacio atras xd
    mostrar_en_recuadro(str(weather))  #ya esta formateado el todo que puso alejandro

    print("""\n

        """)

    save_weather_summary(city_name, weather)
    last_request =  weather
    last_city = city_name

def consult_history():
    global usuario_logueado
    entries = []
    print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ Ingrese el nombre de una ciudad porfavor                                   ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """)
    city_name = input()
    try:
        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["usuario"] == usuario_logueado and row["ciudad"] == city_name:
                    entries.append(row)
    except FileNotFoundError:
        print(f" No hay datos para {usuario_logueado} en {city_name}")
        return

    if not entries:
        print(f" No hay datos para {usuario_logueado} en {city_name}")
        return

    print(f"📊 Entradas para {usuario_logueado} en {city_name}:\n")
    entries.sort(key=itemgetter("fechahora"))

    max_column_width = 0

    for row in entries:
        for value in row.values():
            if len(value) > max_column_width:
                max_column_width = len(value)

    for value in entries[0].keys():
        if len(value) > max_column_width:
            max_column_width = len(value)
    
    print("| ", end="")
    for value in entries[0].keys():
        print(f"{value.center(max_column_width)}",  end="| ")

    print("")

    for e in entries:
        print("| ", end="")
        for value in e.values():
            print(f"{value:<{max_column_width}}", end="| ")
        print("")


def global_statistics():
    try:
        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            total_consultas = 0
            temperaturas = []
            ciudad_consultas = {}
            climate_conditions = {}

            for row in reader:
                total_consultas += 1

                ciudad = row.get("ciudad", "").strip()
                clima = row.get("condicion_clima", "").strip()

                if ciudad:
                    ciudad_consultas[ciudad] = ciudad_consultas.get(ciudad, 0) + 1
                if clima:
                    climate_conditions[clima] = climate_conditions.get(clima, 0) + 1

                temp_str = row.get("temperatura", "").replace(",", ".").strip()
                try:
                    temp = float(temp_str)
                    temperaturas.append(temp)
                except ValueError:
                    pass

            if not total_consultas:
                print("No hay datos en el historial.")
                return

            ciudad_mas_consultada = max(ciudad_consultas, key=ciudad_consultas.get)
            promedio_temp = sum(temperaturas) / len(temperaturas) if temperaturas else 0

        
            print(f"\n Estadísticas Globales:")
            print(f"Ciudad más consultada: {ciudad_mas_consultada}")
            print(f"Temperatura promedio: {promedio_temp:.2f}°C")
            print(f"Total de consultas: {total_consultas}")

            
            print("\n Número de consultas por ciudad:")
            ciudad_labels = list(ciudad_consultas.keys())

            ciudad_vals = list(ciudad_consultas.values())

            charts.bar(ciudad_vals, ciudad_labels, 6, 4, 5)

            
            print("\n Distribución de condiciones climáticas:")
            clima_labels = list(climate_conditions.keys())

            clima_vals = list(climate_conditions.values())

            charts.pie(clima_vals, clima_labels, r=1.0)

    except FileNotFoundError:
        print("El archivo 'historial_global.csv' no fue encontrado.")


def ask_for_api_key():
    print("\n\nPara poder usar el consejo de la IA debes generar una llave de gemini. Para hacerlo ve a 'https://aistudio.google.com/apikey', crea una cuenta si es necesario y genera una llave. Luego ingresala aquí.")
    key = input("Ingresar llave: ")
    with open(ENV_FILE, "a") as file:
        file.write(f"\nGEMINI_KEY={key}")


def ai_advice():
    global last_request
    global last_city

    env = apis.read_env_file(ENV_FILE)
    if "GEMINI_KEY" not in env.keys():
        ask_for_api_key()
        env = apis.read_env_file(ENV_FILE)


    print("""
        ╔════════════════════════════════════════════════════════════════════════════╗
        ║ 1 - Utilizar los datos de la última consulta                               ║
        ║ 2 - Realizar una nueva consulta para el consejo                            ║
        ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    option = input("Elegí una opción: ").strip()


    if option == '1':
        if last_request is None:
            print("No hay datos de consulta previa. Por favor realiza una nueva consulta.")
            return
        weather = last_request
        ok, tip = apis.get_advice_gemini(weather, api_key=env["GEMINI_KEY"])
        if ok:
            print(f"\n Consejo para la ciudad de {last_city.title()}: {tip}")
        else:
            print(f" Error al obtener consejo: {tip}")

    elif option == '2':
        place = input("¿Para qué ciudad querés el consejo?: ").strip()
        weather = apis.get_weather(place, openweathermap_api_key=None) # TODO
        if not weather:
            print("No se pudo obtener el clima para esa ciudad.")
            return
        # Guarda la consulta actual para futuras referencias
           
        ok, tip = apis.get_advice_gemini(weather, api_key=env["GEMINI_KEY"])
        if ok:
            print(f"\n Consejo: {tip}")
        else:
            print(f" Error al obtener consejo: {tip}")

    else:
        print("Opción inválida. Por favor elige 1 o 2.")

def mostrar_acerca_de():
    NOMBRE_DE_GRUPO = "Pibes jansons"
    # Aca falta definir el nombre del grupo, pero hay que cambiar el texto sino se rompe el formato
    print(f"""
    ╔═════════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                                       ACERCA DE...                                              ║
    ╠═════════════════════════════════════════════════════════════════════════════════════════════════╣
    ║    WeatherBuddy - GuardiánClima ITBA                                                            ║  
    ║                                                                                                 ║           
    ║    WeatherBuddy es una aplicación desarrollada por el grupo "{NOMBRE_DE_GRUPO}" del ITBA,       ║
    ║    diseñada para ofrecer información meteorológica precisa, consejos personalizados y           ║
    ║    estadísticas de uso, todo en una experiencia interactiva y educativa.                        ║
    ║                                                                                                 ║
    ║    Descripción de la aplicación:                                                                ║
    ║    WeatherBuddy permite a los usuarios consultar el clima actual de cualquier ciudad,           ║
    ║    guardar un historial global de consultas, generar estadísticas y gráficos a partir de        ║
    ║    los datos recolectados, y recibir consejos de vestimenta personalizados mediante IA.         ║
    ║                                                                                                 ║
    ║    Guía de uso de las opciones del menú:                                                        ║
    ║    - Menú de Acceso: Permite iniciar sesión con un usuario existente o registrar uno nuevo.     ║
    ║    El registro requiere un nombre de usuario válido y una contraseña segura.                    ║
    ║    - 1. Consultar Clima Actual y Guardar en Historial Global: Solicita el nombre de una         ║
    ║    ciudad, obtiene el clima actual desde APIs externas y guarda la consulta en el historial.    ║
    ║    - 2. Ver Mi Historial Personal de Consultas por Ciudad: Permite revisar el historial de      ║
    ║    consultas realizadas por el usuario para una ciudad específica.                              ║ 
    ║    - 3. Estadísticas Globales de Uso y Exportar Historial Completo: Genera estadísticas de      ║
    ║    uso y permite exportar el historial completo en formato CSV, útil para la creación de        ║
    ║    gráficos.                                                                                    ║
    ║    - 4. Consejo IA: ¿Cómo Me Visto Hoy?: Utiliza IA para sugerir vestimenta adecuada según      ║
    ║    el clima consultado.                                                                         ║
    ║    - 5. Acerca De...: Muestra esta descripción detallada.                                       ║
    ║    - 6. Cerrar Sesión: Cierra la sesión y vuelve al menu de inicio                              ║
    ║                                                                                                 ║
    ║    Funcionamiento interno:                                                                      ║
    ║    - Creación de usuarios: El registro de usuarios es simulado y requiere una contraseña que    ║
    ║    cumpla criterios de seguridad (mínimo 8 caracteres, mayúsculas, minúsculas, dígitos y        ║
    ║    caracteres especiales). Se recomienda el uso de contraseñas robustas.                        ║
    ║    - Seguridad: Las credenciales se almacenan de forma simulada e insegura en archivos CSV.     ║
    ║    Para mayor seguridad, se utiliza hashing (SHA-256) en la función de encriptado, aunque       ║
    ║    en un entorno real se recomienda el uso de técnicas avanzadas y almacenamiento seguro.       ║
    ║    - Obtención de datos: El clima se obtiene mediante APIs externas y se almacena en un         ║
    ║    historial global para cada usuario.                                                          ║
    ║    - Estadísticas y gráficos: El historial puede exportarse a CSV para su análisis y            ║
    ║    visualización mediante gráficos.                                                             ║
    ║    - IA para consejos: Se integra una IA que, en base a los datos meteorológicos, sugiere       ║
    ║    cómo vestirse apropiadamente.                                                                ║
    ║                                                                                                 ║
    ║    Desarrolladores:                                                                             ║
    ║    - Patricio Aldasoro                                                                          ║
    ║    - Alejandro De Ugarriza Mohnblatt                                                            ║
    ║    - Zoe María Perez Colman                                                                     ║
    ║    - Tomás Spurio                                                                               ║
    ║    - Bautista Andrés Peral                                                                      ║
    ║                                                                                                 ║
    ║    Grupo: {NOMBRE_DE_GRUPO} (Grupo 42)                                                          ║
    ╚═════════════════════════════════════════════════════════════════════════════════════════════════╝      
    """)

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
            consult_weather() # Consultar Clima Actual y Guardar en Historial Global
        elif opcion == "2":
            consult_history() # Ver Mi Historial Personal de Consultas por Ciudad
        elif opcion == "3":
            pass
            #global_statistics() # Estadísticas Globales de Uso y Exportar Historial Completo
        elif opcion == "4":
            ai_advice() # Consejo IA: ¿Cómo Me Visto Hoy?
        elif opcion == "5":
            mostrar_acerca_de() # Acerca De...
        elif opcion == "6":
            print("Saliendo del programa...")
            exit(0)
        else:
            print("{:^80}".format('Opción no válida. Intente de nuevo.'))

# Iniciar el programa mostrando el menú de acceso
menu_de_acceso()
