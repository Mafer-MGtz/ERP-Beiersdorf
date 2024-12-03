import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Configuración de la base de datos
def setup_ventas_db():
    """Configura la base de datos para el módulo de ventas."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def agregar_pedido(descripcion, cantidad):
    """Agrega un nuevo pedido a la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (descripcion, cantidad) VALUES (?, ?)", (descripcion, cantidad))
    conn.commit()
    conn.close()

def obtener_pedidos():
    """Obtiene todos los pedidos desde la base de datos."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, descripcion, cantidad FROM pedidos")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def mostrar_pedidos(lista):
    """Actualiza la lista de pedidos en la interfaz."""
    lista.delete(*lista.get_children())  # Limpiar la lista
    pedidos = obtener_pedidos()
    for pedido in pedidos:
        lista.insert("", "end", values=(pedido[1], pedido[2]))

def abrir_agregar_pedido(lista):
    """Ventana emergente para agregar un nuevo pedido."""
    ventana = tk.Toplevel()
    ventana.title("Agregar Pedido")
    ventana.geometry("550x250")
    ventana.resizable(False, False)
    ventana.configure(bg="#FFFEFF")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(fill="both", expand=True)

    ttk.Label(main_frame, text="Descripción del pedido:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    descripcion_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    descripcion_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="Cantidad de unidades:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    cantidad_entry = ttk.Entry(main_frame, font=("Arial", 12), width=30)
    cantidad_entry.grid(row=1, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="").grid(row=2, column=0, columnspan=2)

    def guardar_pedido():
        descripcion = descripcion_entry.get()
        cantidad = cantidad_entry.get()

        if not descripcion or not cantidad.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese una descripción y una cantidad válida.")
            return

        agregar_pedido(descripcion, int(cantidad))
        messagebox.showinfo("Éxito", "Pedido agregado correctamente")
        mostrar_pedidos(lista)
        ventana.destroy()

    guardar_btn = ttk.Button(main_frame, text="Guardar", style="Accent.TButton", command=guardar_pedido)
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)
    guardar_btn.grid_configure(sticky="ew", ipadx=10)

def eliminar_pedido(lista):
    """Elimina un pedido seleccionado de la base de datos."""
    seleccionado = lista.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione un pedido para eliminar.")
        return

    pedido_id = lista.item(seleccionado[0])['values'][0]
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE descripcion = ?", (pedido_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
    mostrar_pedidos(lista)

def buscar_pedidos(lista, busqueda):
    """Busca pedidos por descripción."""
    pedidos = obtener_pedidos()
    pedidos_filtrados = [p for p in pedidos if busqueda.lower() in p[1].lower()]
    mostrar_pedidos(lista, pedidos_filtrados)

def modulo_ventas(tab_ventas):
    """Diseño y funcionalidad del módulo de ventas."""
    setup_ventas_db()

    header = ttk.Frame(tab_ventas, style="Header.TFrame", padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Módulo de Ventas", style="Header.TLabel").pack(anchor="center")

    main_frame = ttk.Frame(tab_ventas, padding=20)
    main_frame.pack(fill="both", expand=True)

    buscar_frame = ttk.Frame(main_frame)
    buscar_frame.pack(pady=10, padx=20, fill='x')
    buscar_entry = ttk.Entry(buscar_frame, font=("Arial", 12), width=30)
    buscar_entry.pack(side=tk.LEFT, padx=5)
    buscar_btn = ttk.Button(buscar_frame, text="Buscar", style="Accent.TButton",
                           command=lambda: buscar_pedidos(pedidos_lista, buscar_entry.get()))
    buscar_btn.pack(side=tk.LEFT)

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    ver_ventas_btn = ttk.Button(buttons_frame, text="Ver Ventas", style="Accent.TButton",
                                command=lambda: mostrar_pedidos(pedidos_lista))
    ver_ventas_btn.pack(side="left", padx=10)

    agregar_pedido_btn = ttk.Button(buttons_frame, text="Agregar Pedido", style="Accent.TButton",
                                    command=lambda: abrir_agregar_pedido(pedidos_lista))
    agregar_pedido_btn.pack(side="left", padx=10)

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    pedidos_lista = ttk.Treeview(tree_frame, columns=("Descripción", "Cantidad"), show="headings", height=10)
    pedidos_lista.heading("Descripción", text="Descripción")
    pedidos_lista.heading("Cantidad", text="Cantidad")
    pedidos_lista.column("Descripción", anchor="w", width=200)
    pedidos_lista.column("Cantidad", anchor="center", width=100)
    pedidos_lista.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=pedidos_lista.yview)
    scrollbar.pack(side="right", fill="y")
    pedidos_lista.config(yscrollcommand=scrollbar.set)

    mostrar_pedidos(pedidos_lista)

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
    root.title("ERP - Módulo de Ventas")
    root.geometry("600x500")
    configurar_estilos()

    tab_control = ttk.Notebook(root)
    tab_ventas = ttk.Frame(tab_control)
    tab_control.add(tab_ventas, text="Ventas")
    tab_control.pack(expand=True, fill="both")

    modulo_ventas(tab_ventas)

    root.mainloop()

