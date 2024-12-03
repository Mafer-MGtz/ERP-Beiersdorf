import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def setup_produccion_db():
    """Configura la base de datos para el módulo de producción."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordenes_trabajo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def agregar_orden_trabajo(descripcion, cantidad):
    """Agrega una orden de trabajo a la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ordenes_trabajo (descripcion, cantidad) VALUES (?, ?)", (descripcion, cantidad))
    conn.commit()
    conn.close()

def obtener_ordenes_trabajo():
    """Obtiene todas las órdenes de trabajo desde la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, descripcion, cantidad FROM ordenes_trabajo")
    ordenes = cursor.fetchall()
    conn.close()
    return ordenes

def mostrar_ordenes_trabajo(lista):
    """Actualiza la lista de órdenes de trabajo en la interfaz."""
    lista.delete(*lista.get_children())  # Limpiar la lista
    ordenes = obtener_ordenes_trabajo()
    for orden in ordenes:
        lista.insert("", "end", values=(orden[1], orden[2]))

def abrir_agregar_orden(lista):
    """Ventana emergente para agregar una nueva orden de trabajo."""
    ventana = tk.Toplevel()
    ventana.title("Agregar Orden de Trabajo")
    ventana.geometry("550x250")
    ventana.resizable(False, False)
    ventana.configure(bg="#FFFEFF")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Descripción de la orden:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    descripcion_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    descripcion_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="Cantidad de unidades:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    cantidad_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    cantidad_entry.grid(row=1, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="").grid(row=2, column=0, columnspan=2)

    def guardar_orden():
        descripcion = descripcion_entry.get()
        cantidad = cantidad_entry.get()

        if not descripcion or not cantidad.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese una descripción y una cantidad válida.")
            return

        agregar_orden_trabajo(descripcion, int(cantidad))
        messagebox.showinfo("Éxito", "Orden de trabajo agregada correctamente")
        mostrar_ordenes_trabajo(lista)
        ventana.destroy()

    guardar_btn = ttk.Button(main_frame, text="Guardar", style="Accent.TButton", command=guardar_orden)
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)
    guardar_btn.grid_configure(sticky="ew", ipadx=10)

def eliminar_orden_trabajo(lista):
    """Elimina una orden de trabajo seleccionada de la base de datos."""
    seleccionado = lista.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione una orden para eliminar.")
        return

    orden_id = lista.item(seleccionado[0])['values'][0]
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ordenes_trabajo WHERE descripcion = ?", (orden_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Orden de trabajo eliminada correctamente")
    mostrar_ordenes_trabajo(lista)

def buscar_ordenes_trabajo(lista, busqueda):
    """Busca órdenes de trabajo por descripción."""
    ordenes = obtener_ordenes_trabajo()
    ordenes_filtradas = [o for o in ordenes if busqueda.lower() in o[1].lower()]
    mostrar_ordenes_trabajo(lista, ordenes_filtradas)

def modulo_produccion(tab_produccion):
    """Diseño y funcionalidad del módulo de producción."""
    setup_produccion_db()

    header = ttk.Frame(tab_produccion, style="Header.TFrame", padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Módulo de Producción", style="Header.TLabel").pack(anchor="center")

    main_frame = ttk.Frame(tab_produccion, padding=20)
    main_frame.pack(fill="both", expand=True)

    buscar_frame = ttk.Frame(main_frame)
    buscar_frame.pack(pady=10, padx=20, fill='x')
    buscar_entry = ttk.Entry(buscar_frame, font=("Arial", 12), width=30)
    buscar_entry.pack(side=tk.LEFT, padx=5)
    buscar_btn = ttk.Button(buscar_frame, text="Buscar", style="Accent.TButton",
                           command=lambda: buscar_ordenes_trabajo(ordenes_lista, buscar_entry.get()))
    buscar_btn.pack(side=tk.LEFT)

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    agregar_orden_btn = ttk.Button(buttons_frame, text="Agregar Orden de Trabajo", style="Accent.TButton",
                                   command=lambda: abrir_agregar_orden(ordenes_lista))
    agregar_orden_btn.pack(side="left", padx=10)

    eliminar_orden_btn = ttk.Button(buttons_frame, text="Eliminar Orden de Trabajo", style="Accent.TButton",
                                    command=lambda: eliminar_orden_trabajo(ordenes_lista))
    eliminar_orden_btn.pack(side="left", padx=10)

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    ordenes_lista = ttk.Treeview(tree_frame, columns=("Descripción", "Cantidad"), show="headings", height=10)
    ordenes_lista.heading("Descripción", text="Descripción")
    ordenes_lista.heading("Cantidad", text="Cantidad")
    ordenes_lista.column("Descripción", anchor="w", width=200)
    ordenes_lista.column("Cantidad", anchor="center", width=100)
    ordenes_lista.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=ordenes_lista.yview)
    scrollbar.pack(side="right", fill="y")
    ordenes_lista.config(yscrollcommand=scrollbar.set)

    mostrar_ordenes_trabajo(ordenes_lista)

def configurar_estilos():
    estilo = ttk.Style()
    estilo.theme_use("clam")
    
    # Estilo de botones
    estilo.configure("Accent.TButton", background="#4CAF50", foreground="white", font=("Arial", 11, "bold"), padding=8)
    estilo.map("Accent.TButton", background=[("active", "#45a049")])

    # Estilo de encabezado
    estilo.configure("Header.TFrame", background="#2196F3")
    estilo.configure("Header.TLabel", background="#2196F3", foreground="white", font=("Arial", 16, "bold"))

    # Estilo general
    estilo.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    estilo.configure("Treeview", font=("Arial", 11), rowheight=25)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ERP - Módulo de Producción")
    root.geometry("600x500")
    configurar_estilos()

    tab_control = ttk.Notebook(root)
    tab_produccion = ttk.Frame(tab_control)
    tab_control.add(tab_produccion, text="Producción")
    tab_control.pack(expand=True, fill="both")

    modulo_produccion(tab_produccion)

    root.mainloop()
