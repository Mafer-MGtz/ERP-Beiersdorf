import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def setup_database():
    """Configura la base de datos para el módulo de recursos humanos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        puesto TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def agregar_empleado(nombre, puesto):
    """Agrega un nuevo empleado a la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO empleados (nombre, puesto) VALUES (?, ?)", (nombre, puesto))
    conn.commit()
    conn.close()

def obtener_empleados():
    """Obtiene todos los empleados desde la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, puesto FROM empleados")
    empleados = cursor.fetchall()
    conn.close()
    return empleados

def mostrar_empleados(lista):
    """Actualiza la lista de empleados en la interfaz."""
    lista.delete(*lista.get_children())  # Limpiar la lista
    empleados = obtener_empleados()
    for empleado in empleados:
        lista.insert("", "end", values=(empleado[1], empleado[2]))

def abrir_agregar_empleado(lista):
    """Ventana emergente para agregar un nuevo empleado."""
    ventana = tk.Toplevel()
    ventana.title("Agregar Empleado")
    ventana.geometry("550x250")
    ventana.resizable(False, False)
    ventana.configure(bg="#FFFEFF")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Nombre del empleado:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    nombre_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    nombre_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="Puesto:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    puesto_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    puesto_entry.grid(row=1, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="").grid(row=2, column=0, columnspan=2)

    def guardar_empleado():
        nombre = nombre_entry.get()
        puesto = puesto_entry.get()

        if not nombre or not puesto:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos")
            return

        agregar_empleado(nombre, puesto)
        messagebox.showinfo("Éxito", "Empleado agregado correctamente")
        mostrar_empleados(lista)
        ventana.destroy()

    guardar_btn = ttk.Button(main_frame, text="Guardar", style="Accent.TButton", command=guardar_empleado)
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)
    guardar_btn.grid_configure(sticky="ew", ipadx=10)

def abrir_editar_empleado(lista):
    """Ventana emergente para editar un empleado seleccionado."""
    seleccionado = lista.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione un empleado para editar")
        return

    empleado_nombre = lista.item(seleccionado[0])['values'][0]
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, puesto FROM empleados WHERE nombre = ?", (empleado_nombre,))
    empleado = cursor.fetchone()
    conn.close()

    ventana = tk.Toplevel()
    ventana.title("Editar Empleado")
    ventana.geometry("450x250")
    ventana.resizable(False, False)
    ventana.configure(bg="#FFFEFF")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Nombre del empleado:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    nombre_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    nombre_entry.insert(tk.END, empleado[1])
    nombre_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="Puesto:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    puesto_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    puesto_entry.insert(tk.END, empleado[2])
    puesto_entry.grid(row=1, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="").grid(row=2, column=0, columnspan=2)

    def guardar_editar_empleado():
        nombre = nombre_entry.get()
        puesto = puesto_entry.get()

        if not nombre or not puesto:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos")
            return

        conn = sqlite3.connect("erp.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE empleados SET nombre = ?, puesto = ? WHERE id = ?", (nombre, puesto, empleado[0]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
        mostrar_empleados(lista)
        ventana.destroy()

    guardar_btn = ttk.Button(main_frame, text="Guardar", style="Accent.TButton", command=guardar_editar_empleado)
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)
    guardar_btn.grid_configure(sticky="ew", ipadx=10)

def eliminar_empleado(lista):
    """Elimina un empleado seleccionado de la base de datos."""
    seleccionado = lista.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione un empleado para eliminar")
        return

    empleado_nombre = lista.item(seleccionado[0])['values'][0]
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE nombre = ?", (empleado_nombre,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
    mostrar_empleados(lista)

def modulo_rrhh(tab_rrhh):
    """Diseño y funcionalidad del módulo de recursos humanos."""
    setup_database()

    header = ttk.Frame(tab_rrhh, style="Header.TFrame", padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Módulo de Recursos Humanos", style="Header.TLabel").pack(anchor="center")

    main_frame = ttk.Frame(tab_rrhh, padding=20)
    main_frame.pack(fill="both", expand=True)

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    agregar_empleado_btn = ttk.Button(buttons_frame, text="Agregar Empleado", style="Accent.TButton",
                                      command=lambda: abrir_agregar_empleado(empleados_lista))
    agregar_empleado_btn.pack(side="left", padx=10)

    editar_empleado_btn = ttk.Button(buttons_frame, text="Editar Empleado", style="Accent.TButton",
                                     command=lambda: abrir_editar_empleado(empleados_lista))
    editar_empleado_btn.pack(side="left", padx=10)

    eliminar_empleado_btn = ttk.Button(buttons_frame, text="Eliminar Empleado", style="Accent.TButton",
                                       command=lambda: eliminar_empleado(empleados_lista))
    eliminar_empleado_btn.pack(side="left", padx=10)

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    empleados_lista = ttk.Treeview(tree_frame, columns=("Nombre", "Puesto"), show="headings", height=10)
    empleados_lista.heading("Nombre", text="Nombre")
    empleados_lista.heading("Puesto", text="Puesto")
    empleados_lista.column("Nombre", anchor="w", width=200)
    empleados_lista.column("Puesto", anchor="center", width=100)
    empleados_lista.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=empleados_lista.yview)
    scrollbar.pack(side="right", fill="y")
    empleados_lista.config(yscrollcommand=scrollbar.set)

    mostrar_empleados(empleados_lista)

def configurar_estilos():
    estilo = ttk.Style()
    estilo.theme_use("clam")
    
    # Estilo de botones
    estilo.configure("Accent.TButton", background="#4CAF50", foreground="white", font=("Arial", 11, "bold"), padding=8)
    estilo.map("Accent.TButton", background=[("active", "#45a049")])

    # Estilo de encabezado
    estilo.configure("Header.TFrame", background="#2196F3")
    estilo.configure("Treeview", font=("Arial", 11), rowheight=25)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ERP - Recursos Humanos")
    root.geometry("800x600")
    configurar_estilos()

    tab_control = ttk.Notebook(root)
    tab_rrhh = ttk.Frame(tab_control)
    tab_control.add(tab_rrhh, text="Recursos Humanos")
    tab_control.pack(expand=1, fill="both")

    modulo_rrhh(tab_rrhh)
    root.mainloop()

