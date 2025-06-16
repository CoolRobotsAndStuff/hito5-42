# Integrar Api's necesarias
# AYUDA NO SE USAR APIS AAAAAAAAAA
# Importar las librerías necesarias
import io
import hashlib
import apis as apis
import charts as charts
import csv
import os
from datetime import datetime
from operator import itemgetter
import shutil

MATPLOTLIB_SUPPORT = True
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from PIL import Image
except ImportError:
    MATPLOTLIB_SUPPORT = False

# Declarar Constantes
ARCHIVO_USUARIOS = 'usuarios_simulados.csv' # Nombre del archivo para almacenar usuarios y contraseñas
ARCHIVO_HISTORIAL_GLOBAL = 'historial_global.csv'
ENV_FILE='.env'
TIMESTAMP_FORMAT = "%d-%m-%Y %H:%M:%S"
usuario_logueado = None

charts.windows_enable_unicode_and_ansi()

# Banner del programa
banner = '''
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
'''

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
    clear_screen()
    global usuario_logueado
    print(center_multiline('----- Registro de usuario -----'))
    nombre_usuario = ""
    nombre_usuario = input('          Nombre de usuario: ').strip()
    if not nombre_usuario.isalpha():
        print(center_multiline("El nombre de usuario contiene caracteres inválidos, intente nuevamente."))
        press_enter_dialog()
        return
    if nombre_usuario in usuarios:
        print(center_multiline('El usuario ya existe, ingrese otro.'))
        press_enter_dialog()
        return
    while True:
        contraseña = input('          Contraseña: ')
        valido, mensajes = validar_contrasena(contraseña)
        if not valido:
            print('          Contraseña insegura:')
            for msg in mensajes:
                print(" "*10, end="")
                print(msg)
            continue
        confirmacion = input('          Confirme contraseña: ')
        if contraseña != confirmacion:
            print('          Las contraseñas no coinciden, intente nuevamente.')
            continue
        usuarios[nombre_usuario] = contraseña
        guardar_usuarios(nombre_usuario, contraseña)
        usuario_logueado = nombre_usuario
        clear_screen()
        print(f'Usuario registrado correctamente. Bienvenido, {usuario_logueado}! \n')
        menu_principal()
        break

# Función para iniciar sesión con un usuario ya registrado.
def iniciar_sesion(usuarios):
    clear_screen()
    global usuario_logueado
    print("\n\n")
    print(center_multiline('------ Inicio de sesión ------'))
    nombre_usuario = input('\n\n          Nombre de usuario: ').strip()
    if nombre_usuario not in usuarios:
        print('Usuario no registrado. Por favor revise el nombre de usuario y vuelva a intentar o registre un nuevo usuario.')
        press_enter_dialog()
        return
    contraseña = input('          Contraseña: ')
    if usuarios[nombre_usuario] == contraseña:
        usuario_logueado = nombre_usuario
        clear_screen()
        print(center_multiline(f'Bienvenido, {usuario_logueado}!'))
        menu_principal()  # Mostrar menú principal tras inicio de sesión correcto
    else:
        print(center_multiline('Contraseña incorrecta.'))
        while True:
            print(center_multiline("¿Desea intentar de nuevo (1) o volver al menú de inicio (2)?"))
            opcion = input("          > ").strip()
            if opcion == '1':
                return iniciar_sesion(usuarios)
            elif opcion == '2':
                return  # Vuelve al menú de acceso (menu_de_acceso)
            else:
                print(center_multiline("Opción no válida. Ingrese 1 para reintentar o 2 para volver al menú de acceso."))

