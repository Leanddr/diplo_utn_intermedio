# App Estacionamiento - Nivel Intermedio UTN

Aplicación de gestión de estacionamiento desarrollada para la 
**Diplomatura UTN - Python Nivel Intermedio**.

## Requisitos Cumplidos

### Nivel Inicial (Base)
- [x] ABMC (CRUD) completo
- [x] Base de datos SQLite3
- [x] Validación con regex (email y patente)
- [x] Código según PEP8

### Nivel Intermedio (Agregados)
- [x] **Módulos separados** (model, view, controller, validaciones)
- [x] **Patrón MVC** implementado
- [x] **Paradigma POO** - Clases BaseDeDatos, Estacionamiento, EstacionamientoModel
- [x] **Manejo de excepciones** (try/except en operaciones de BD)
- [x] **Clases para conexión a BD** - Usando Peewee ORM
- [x] **ORM Peewee** - Mapeo objeto-relacional para SQLite
- [x] **Documentación con Sphinx** - Carpeta docs/ configurada

---

## Estructura del Proyecto

```
app_estacionameinto/
├── main.py           # Punto de entrada de la aplicación
├── model.py          # MODELO - Clases BaseDeDatos y Estacionamiento
├── view.py           # VISTA - Interfaz gráfica Tkinter
├── controller.py     # CONTROLADOR - Lógica de negocio
├── validaciones.py   # Funciones de validación (email, patente, cálculos)
├── README.md         # Este archivo
└── docs/             # Documentación Sphinx
    ├── conf.py       # Configuración de Sphinx
    ├── index.rst     # Página principal
    ├── modules.rst   # Documentación de módulos
    └── Makefile      # Para generar documentación
```

---

## Arquitectura MVC

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│      VISTA      │     │   CONTROLADOR    │     │     MODELO      │
│    (view.py)    │────▶│ (controller.py)  │────▶│   (model.py)    │
│    Tkinter      │◀────│                  │◀────│    SQLite       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                        │
         │              validaciones.py                   │
         │              (email, patente,                  │
         │               cálculos)                        │
         │                                                │
         └────────────────────────────────────────────────┘
```

---

## Clases Implementadas (POO)

### Peewee ORM

La aplicación usa **Peewee**, un ORM (Object-Relational Mapping) que permite trabajar con la base de datos usando clases de Python en lugar de SQL directo.

**¿Qué es un ORM?**
- Mapea clases Python → tablas de la BD
- Mapea atributos → columnas
- Mapea instancias → filas

**Ventajas:**
- Código más limpio y "Pythónico"
- No escribimos SQL manualmente
- Validaciones automáticas de tipos
- Menos errores

### Clase `EstacionamientoModel` (model.py)

Representa la **tabla** `estacionamientos` en la base de datos.
Cada atributo es una columna de la tabla.

```python
class EstacionamientoModel(BaseModel):
    id = AutoField(primary_key=True)
    patente = CharField(max_length=20, null=False)
    vehiculo = CharField(max_length=50, null=False)
    nombre = CharField(max_length=100, null=False)
    # ... más campos
    
    class Meta:
        table_name = 'estacionamientos'
```

**Uso:**
```python
# ANTES (SQL directo):
cursor.execute("INSERT INTO estacionamientos (patente, ...) VALUES (?, ?)", data)

# AHORA (Peewee):
EstacionamientoModel.create(patente="ABC123", vehiculo="Auto", ...)
```

### Clase `Estacionamiento` (model.py)

Clase de **servicio** que contiene los métodos CRUD.
Usa `EstacionamientoModel` internamente.

**Métodos:**
- `registrar_ingreso(patente, vehiculo, ...)` - Alta
- `obtener_estacionados()` - Consulta activos
- `obtener_historial()` - Consulta finalizados
- `registrar_salida(id, total)` - Actualiza a finalizado
- `editar_registro(id, ...)` - Modificación
- `eliminar_registro(id)` - Baja

### Clase `BaseDeDatos` (model.py)

Maneja la inicialización de la base de datos.
Crea las tablas usando Peewee.

```python
with BaseDeDatos() as db:
    db.crear_tabla()  # Crea la tabla si no existe
```

---

## Manejo de Excepciones

Todas las operaciones de base de datos están envueltas en `try/except`:

```python
def registrar_ingreso(self, patente, ...):
    try:
        with BaseDeDatos() as db:
            db.cursor.execute(sql, data)
            db.commit()
        return True
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo registrar: {e}")
        return False
```

---

## Validaciones

### Patente (alfanumérico)
```python
patron = r'^[A-Za-z0-9]+$'  # Solo letras y números
```

### Email
```python
patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
```

---

## Cómo Ejecutar

### 1. Activar el entorno virtual
```bash
cd "/home/david/UTN Python/Python_Intermedio/app_estacionameinto"
source venv/bin/activate
```

### 2. Ejecutar la aplicación
```bash
python3 main.py
```

### Instalación de dependencias (si es necesario)
```bash
python3 -m venv venv
source venv/bin/activate
pip install peewee
```

---

## Generar Documentación Sphinx

### 1. Instalar Sphinx (si no está instalado)
```bash
pip install sphinx
```

### 2. Generar HTML
```bash
cd docs
make html
```

### 3. Ver la documentación
Abrir `docs/_build/html/index.html` en el navegador.

---

## Autores

- **[Nombre del alumno]**
- **Diplomatura UTN - Python Nivel Intermedio 2026**
