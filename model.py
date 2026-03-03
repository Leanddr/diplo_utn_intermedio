from datetime import datetime
from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    CharField,
    TextField,
    FloatField,
)


#-----------------------------------------------------------
# Modelo - Versión con Peewee ORM
#------------------------------------------------------------
# Peewee es un ORM (Object-Relational Mapping) que permite
# trabajar con la base de datos usando CLASES de Python
# en lugar de escribir SQL directamente.
#
# VENTAJAS DE USAR PEEWEE:
# 1. Más "Pythónico" y orientado a objetos
# 2. No escribimos SQL manualmente (menos errores)
# 3. Los datos se manejan como objetos Python
# 4. Validaciones automáticas de tipos de datos
#
# CONCEPTOS CLAVE:
# - Model: clase que representa una TABLA
# - Field: representa una COLUMNA
# - La instancia de un Model es una FILA
#------------------------------------------------------------


# ============================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================
# Creamos la conexión a SQLite usando Peewee.
# Es la misma base de datos que veníamos usando.
# ============================================================

# Nombre del archivo de base de datos (mismo que antes)
DATABASE_NAME = "appestacionamiento.db"

# Creamos la conexión a la base de datos SQLite
# pragmas son configuraciones de SQLite para mejor rendimiento
db = SqliteDatabase(
    DATABASE_NAME,
    pragmas={
        'journal_mode': 'wal',      # Mejor rendimiento en escrituras
        'foreign_keys': 1,          # Activar claves foráneas
    }
)


# ============================================================
# CLASE BASE PARA TODOS LOS MODELOS
# ============================================================
# Esta clase define la conexión a usar en todos los modelos.
# Todos nuestros modelos heredarán de esta clase.
# ============================================================

class BaseModel(Model):
    """
    Clase base que define la conexión a la base de datos.
    Todos los modelos de la aplicación heredan de esta clase.
    """
    
    class Meta:
        # Le decimos a Peewee qué base de datos usar
        database = db


# ============================================================
# MODELO: EstacionamientoModel
# ============================================================
# Esta clase representa la TABLA 'estacionamientos'.
# Cada atributo de la clase es una COLUMNA de la tabla.
#
# Tipos de campos (Fields) que usamos:
# - AutoField: entero autoincremental (para el ID)
# - CharField: texto con longitud máxima
# - TextField: texto sin límite
# - FloatField: número decimal
#
# Parámetros comunes:
# - null=True: permite valores NULL
# - null=False: campo obligatorio (NOT NULL)
# ============================================================

class EstacionamientoModel(BaseModel):
    """
    Modelo que representa un registro de estacionamiento.
    
    Cada instancia de esta clase es una FILA en la tabla 'estacionamientos'.
    Peewee se encarga de crear la tabla y manejar el SQL automáticamente.
    
    Ejemplo de uso::
    
        # Crear nuevo registro
        nuevo = EstacionamientoModel.create(
            patente="ABC123",
            vehiculo="Auto",
            ...
        )
        
        # Buscar registros
        activos = EstacionamientoModel.select().where(
            EstacionamientoModel.estado == "En curso"
        )
    """
    
    # ---------------------------------------------------------
    # DEFINICIÓN DE COLUMNAS (Fields)
    # ---------------------------------------------------------
    
    # ID autoincremental (clave primaria)
    id = AutoField(primary_key=True)
    
    # Datos del vehículo
    patente = CharField(max_length=20, null=False)
    vehiculo = CharField(max_length=50, null=False)
    
    # Datos del contacto
    nombre = CharField(max_length=100, null=False)
    apellido = CharField(max_length=100, null=False)
    dni = CharField(max_length=20, null=False)
    email = CharField(max_length=100, null=False)
    
    # Datos del estacionamiento
    fecha = CharField(max_length=20, null=False)
    hora_ingreso = CharField(max_length=10, null=False)
    hora_egreso = CharField(max_length=10, null=True)  # Puede ser NULL al inicio
    valor_hora = FloatField(null=False)
    total = FloatField(null=True)  # Se calcula al salir
    estado = CharField(max_length=20, null=False)
    
    class Meta:
        # Nombre de la tabla en la base de datos
        table_name = 'estacionamientos'


# ============================================================
# CLASE: Estacionamiento (Servicio/Repositorio)
# ============================================================
# Esta clase contiene los MÉTODOS para operar sobre el modelo.
# Es la misma interfaz que teníamos antes, pero ahora usa Peewee.
#
# El controlador sigue llamando a los mismos métodos:
# - registrar_ingreso()
# - obtener_estacionados()
# - etc.
#
# La diferencia es que internamente usamos Peewee en lugar de SQL.
# ============================================================

