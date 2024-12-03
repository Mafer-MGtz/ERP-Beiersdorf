import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def setup_inventarios_db():
    """Configura la base de datos para el módulo de inventarios."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def agregar_producto(nombre, cantidad):
    """Agrega un producto a la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad) VALUES (?, ?)", (nombre, cantidad))
    conn.commit()
    conn.close()

def obtener_productos():
    """Obtiene todos los productos desde la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, cantidad FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def mostrar_productos(lista):
    """Actualiza la lista de productos en la interfaz."""
    lista.delete(*lista.get_children())  # Limpiar la lista
    productos = obtener_productos()
    for producto in productos:
        lista.insert("", "end", values=(producto[1], producto[2]))

def abrir_agregar_producto(lista):
    """Ventana emergente para agregar un nuevo producto."""
    ventana = tk.Toplevel()
    ventana.title("Agregar Producto")
    ventana.geometry("550x250")
    ventana.resizable(False, False)
    ventana.configure(bg="#FFFEFF")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Nombre del producto:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    nombre_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    nombre_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="Cantidad:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    cantidad_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    cantidad_entry.grid(row=1, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="").grid(row=2, column=0, columnspan=2)

    def guardar_producto():
        nombre = nombre_entry.get()
        cantidad = cantidad_entry.get()

        if not nombre or not cantidad.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese un nombre y una cantidad válida.")
            return

        agregar_producto(nombre, int(cantidad))
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        mostrar_productos(lista)
        ventana.destroy()

    guardar_btn = ttk.Button(main_frame, text="Guardar", style="Accent.TButton", command=guardar_producto)
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)
    guardar_btn.grid_configure(sticky="ew", ipadx=10)

def eliminar_producto(lista):
    """Elimina un producto seleccionado de la base de datos."""
    seleccionado = lista.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar.")
        return

    producto_id = lista.item(seleccionado[0])['values'][0]
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre = ?", (producto_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
    mostrar_productos(lista)

def buscar_productos(lista, busqueda):
    """Busca productos por nombre."""
    productos = obtener_productos()
    productos_filtrados = [p for p in productos if busqueda.lower() in p[1].lower()]
    mostrar_productos(lista, productos_filtrados)

def modulo_inventarios(tab_inventarios):
    """Diseño y funcionalidad del módulo de inventarios."""
    setup_inventarios_db()

    header = ttk.Frame(tab_inventarios, style="Header.TFrame", padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Módulo de Inventarios", style="Header.TLabel").pack(anchor="center")

    main_frame = ttk.Frame(tab_inventarios, padding=20)
    main_frame.pack(fill="both", expand=True)

    buscar_frame = ttk.Frame(main_frame)
    buscar_frame.pack(pady=10, padx=20, fill='x')
    buscar_entry = ttk.Entry(buscar_frame, font=("Arial", 12), width=30)
    buscar_entry.pack(side=tk.LEFT, padx=5)
    buscar_btn = ttk.Button(buscar_frame, text="Buscar", style="Accent.TButton",
                           command=lambda: buscar_productos(productos_lista, buscar_entry.get()))
    buscar_btn.pack(side=tk.LEFT)

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    agregar_producto_btn = ttk.Button(buttons_frame, text="Agregar Producto", style="Accent.TButton",
                                      command=lambda: abrir_agregar_producto(productos_lista))
    agregar_producto_btn.pack(side="left", padx=10)

    eliminar_producto_btn = ttk.Button(buttons_frame, text="Eliminar Producto", style="Accent.TButton",
                                       command=lambda: eliminar_producto(productos_lista))
    eliminar_producto_btn.pack(side="left", padx=10)

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    productos_lista = ttk.Treeview(tree_frame, columns=("Nombre", "Cantidad"), show="headings", height=10)
    productos_lista.heading("Nombre", text="Nombre")
    productos_lista.heading("Cantidad", text="Cantidad")
    productos_lista.column("Nombre", anchor="w", width=200)
    productos_lista.column("Cantidad", anchor="center", width=100)
    productos_lista.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=productos_lista.yview)
    scrollbar.pack(side="right", fill="y")
    productos_lista.config(yscrollcommand=scrollbar.set)

    mostrar_productos(productos_lista)

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
    root.title("ERP - Módulo de Inventarios")
    root.geometry("600x500")
    configurar_estilos()

    tab_control = ttk.Notebook(root)
    tab_inventarios = ttk.Frame(tab_control)
    tab_control.add(tab_inventarios, text="Inventarios")
    tab_control.pack(expand=True, fill="both")

    modulo_inventarios(tab_inventarios)

    root.mainloop()