# Menu de inicio pre-registro.
# De aca se va al menu principal
def menu_de_acceso():
    usuarios = cargar_usuarios()
    while True:
        clear_screen()
        print(center_multiline(banner))
        print("")
        input(center_multiline("Presione [Enter] para empezar"))
        while True:
            clear_screen()
            print(center_multiline("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                           MENÚ DE INICIO                                   ║
    ╠════════════════════════════════════════════════════════════════════════════╣
    ║   1. Iniciar sesión                                                        ║
    ║   2. Registrar usuario                                                     ║
    ║   3. Salir                                                                 ║
    ╚════════════════════════════════════════════════════════════════════════════╝
            """))
            print(center_multiline("Ingrese la opción deseada"))
            opcion = input("         > ").strip()
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

        date_time_string = datetime.now().strftime(TIMESTAMP_FORMAT)
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
    clear_screen()
    global last_request
    global last_city
    print(center_multiline("""
╔════════════════════════════════════════════════════════════════════════════╗
║ Ingrese el nombre de una ciudad porfavor                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
    """))
    city_name = input("          Ciudad: ")
    city_name = normalize_city_name(city_name)

    clear_screen()

    try:
        weather = apis.get_weather(city_name)

        #Si la API devuelve None o datos vacíos
        if not weather or isinstance(weather, str):
            print("No se pudo obtener el clima para esa ciudad. Revise el nombre.")
            press_enter_dialog()
            return

    except Exception as e:
        print("Error al consultar el clima: Asegurese de introducir el nombre de la ciudad correctamente")
        press_enter_dialog()
        return


    print(center_multiline(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ Clima Actual de {city_name:<25}                                  ║ 
╚════════════════════════════════════════════════════════════════════════════╝
            """))
    print(center_multiline(str(weather), pad_right=False))
    print("\n")
    press_enter_dialog()

    save_weather_summary(city_name, weather)
    last_request =  weather
    last_city = city_name

def normalize_city_name(name):
    return name.strip().lower()

# TODO show available cities
def consult_history():
    clear_screen()
    global usuario_logueado
    entries = []
    print(center_multiline("""
╔════════════════════════════════════════════════════════════════════════════╗
║ Ingrese el nombre de una ciudad porfavor                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
        """))
    city_name = input("          > ")
    try:
        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["usuario"] == usuario_logueado and row["ciudad"] == normalize_city_name(city_name):
                    entries.append(row)
    except FileNotFoundError:
        print(f" No hay datos para {usuario_logueado} en {city_name}")
        press_enter_dialog()
        return

    if not entries:
        print(f" No hay datos para {usuario_logueado} en {city_name}")
        press_enter_dialog()
        return

    print(center_multiline(f"📊 Entradas para {usuario_logueado} en {normalize_city_name(city_name).title()}:\n"))
    entries.sort(key=itemgetter("fechahora"))

    max_column_widths = [0]*len(entries[0].keys())

    for row in entries:
        for i, value in enumerate(row.values()):
            if len(value) > max_column_widths[i]:
                max_column_widths[i] = len(value)

    for i, value in enumerate(entries[0].keys()):
        if len(value) > max_column_widths[i]:
            max_column_widths[i] = len(value)

    table = ""
    
    table += "| "
    for i, value in enumerate(entries[0].keys()):
        table += f"{value.center(max_column_widths[i])}" + " | "

    table += "\n"

    for e in entries:
        table += "| " 
        for i, value in enumerate(e.values()):
            padding = max_column_widths[i]
            table += f"{value:<{padding}}" + " | "
        table += "\n"

    print(center_multiline(table, pad_right=False))

    press_enter_dialog()

def clear_screen():
    print("\033[H\033[J")

# TODO show global stats
# TODO export matplotlib graphics/csv
def stats_prompt():
    print("    1 - Salir     2 - Consultas por Ciudad     3 - Porcentaje de Condiciones Climáticas     4 - Temperaturas históricas por ciudad\n    5 - Estadísticas globales")

def handle_common_stats_input(ipt) -> bool:
    if ipt in ("1", "q"):
        return True
    elif ipt == "2":
        show_stats()
        return True
    elif ipt == "3":
        show_climate_percents()
        return True
    elif ipt == "4":
        show_city_temperatures(0)
        return True
    elif ipt == "5":
        global_statistics()
        return True

    return False

