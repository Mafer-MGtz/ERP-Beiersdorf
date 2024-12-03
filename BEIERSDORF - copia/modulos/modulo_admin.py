import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Configuración de la base de datos
def crear_base_de_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        usuario TEXT PRIMARY KEY,
                        nombre TEXT,
                        rol TEXT)''')
    conn.commit()
    conn.close()

# Función para obtener todos los usuarios de la base de datos
def obtener_usuarios():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario_db(usuario, nombre, rol):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, nombre, rol) VALUES (?, ?, ?)", (usuario, nombre, rol))
        conn.commit()
        messagebox.showinfo("Éxito", f"Usuario {usuario} agregado exitosamente")
    except sqlite3.IntegrityError:
        messagebox.showwarning("Error", f"El usuario {usuario} ya existe.")
    conn.close()

class AdminWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Módulo de Administración")
        self.master.geometry("600x500")
        self.master.resizable(False, False)

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para botones
        estilo.configure("Accent.TButton", background="#22a2e3", foreground="white", font=("Arial", 12, "bold"), padding=10)
        estilo.map("Accent.TButton", background=[("active", "#206e95")])

        # Estilo para etiquetas de encabezado
        estilo.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground="#333", background="#f5f5f5")

    def crear_widgets(self):
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill="both", expand=True)

        self.label = ttk.Label(main_frame, text="Bienvenido al Módulo de Administración", style="Header.TLabel")
        self.label.pack(pady=20)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        self.lista_btn = ttk.Button(buttons_frame, text="Ver Usuarios", style="Accent.TButton", command=self.mostrar_usuarios)
        self.lista_btn.pack(side="left", padx=20)

        self.agregar_btn = ttk.Button(buttons_frame, text="Agregar Usuario", style="Accent.TButton", command=self.agregar_usuario)
        self.agregar_btn.pack(side="left", padx=20)

    def mostrar_usuarios(self):
        lista_ventana = tk.Toplevel(self.master)
        lista_ventana.title("Lista de Usuarios")
        lista_ventana.geometry("600x300")
        lista_ventana.resizable(False, False)

        main_frame = ttk.Frame(lista_ventana, padding=20)
        main_frame.pack(fill="both", expand=True)

        usuarios = obtener_usuarios()

        if usuarios:
            usuarios_lista = "\n".join([f"Usuario: {user} - Nombre: {nombre} - Rol: {rol}"
                                        for user, nombre, rol in usuarios])
        else:
            usuarios_lista = "No hay usuarios registrados."

        usuarios_label = ttk.Label(main_frame, text=usuarios_lista, font=("Arial", 14), anchor="w")
        usuarios_label.pack(pady=20, fill="x")

        cerrar_btn = ttk.Button(main_frame, text="Cerrar", style="Accent.TButton", command=lista_ventana.destroy)
        cerrar_btn.pack(pady=10)

    def agregar_usuario(self):
        agregar_ventana = tk.Toplevel(self.master)
        agregar_ventana.title("Agregar Usuario")
        agregar_ventana.geometry("350x400")
        agregar_ventana.resizable(False, False)

        main_frame = ttk.Frame(agregar_ventana, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Nombre de Usuario:", font=("Arial", 12)).pack(pady=10, anchor="w")
        self.usuario_entry = ttk.Entry(main_frame, width=30)
        self.usuario_entry.pack(pady=5)

        ttk.Label(main_frame, text="Nombre Completo del Usuario:", font=("Arial", 12)).pack(pady=10, anchor="w")
        self.nombre_entry = ttk.Entry(main_frame, width=30)
        self.nombre_entry.pack(pady=5)

        ttk.Label(main_frame, text="Rol (admin/usuario):", font=("Arial", 12)).pack(pady=10, anchor="w")
        self.rol_entry = ttk.Entry(main_frame, width=30)
        self.rol_entry.pack(pady=5)

        agregar_btn = ttk.Button(main_frame, text="Agregar Usuario", style="Accent.TButton", command=self.guardar_usuario)
        agregar_btn.pack(pady=20)

    def guardar_usuario(self):
        usuario = self.usuario_entry.get()
        nombre = self.nombre_entry.get()
        rol = self.rol_entry.get()

        if usuario and nombre and rol:
            agregar_usuario_db(usuario, nombre, rol)
            self.usuario_entry.delete(0, tk.END)
            self.nombre_entry.delete(0, tk.END)
            self.rol_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")

if __name__ == "__main__":
    crear_base_de_datos()
    root = tk.Tk()
    app = AdminWindow(root)
    root.mainloop()

