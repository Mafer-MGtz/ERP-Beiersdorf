import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style, ttk
from modulos.modulo_finanzas import modulo_finanzas, configurar_estilos
from modulos.modulo_inventarios import modulo_inventarios
from modulos.modulo_produccion import modulo_produccion
from modulos.modulo_ventas import modulo_ventas
from modulos.modulo_rrhh import modulo_rrhh
from modulos.modulo_admin import AdminWindow
from PIL import Image, ImageTk

# Diccionario de usuarios y roles
usuarios = {
    "admin": {"password": "admin123", "role": "admin"},
    "finanzas": {"password": "finanzas123", "role": "finanzas"},
    "inventarios": {"password": "inventarios123", "role": "inventarios"},
    "produccion": {"password": "produccion123", "role": "produccion"},
    "ventas": {"password": "ventas123", "role": "ventas"},
    "rrhh": {"password": "rrhh123", "role": "rrhh"},
}

# Función de autenticación
def autenticar(usuario_entry, password_entry, login_window):
    usuario = usuario_entry.get()
    contraseña = password_entry.get()

    if usuario in usuarios and usuarios[usuario]["password"] == contraseña:
        rol = usuarios[usuario]["role"]
        login_window.withdraw()  # Ocultar la ventana en lugar de destruirla
        ventana_principal(rol, login_window)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Ventana principal según rol
def ventana_principal(rol, login_window):
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión")
    ventana.geometry("800x500")
    style = Style(theme="darkly")

    # Configurar estilos generales
    configurar_estilos()

    tab_principal = ttk.Notebook(ventana, bootstyle="primary")
    tab_principal.pack(fill="both", expand=True, pady=10, padx=10)

    try:
        if rol == "admin":
            tab_admin = ttk.Frame(tab_principal)
            tab_principal.add(tab_admin, text="Admin")
            AdminWindow(tab_admin)

        elif rol == "finanzas":
            tab_finanzas = ttk.Frame(tab_principal)
            tab_principal.add(tab_finanzas, text="Finanzas")
            modulo_finanzas(tab_finanzas)

        elif rol == "inventarios":
            tab_inventarios = ttk.Frame(tab_principal)
            tab_principal.add(tab_inventarios, text="Inventarios")
            modulo_inventarios(tab_inventarios)

        elif rol == "produccion":
            tab_produccion = ttk.Frame(tab_principal)
            tab_principal.add(tab_produccion, text="Producción")
            modulo_produccion(tab_produccion)

        elif rol == "ventas":
            tab_ventas = ttk.Frame(tab_principal)
            tab_principal.add(tab_ventas, text="Ventas")
            modulo_ventas(tab_ventas)

        elif rol == "rrhh":
            tab_rrhh = ttk.Frame(tab_principal)
            tab_principal.add(tab_rrhh, text="Recursos Humanos")
            modulo_rrhh(tab_rrhh)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el módulo: {e}")

    # Al cerrar la ventana principal, volver al login
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana, login_window))
    ventana.mainloop()

def cerrar_ventana(ventana, login_window):
    ventana.destroy()
    login_window.deiconify()  # Mostrar el login nuevamente

# Ventana de login
def ventana_login():
    # Crear ventana de inicio de sesión
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("800x500")
    style = Style(theme="flatly")

    # Título
    title_label = ttk.Label(
        login_window,
        text="Bienvenido al Sistema",
        font=("Arial", 18, "bold"),
        bootstyle="primary",
    )
    title_label.pack(pady=20)

    # Imagen
    try:
        img = Image.open("logo.png")
        img = img.resize((425, 70))  # Ajusta el tamaño si es necesario
        img = ImageTk.PhotoImage(img)
        img_label = ttk.Label(login_window, image=img)
        img_label.image = img  # Evitar que la imagen sea recolectada por el GC
        img_label.pack(pady=10)
    except FileNotFoundError:
        img_label = ttk.Label(login_window, text="Logo no disponible", font=("Arial", 12))
        img_label.pack(pady=10)

    # Campo de usuario
    usuario_label = ttk.Label(login_window, text="Usuario:", bootstyle="info")
    usuario_label.pack(pady=5)
    usuario_entry = ttk.Entry(login_window, width=30)
    usuario_entry.pack(pady=5)

    # Campo de contraseña
    password_label = ttk.Label(login_window, text="Contraseña:", bootstyle="info")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    # Botón de login
    login_btn = ttk.Button(
        login_window,
        text="Ingresar",
        bootstyle="success",
        width=20,
        command=lambda: autenticar(usuario_entry, password_entry, login_window),
    )
    login_btn.pack(pady=20)

    # Pie de página
    footer_label = ttk.Label(
        login_window,
        text="Sistema de Gestión v1.0",
        font=("Arial", 10),
        bootstyle="secondary",
    )
    footer_label.pack(side="bottom", pady=10)

    login_window.mainloop()

# Ejecutar el login
ventana_login()

