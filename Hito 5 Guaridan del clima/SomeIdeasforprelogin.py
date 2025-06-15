import pandas as pd
import tkinter as tk
from tkinter import messagebox
import csv
import math
import string
import random

maxlength = 20
Problems = []
# GUI setup
root = tk.Tk()
root.title("Guardidan del clima ITBA")
root.geometry("300x200")

# Input fields
tk.Label(root, text="Usuario:").pack(padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Contraseña:").pack(padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Inicializo variables necesarias
User = ""
Password = ""
found = False
loging = False  # to verify if it's logging or registering, it's a trick
SafeLength = 10  # characters

# Funciones
def detectUsers(name_to_check, password_to_check):
    global found, loging
    with open('usuarios_simulados.csv', newline='') as usersfile:
        reader = csv.DictReader(usersfile)
        for row in reader:
            if loging:
                if row['username'] == name_to_check and row['password'] == password_to_check:
                    found = True
                    break
            else:
                if row['username'] == name_to_check:
                    found = True
                    break
        else:
            found = False

def Login():
    global User, Password, loging
    loging = True
    User = username_entry.get()
    Password = password_entry.get()
    detectUsers(User, Password)
    if not found:
        messagebox.showerror("Error", "El usuario no existe o contraseña incorrecta.")
        return True
    else:
        messagebox.showinfo("Datos válidos", "Inicio de sesión correcto.")
        return False

def Register():
    global User, Password, loging
    loging = False
    User = username_entry.get()
    Password = password_entry.get()
    detectUsers(User, Password)
    if found:
        messagebox.showerror("Error", "El usuario ya existe.")
        return True
    else:
        messagebox.showinfo("Datos válidos", "Registrado correctamente.")
        return False

def estimate_entropy(password): #randomness of the password, like $a%vsaw·qa
    pool_size = 0
    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0

    entropy = len(password) * math.log2(pool_size)
    return entropy

def has_repetition(password, length=3):
    for i in range(len(password) - length + 1):
        if len(set(password[i:i+length])) == 1:
            return True
    return False

def has_sequence(password, length=3):
    for i in range(len(password) - length + 1):
        chunk = password[i:i+length]
        codes = [ord(c) for c in chunk]
        if all(codes[j] + 1 == codes[j+1] for j in range(len(codes)-1)):
            return True
        if all(codes[j] - 1 == codes[j+1] for j in range(len(codes)-1)):
            return True
    return False

def theres_a_problem(problem, *args):
    return problem or any(args)

def IsASafePassword(password):
    Randomness = estimate_entropy(password)
    if theres_a_problem(estimate_entropy(password) < 40, has_sequence(password), has_repetition(password)):
        if Randomness < 40:
            Problems.append("Uso de palabras comunes y falta de entropía")
        if len(password) < SafeLength:
            Problems.append("Corta longitud")
        if has_sequence(password, 3):
            Problems.append("Hay secuencias en la contraseña lo que la hace predecible")
        if has_repetition(password, 3):
            Problems.append("Hay repeticiones en la contraseña lo que la hace fácil de predecir")
        Safe_Pass = GenerateSafePassword()
        messagebox.showinfo(Safe_Pass)
        return False
    else:
        return True

def GenerateSafePassword():
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        length = random.randint(SafeLength, maxlength)
        new_password = ''.join(random.choices(characters, k=length))
        entropy = estimate_entropy(new_password)
        if not theres_a_problem(entropy < 40, has_sequence(new_password), has_repetition(new_password)):
            return new_password

def PreLogin():
    print(f"//// GUARDIAN DEL CLIMA ITBA ////")
    root.mainloop()


tk.Button(root, text="Iniciar Sesión", command=Login).pack(padx=10, pady=10)
tk.Button(root, text="Registrarse", command=Register).pack(padx=10, pady=10)