def show_city_temperatures(n):
    clear_screen()
    try:
        city = ""
        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            requested_cities = {}
            for row in reader:
                if row["ciudad"] not in requested_cities.keys():
                    requested_cities[row["ciudad"]] = 0
                requested_cities[row["ciudad"]] += 1

            requested_cities = dict(sorted(requested_cities.items(), key=lambda item: item[1], reverse=True))
            city = list(requested_cities.keys())[n%len(requested_cities)]

        temperatures = {}
        terminal_size = shutil.get_terminal_size()
        print("")
        print("--------- Temperaturas de Ciudades a Través del Tiempo --------".center(terminal_size.columns))
        print("\n")
        print(f"(p) Previa <----- {city.title()} ----> (n) Siguiente".center(terminal_size.columns))

        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["ciudad"] == city:
                    dt = datetime.strptime(row["fechahora"], TIMESTAMP_FORMAT)
                    seconds_since_epoch = int(dt.timestamp())
                    temperatures[seconds_since_epoch] = {
                        "temp": float(row["temperatura_c"]),
                        "display_time": row["fechahora"]
                    }

        temperatures = dict(sorted(temperatures.items()))

        ys = [v["temp"] for v in temperatures.values()]
        xs = [k for k in temperatures.keys()]
        labels = [v["display_time"] for v in temperatures.values()]
        if len(ys) <= 1:
            print("\n"*10)
            print("Se necesitan por lo menos dos datos de temperatura de cada ciudad para ver las estadísticas.".center(terminal_size.columns))
            print("\n"*10)
        else:
            width = terminal_size.columns-7
            if width > 80:
                width -= 30
            charts.line(labels, xs, ys, w=width, h=20, div_n=5, vpadding=2)

            #charts.pie(list(requested_weathers.values()), list(requested_weathers.keys()), r=10)
        print("\n\n    Opciones:\n    n - Siguiente   p - Previa   v - Ver Gráficos")
        stats_prompt()
        while True:
            ipt = input("\n > ")

            if ipt == "n":
                show_city_temperatures(n+1)
                break

            elif ipt == "p":
                show_city_temperatures(n-1)
                break

            elif ipt == "v":
                if MATPLOTLIB_SUPPORT:
                    dates = [datetime.strptime(date, TIMESTAMP_FORMAT) for date in labels]

                    plt.figure(figsize=(12, 6), dpi=300)
                    plt.plot(dates, ys, marker='o')
                    plt.title(f'Temperaturas en {city.title()} a través del tiempo')
                    plt.xlabel('Fecha y Hora')
                    plt.ylabel('Temperatura en Celcius')
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(TIMESTAMP_FORMAT))

                    plt.ylim(min(ys) - 2, max(ys) + 2)
                    plt.xticks(rotation=15)

                    plt.grid()
                    try:
                        plt.show(True)
                    except:
                        with io.BytesIO() as buf:
                            plt.savefig(buf, format='png')
                            buf.seek(0)
                            Image.open(buf).show("chart")
                else:
                    clear_screen()
                    print(center_multiline("\n\n\nNo se pueden mostar gráfios, la librería matplotlib no está instalada.\nInstálela con 'pip install matplotlib'"))
                    press_enter_dialog()

                show_city_temperatures(n)
                return


            elif handle_common_stats_input(ipt):
                break

        clear_screen()

    except FileNotFoundError:
        print(center_multiline("\n\n\nTodavía no hay datos de uso! Haz por lo menos una consulta para ver las estadísticas."))
        press_enter_dialog()
        return

def show_climate_percents():
    clear_screen()
    try:
        terminal_size = shutil.get_terminal_size()
        print("")
        print("--------- Porcentajes de Condiciones Climáticas --------".center(terminal_size.columns))
        print("\n")
        requested_weathers = {}
        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["condicion_clima"] not in requested_weathers.keys():
                    requested_weathers[row["condicion_clima"]] = 0
                requested_weathers[row["condicion_clima"]] += 1
            
            width = terminal_size.columns-7
            if width > 80:
                width -= 10
            charts.pie(list(requested_weathers.values()), list(requested_weathers.keys()), r=10)
        
        print("    Opciones:\n    v - Ver Gráficos")
        stats_prompt()
        while True:
            ipt = input("\n > ")

            if ipt == "v":
                if MATPLOTLIB_SUPPORT:
                    plt.figure(dpi=300)
                    plt.pie(list(requested_weathers.values()), labels=list(requested_weathers.keys()))
                    plt.axis('equal')
                    try:
                        plt.show(True)
                    except:
                        with io.BytesIO() as buf:
                            plt.savefig(buf, format='png')
                            buf.seek(0)
                            Image.open(buf).show("chart")

                else:
                    clear_screen()
                    print(center_multiline("\n\n\nNo se pueden mostar gráfios, la librería matplotlib no está instalada.\nInstálela con 'pip install matplotlib'"))
                    press_enter_dialog()

                show_climate_percents()
                return

            elif handle_common_stats_input(ipt):
                break

        clear_screen()

    except FileNotFoundError:
        print(center_multiline("\n\n\nTodavía no hay datos de uso! Haz por lo menos una consulta para ver las estadísticas."))
        press_enter_dialog()
        return