class Estacionamiento:
    """
    Clase de servicio para operaciones CRUD sobre estacionamientos.
    
    Usa el modelo EstacionamientoModel (Peewee) internamente.
    Mantiene la misma interfaz que la versión anterior para
    compatibilidad con el controlador.
    """
    
    # ---------------------------------------------------------
    # CREATE - Alta de nuevo estacionamiento
    # ---------------------------------------------------------
    
    def registrar_ingreso(self, patente, vehiculo, nombre, apellido, 
                          dni, email, valor_hora):
        """
        Registra un nuevo vehículo en el estacionamiento.
        
        Parámetros:
            patente: patente del vehículo
            vehiculo: tipo de vehículo (auto, moto, etc.)
            nombre: nombre del contacto
            apellido: apellido del contacto
            dni: DNI del contacto
            email: email del contacto
            valor_hora: precio por hora
        
        Retorna:
            True si se registró correctamente, False si hubo error
        """
        # Fecha y hora actual
        fecha = datetime.now().strftime("%d/%m/%y")
        hora_ingreso = datetime.now().strftime("%H:%M")
        estado = "En curso"
        
        try:
            # Con Peewee usamos .create() en lugar de INSERT SQL
            EstacionamientoModel.create(
                patente=patente,
                vehiculo=vehiculo,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                email=email,
                fecha=fecha,
                hora_ingreso=hora_ingreso,
                valor_hora=valor_hora,
                estado=estado
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo registrar el ingreso: {e}")
            return False
    
    # ---------------------------------------------------------
    # READ - Consultar estacionamientos en curso
    # ---------------------------------------------------------
    
    def obtener_estacionados(self):
        """
        Obtiene todos los vehículos actualmente estacionados.
        
        Retorna:
            Lista de tuplas con los registros (para compatibilidad con Treeview)
        """
        try:
            # Con Peewee usamos .select().where() en lugar de SELECT SQL
            query = EstacionamientoModel.select().where(
                EstacionamientoModel.estado == "En curso"
            )
            
            # Convertimos a lista de tuplas para el Treeview
            resultados = []
            for registro in query:
                resultados.append(self._modelo_a_tupla(registro))
            
            return resultados
        except Exception as e:
            print(f"[ERROR] No se pudieron obtener los estacionados: {e}")
            return []
    
    # ---------------------------------------------------------
    # READ - Consultar historial de finalizados
    # ---------------------------------------------------------
    
    def obtener_historial(self):
        """
        Obtiene todos los estacionamientos finalizados.
        
        Retorna:
            Lista de tuplas con los registros finalizados
        """
        try:
            query = EstacionamientoModel.select().where(
                EstacionamientoModel.estado == "Finalizado"
            ).order_by(EstacionamientoModel.hora_ingreso.desc())
            
            resultados = []
            for registro in query:
                resultados.append(self._modelo_a_tupla(registro))
            
            return resultados
        except Exception as e:
            print(f"[ERROR] No se pudo obtener el historial: {e}")
            return []
    
    # ---------------------------------------------------------
    # READ - Obtener datos para calcular salida
    # ---------------------------------------------------------
    
    def obtener_datos_para_salida(self, id_registro):
        """
        Obtiene hora_ingreso y valor_hora de un registro.
        
        Parámetros:
            id_registro: ID del estacionamiento
        
        Retorna:
            Tupla (hora_ingreso, valor_hora) o None si no existe
        """
        try:
            # Con Peewee usamos .get_or_none() para buscar por ID
            registro = EstacionamientoModel.get_or_none(
                (EstacionamientoModel.id == id_registro) &
                (EstacionamientoModel.estado == "En curso")
            )
            
            if registro:
                return (registro.hora_ingreso, registro.valor_hora)
            return None
        except Exception as e:
            print(f"[ERROR] No se pudieron obtener datos para salida: {e}")
            return None
    
    # ---------------------------------------------------------
    # UPDATE - Registrar salida de vehículo
    # ---------------------------------------------------------
    
    def registrar_salida(self, id_registro, total):
        """
        Registra la salida de un vehículo.
        
        Parámetros:
            id_registro: ID del estacionamiento
            total: monto total a cobrar
        
        Retorna:
            True si se registró correctamente, False si hubo error
        """
        hora_egreso = datetime.now().strftime("%H:%M")
        
        try:
            # Con Peewee usamos .update().where() en lugar de UPDATE SQL
            filas_actualizadas = EstacionamientoModel.update(
                hora_egreso=hora_egreso,
                total=total,
                estado="Finalizado"
            ).where(
                EstacionamientoModel.id == id_registro
            ).execute()
            
            return filas_actualizadas > 0
        except Exception as e:
            print(f"[ERROR] No se pudo registrar la salida: {e}")
            return False
    
    # ---------------------------------------------------------
    # UPDATE - Editar registro existente
    # ---------------------------------------------------------
    
    def editar_registro(self, id_registro, patente, vehiculo, nombre, 
                        apellido, dni, email, valor_hora):
        """
        Edita los datos de un estacionamiento en curso.
        
        Retorna:
            True si se editó correctamente, False si hubo error
        """
        try:
            filas_actualizadas = EstacionamientoModel.update(
                patente=patente,
                vehiculo=vehiculo,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                email=email,
                valor_hora=valor_hora
            ).where(
                EstacionamientoModel.id == id_registro
            ).execute()
            
            return filas_actualizadas > 0
        except Exception as e:
            print(f"[ERROR] No se pudo editar el registro: {e}")
            return False
    
    # ---------------------------------------------------------
    # DELETE - Eliminar registro
    # ---------------------------------------------------------
    
    def eliminar_registro(self, id_registro):
        """
        Elimina un registro de la base de datos.
        
        Parámetros:
            id_registro: ID del estacionamiento a eliminar
        
        Retorna:
            True si se eliminó correctamente, False si hubo error
        """
        try:
            # Con Peewee usamos .delete().where() en lugar de DELETE SQL
            filas_eliminadas = EstacionamientoModel.delete().where(
                EstacionamientoModel.id == id_registro
            ).execute()
            
            return filas_eliminadas > 0
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el registro: {e}")
            return False
    
    # ---------------------------------------------------------
    # MÉTODO AUXILIAR - Convertir modelo a tupla
    # ---------------------------------------------------------
    
    def _modelo_a_tupla(self, registro):
        """
        Convierte un objeto EstacionamientoModel a tupla.
        
        Esto es necesario porque el Treeview de Tkinter
        espera los datos como tuplas, no como objetos.
        
        Parámetros:
            registro: instancia de EstacionamientoModel
        
        Retorna:
            Tupla con todos los campos en orden
        """
        return (
            registro.id,
            registro.patente,
            registro.vehiculo,
            registro.nombre,
            registro.apellido,
            registro.dni,
            registro.email,
            registro.fecha,
            registro.hora_ingreso,
            registro.hora_egreso or "",  # Si es None, usar string vacío
            registro.valor_hora,
            registro.total or "",
            registro.estado
        )


# ============================================================
# CLASE: BaseDeDatos (para compatibilidad con main.py)
# ============================================================
# Mantenemos esta clase para que main.py siga funcionando.
# Con Peewee la conexión se maneja diferente, pero la interfaz
# es la misma.
# ============================================================

class BaseDeDatos:
    """
    Clase para inicializar la base de datos.
    
    Con Peewee, la conexión se maneja automáticamente.
    Esta clase solo se usa para crear las tablas al inicio.
    """
    
    def __enter__(self):
        """Se conecta a la base de datos."""
        db.connect(reuse_if_open=True)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión si está abierta."""
        if not db.is_closed():
            db.close()
    
    def crear_tabla(self):
        """
        Crea la tabla 'estacionamientos' si no existe.
        
        Con Peewee usamos create_tables() que lee la definición
        de los campos directamente de la clase EstacionamientoModel.
        """
        try:
            # safe=True significa "CREATE TABLE IF NOT EXISTS"
            db.create_tables([EstacionamientoModel], safe=True)
            print("[INFO] Tabla 'estacionamientos' verificada/creada")
        except Exception as e:
            print(f"[ERROR] No se pudo crear la tabla: {e}")
            raise


# ============================================================
# FUNCIONES DE COMPATIBILIDAD (para código anterior)
# ============================================================
# Estas funciones mantienen la interfaz anterior por si
# algún código todavía las usa.
# ============================================================

def crear_base():
    """FUNCIÓN DE COMPATIBILIDAD - Usar BaseDeDatos() en su lugar"""
    db.connect(reuse_if_open=True)
    return db

def crear_tabla(con):
    """FUNCIÓN DE COMPATIBILIDAD - Usar BaseDeDatos().crear_tabla() en su lugar"""
    with BaseDeDatos() as base:
        base.crear_tabla()