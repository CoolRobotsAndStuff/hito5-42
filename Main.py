import hashlib
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
        ║   1. Consultar clima                                                       ║
        ║   2. Ver historial de consultas                                            ║
        ║   3. Estadísticas globales                                                 ║
        ║   4. Consejos de vestimenta                                                ║
        ║   5. Salir                                                                 ║
        ╚════════════════════════════════════════════════════════════════════════════╝
        """)
        print("\n{:^80}\n".format("Ingrese la opción deseada:"))
        opción = input("> ").strip()
        if opción == "1":
            consultar_clima()
        elif opción == "2":
            historial_consultas()
        elif opción == "3":
            estadisticas_globales()
        elif opción == "4":
            consejos_vestimenta()
        elif opción == "5":
            print("Saliendo del programa...")
            exit()
        else:
            print("{:^80}".format('Opción no válida. Intente de nuevo.'))

def consultar_clima():
    # Aca va la lógica para consultar el clima
    pass

def historial_consultas():
    # Aca va la lógica para ver el historial de consultas
    pass

def estadisticas_globales():
    # Aca va la lógica para generar estadísticas globales
    pass

def consejos_vestimenta():
    # Aca va la lógica para ofrecer consejos de vestimenta
    pass

# iniciar el programa
menu_de_acceso()
