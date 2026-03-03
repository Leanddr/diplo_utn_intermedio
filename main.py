from model import BaseDeDatos
from view import iniciar_app


#-----------------------------------------------------------
# Punto de entrada de la aplicación
#------------------------------------------------------------
# Este archivo es el que se ejecuta para iniciar la app.
# 
# Pasos que realiza:
# 1. Inicializa la base de datos (crea la tabla si no existe)
# 2. Inicia la interfaz gráfica (Tkinter)
#
# USO:
#   python main.py
#------------------------------------------------------------


def inicializar_db():
    """
    Inicializa la base de datos.
    
    Usa la clase BaseDeDatos con el patrón 'with' (context manager)
    para asegurar que la conexión se cierre automáticamente.
    
    Si la tabla no existe, la crea. Si ya existe, no hace nada
    (gracias al IF NOT EXISTS en el SQL).
    """
    # Usamos 'with' para que la conexión se cierre automáticamente
    # al salir del bloque, incluso si hay error
    with BaseDeDatos() as db:
        db.crear_tabla()
    
    print("[INFO] Base de datos inicializada correctamente")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    # Primero: inicializar la base de datos
    inicializar_db()
    
    # Segundo: iniciar la interfaz gráfica
    iniciar_app()