def show_stats():
    clear_screen()
    try:
        terminal_size = shutil.get_terminal_size()
        print("--------- Consultas por Ciudad --------".center(terminal_size.columns))
        print("\n")
        requested_cities = {}
        with open("historial_global.csv", mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["ciudad"] not in requested_cities.keys():
                    requested_cities[row["ciudad"]] = 0
                requested_cities[row["ciudad"]] += 1
            
        width = terminal_size.columns-7
        if width > 80:
            width -= 10
        charts.bar(list(requested_cities.values()), list(k.title() for k in requested_cities.keys()), width, h=20, div_n=6)

        print("\n\n    Opciones:\n    v - Ver Gráficos")
        stats_prompt()
        while True:
            ipt = input("\n > ")
            if ipt == "v": 
                if MATPLOTLIB_SUPPORT:
                    plt.figure(figsize=(12, 6), dpi=300)
                    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
                    plt.bar(list(requested_cities.keys()), list(requested_cities.values()), color=colors)
                    plt.xticks(rotation=20)
                    try:
                        plt.show(True)
                    except:
                        with io.BytesIO() as buf:
                            plt.savefig(buf, format='png')
                            buf.seek(0)
                            Image.open(buf).show("chart")

                else:
                    clear_screen()
                    print(center_multiline("\n\n\nNo se pueden mostar gráfios, la librería matplotlib no está instalada.\nInstálela con 'pip install matplotlib'"))
                    press_enter_dialog()
                show_stats()
                return

            elif handle_common_stats_input(ipt):
                break

        clear_screen()

    except FileNotFoundError:
        print(center_multiline("\n\n\nTodavía no hay datos de uso! Haz por lo menos una consulta para ver las estadísticas."))
        press_enter_dialog()
        return


def global_statistics():
    try:
        clear_screen()
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

                temp_str = row.get("temperatura_c", "").replace(",", ".").strip()
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

        
            print(center_multiline(f"""\n\n\n
-------- Estadísticas Globales --------

     - Ciudad más consultada: {ciudad_mas_consultada.title()}
     
     - Temperatura promedio: {promedio_temp:.2f}°C
     
     - Total de consultas: {total_consultas} """))

        print("\n\n    Opciones:\n")
        stats_prompt()
        while True:
            ipt = input("\n > ")

            if handle_common_stats_input(ipt):
                break

    except FileNotFoundError:
        print("El archivo 'historial_global.csv' no fue encontrado.")


def ask_for_api_key():
    clear_screen()
    print("\n\n    Para poder usar el consejo de la IA debes generar una llave de gemini. Para hacerlo ve a 'https://aistudio.google.com/apikey', crea una cuenta si es necesario y genera una llave. Luego ingresala aquí.")
    key = input("Ingresar llave: ")
    with open(ENV_FILE, "a") as file:
        file.write(f"\nGEMINI_KEY={key}")

    print(center_multiline("Llave ingresada correctamente!"))
    press_enter_dialog()

def center_multiline(text: str, pad_right=True) -> str:
    width = shutil.get_terminal_size().columns
    lines = text.splitlines()
    
    def calculate_line_width(line: str) -> int:
        return len(line)
        return sum(2 if ord(char) > 0x7F else 1 for char in line)

    max_line_width = max(calculate_line_width(line) for line in lines) if lines else 0

    left_padding = ((width//2) - (max_line_width//2))
    
    centered_lines = []
    
    for line in lines:
        line_width = calculate_line_width(line)
        
        # Calculate the padding needed to center the line
        right_padding = width - left_padding - line_width
        centered_line = ""
        if left_padding > 0:
            centered_line += ' ' * left_padding
        centered_line += line
        if right_padding > 0 and pad_right:
            centered_line += ' ' * right_padding
        
        centered_lines.append(centered_line)
    
    # Join the centered lines into a single string with newlines
    return '\n'.join(centered_lines)


def ai_advice():
    global last_request
    global last_city

    env = apis.read_env_file(ENV_FILE)
    if "GEMINI_KEY" not in env.keys():
        ask_for_api_key()
        env = apis.read_env_file(ENV_FILE)

    while True:

        clear_screen()
        print(center_multiline("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║ 1 - Utilizar los datos de la última consulta                               ║
    ║ 2 - Realizar una nueva consulta para el consejo                            ║
    ║ 3 - Salir                                                                  ║
    ╚════════════════════════════════════════════════════════════════════════════╝
        """))
        print(center_multiline("Elegí una opción"))
        option = input("           > ").strip()

        if option == '1':
            if last_request is None:
                print(center_multiline("No hay datos de consulta previa. Por favor realiza una nueva consulta."))
                press_enter_dialog()
                continue
            weather = last_request
            try:
                ok, tip = apis.get_advice_gemini(weather, api_key=env["GEMINI_KEY"])
                if ok:
                    print(center_multiline(f"\n Consejo para la ciudad de {last_city.title()}: {tip}"))
                else:
                    print(center_multiline(f"Error al obtener consejo: {tip}"))
            except:
                print(center_multiline(f"Error al obtener consejo, asegúrese de estar conectado a internet."))
            press_enter_dialog()


        elif option == '2':
            place = input("          ¿Para qué ciudad querés el consejo?: ").strip()

            try:
                weather = apis.get_weather(place, openweathermap_api_key=None) # TODO
                if not weather:
                    print(center_multiline("No se pudo obtener el clima para esa ciudad."))
                    press_enter_dialog()
                    return
            except:
                print(center_multiline(f"Error al obtener consejo, asegúrese de estar conectado a internet y haber escrito correctamente el nombre de la ciudad."))
                press_enter_dialog()
                return
            # Guarda la consulta actual para futuras referencias
            
            ok, tip = apis.get_advice_gemini(weather, api_key=env["GEMINI_KEY"])
            clear_screen() 
            terminal_size = shutil.get_terminal_size()
            print(center_multiline(f"\n\n\n------- Clima en {place} --------\n\n"))
            print(center_multiline(str(weather), pad_right=False))
            print("\n")
            if ok:
                print(center_multiline(f"Consejo: {tip}"))
            else:
                print(center_multiline(f"Error al obtener consejo: {tip}"))

            press_enter_dialog()
            return

        elif option == "3":
            return

        else:
            print("Opción inválida.")

def press_enter_dialog():
    print("\n")
    input(center_multiline("Presiona [Enter] para continuar"))

def mostrar_acerca_de():
    clear_screen()
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
    press_enter_dialog()

# aca arme el Menú principal para :
# consultar el clima,
# guardar un historial global de consultas,
# generar estadísticas globales
# ofrecer consejos de vestimenta mediante IA.
def menu_principal():
    global usuario_logueado
    global last_city
    global last_request
    while True:
        clear_screen()
        print(center_multiline("""
╔════════════════════════════════════════════════════════════════════════════╗
║                           MENÚ PRINCIPAL                                   ║
╠════════════════════════════════════════════════════════════════════════════╣
║ 1. Consultar Clima Actual y Guardar en Historial Global                    ║
║ 2. Ver Mi Historial Personal de Consultas por Ciudad                       ║
║ 3. Estadísticas Globales de Uso y Exportar Historial Completo              ║
║ 4. Consejo IA: ¿Cómo Me Visto Hoy?                                         ║
║ 5. Acerca De...                                                            ║
║ 6. Cerrar sesión                                                           ║
║ 7. Salir                                                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
        """))
        print(center_multiline("Ingrese la opción deseada"))
        opcion = input("         > ").strip()
        if opcion == "1":
            consult_weather() # Consultar Clima Actual y Guardar en Historial Global
        elif opcion == "2":
            consult_history() # Ver Mi Historial Personal de Consultas por Ciudad
        elif opcion == "3":
            show_stats() # Estadísticas Globales de Uso y Exportar Historial Completo
        elif opcion == "4":
            ai_advice() # Consejo IA: ¿Cómo Me Visto Hoy?
        elif opcion == "5":
            mostrar_acerca_de() # Acerca De...
        elif opcion == "6":
            usuario_logueado = None
            last_request = None
            last_city = None
            menu_de_acceso()
            return
        elif opcion == "7":
            print("Saliendo del programa...")
            exit(0)
        else:
            print("{:^80}".format('Opción no válida. Intente de nuevo.'))

        # TODO: opción de cerrar sesión

# Iniciar el programa mostrando el menú de acceso
if __name__ == "__main__":
    menu_de_acceso()
