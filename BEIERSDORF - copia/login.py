import tkinter as tk
from tkinter import messagebox

# Simulación de base de datos de usuarios
usuarios = {
    "admin": {"password": "1234", "role": "Administrador"},
    "user1": {"password": "abcd", "role": "Usuario"},
}

# Función para autenticar usuarios
def autenticar(usuario_entry, password_entry, login_window, usuarios, ventana_principal):
    usuario = usuario_entry.get()
    contraseña = password_entry.get()

    if usuario in usuarios and usuarios[usuario]["password"] == contraseña:
        rol = usuarios[usuario]["role"]
        login_window.destroy()
        ventana_principal(rol)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función principal de la ventana después del inicio de sesión
def ventana_principal(rol):
    ventana = tk.Tk()
    ventana.title("Panel Principal")
    ventana.geometry("500x300")
    tk.Label(ventana, text=f"Bienvenido, tu rol es: {rol}", font=("Arial", 14)).pack(pady=20)
    ventana.mainloop()

# Configuración de la ventana de inicio de sesión
def ventana_login():
    login_window = tk.Tk()
    login_window.title("Inicio de Sesión")
    login_window.geometry("400x300")
    login_window.configure(bg="#f4f4f4")

    # Título
    tk.Label(login_window, text="Iniciar Sesión", font=("Arial", 20, "bold"), bg="#f4f4f4", fg="#333").pack(pady=10)

    # Usuario
    tk.Label(login_window, text="Usuario:", font=("Arial", 12), bg="#f4f4f4", fg="#555").pack(pady=5)
    usuario_entry = tk.Entry(login_window, font=("Arial", 12), width=30)
    usuario_entry.pack()

    # Contraseña
    tk.Label(login_window, text="Contraseña:", font=("Arial", 12), bg="#f4f4f4", fg="#555").pack(pady=5)
    password_entry = tk.Entry(login_window, font=("Arial", 12), width=30, show="*")
    password_entry.pack()

    # Botón de inicio de sesión
    tk.Button(
        login_window,
        text="Iniciar Sesión",
        font=("Arial", 12, "bold"),
        bg="#007BFF",
        fg="white",
        width=15,
        command=lambda: autenticar(usuario_entry, password_entry, login_window, usuarios, ventana_principal),
    ).pack(pady=20)

    # Pie de página
    tk.Label(
        login_window,
        text="Sistema de Gestión v1.0",
        font=("Arial", 10),
        bg="#f4f4f4",
        fg="#aaa",
    ).pack(side="bottom", pady=10)

    login_window.mainloop()

# Ejecutar la ventana de inicio de sesión
ventana_login()

