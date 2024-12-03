import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Configuración de la base de datos
def setup_database():
    """Configura la base de datos si no existe."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        monto REAL
    )
    """)
    conn.commit()
    conn.close()

def mostrar_balance(tab_finanzas):
    """Muestra el balance total."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(monto) FROM transacciones")
    balance = cursor.fetchone()[0]
    balance = balance if balance else 0
    conn.close()
    messagebox.showinfo("Balance de Cuentas", f"El balance actual es: ${balance:.2f}")

def agregar_transaccion_gui(tab_finanzas):
    """Abre una ventana para agregar transacciones."""
    agregar_window = tk.Toplevel(tab_finanzas)
    agregar_window.title("Agregar Transacción")
    agregar_window.geometry("450x250")
    agregar_window.resizable(False, False)
    agregar_window.configure(bg="#f3f3f3")  # Fondo claro

    # Frame principal
    main_frame = ttk.Frame(agregar_window, padding=20)
    main_frame.pack(fill="both", expand=True)

    # Etiquetas y campos de entrada
    ttk.Label(main_frame, text="Descripción:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
    descripcion_entry = ttk.Entry(main_frame, width=30, font=("Arial", 12))
    descripcion_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(main_frame, text="Monto:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
    monto_entry = ttk.Entry(main_frame, width=30, font=("Arial", 12))
    monto_entry.grid(row=1, column=1, pady=10, padx=10)

    # Espaciador para separar el botón
    ttk.Label(main_frame, text="").grid(row=2, column=0, columnspan=2)

    def guardar_transaccion():
        """Guardar la transacción en la base de datos."""
        descripcion = descripcion_entry.get().strip()
        monto_text = monto_entry.get().strip()
        if not descripcion or not monto_text:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        try:
            monto = float(monto_text)
            conn = sqlite3.connect("erp.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transacciones (descripcion, monto) VALUES (?, ?)", (descripcion, monto))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Transacción agregada con éxito.")
            agregar_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")

    # Botón Guardar
    guardar_btn = ttk.Button(main_frame, text="Guardar", style="Accent.TButton", command=guardar_transaccion)
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)

    # Centrar el botón
    guardar_btn.grid_configure(sticky="ew", ipadx=10)

def cargar_transacciones(tab_finanzas, transacciones_lista):
    """Carga las transacciones en el Treeview."""
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion, monto FROM transacciones")
    transacciones = cursor.fetchall()
    conn.close()
    transacciones_lista.delete(*transacciones_lista.get_children())
    for transaccion in transacciones:
        transacciones_lista.insert("", "end", values=(transaccion[0], f"${transaccion[1]:.2f}"))

def modulo_finanzas(tab_finanzas):
    """Interfaz del módulo de Finanzas."""
    setup_database()

    # Encabezado
    header = ttk.Frame(tab_finanzas, style="Header.TFrame", padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Módulo de Finanzas", style="Header.TLabel").pack(anchor="center")

    main_frame = ttk.Frame(tab_finanzas, padding=20)
    main_frame.pack(fill="both", expand=True)

    # Botones principales
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(pady=10)

    balance_btn = ttk.Button(buttons_frame, text="Ver Balance", style="Accent.TButton", command=lambda: mostrar_balance(tab_finanzas))
    balance_btn.pack(side="left", padx=10)

    agregar_transaccion_btn = ttk.Button(buttons_frame, text="Agregar Transacción", style="Accent.TButton", command=lambda: agregar_transaccion_gui(tab_finanzas))
    agregar_transaccion_btn.pack(side="left", padx=10)

    # Tabla de transacciones
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, pady=10)

    transacciones_lista = ttk.Treeview(tree_frame, columns=("Descripción", "Monto"), show="headings", height=10)
    transacciones_lista.heading("Descripción", text="Descripción")
    transacciones_lista.heading("Monto", text="Monto")
    transacciones_lista.column("Descripción", anchor="w", width=200)
    transacciones_lista.column("Monto", anchor="center", width=100)
    transacciones_lista.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=transacciones_lista.yview)
    scrollbar.pack(side="right", fill="y")
    transacciones_lista.config(yscrollcommand=scrollbar.set)

    cargar_transacciones(tab_finanzas, transacciones_lista)

# Configurar estilos generales
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

# Ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema ERP - Finanzas")
    root.geometry("600x500")
    configurar_estilos()

    tab_control = ttk.Notebook(root)
    tab_finanzas = ttk.Frame(tab_control)
    tab_control.add(tab_finanzas, text="Finanzas")
    tab_control.pack(expand=True, fill="both")

    modulo_finanzas(tab_finanzas)

    root.mainloop()
