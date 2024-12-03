from ttkbootstrap import Style

def configurar_estilos():
    """
    Configura estilos personalizados para los widgets.
    """
    style = Style(theme="cosmo")  # Puedes usar otros temas como "darkly", "flatly", etc.

    # Define estilos personalizados
    style.configure("primary.TLabel", font=("Arial", 12), foreground="#1A73E8")
    style.configure("success.TButton", font=("Arial", 10), background="#28a745", foreground="white")

    # Retorna el objeto de estilo para su uso
    return style

