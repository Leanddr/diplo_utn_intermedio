.. App Estacionamiento documentation master file

=========================================
App Estacionamiento - Documentación
=========================================

Aplicación de gestión de estacionamiento desarrollada para la 
**Diplomatura UTN - Python Nivel Intermedio**.

.. contents:: Contenido
   :local:
   :depth: 2

Descripción General
===================

Esta aplicación permite gestionar un estacionamiento con las siguientes funcionalidades:

* **Alta de vehículos**: Registrar el ingreso de vehículos
* **Consulta**: Ver vehículos actualmente estacionados
* **Salida**: Registrar la salida y calcular el monto a cobrar
* **Edición**: Modificar datos de un estacionamiento en curso
* **Eliminación**: Borrar registros
* **Historial**: Ver estacionamientos finalizados

Arquitectura MVC
================

La aplicación está estructurada siguiendo el patrón **Modelo-Vista-Controlador (MVC)**:

* **Modelo** (``model.py``): Clases para acceso a base de datos
* **Vista** (``view.py``): Interfaz gráfica con Tkinter
* **Controlador** (``controller.py``): Lógica de negocio y coordinación

Diagrama de Arquitectura::

    ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
    │    Vista    │────▶│ Controlador  │────▶│   Modelo    │
    │  (Tkinter)  │◀────│              │◀────│  (SQLite)   │
    └─────────────┘     └──────────────┘     └─────────────┘

Tecnologías Utilizadas
======================

* **Python 3**: Lenguaje de programación
* **Tkinter**: Interfaz gráfica
* **Peewee ORM**: Mapeo objeto-relacional para SQLite
* **SQLite3**: Base de datos
* **POO**: Programación Orientada a Objetos
* **Sphinx**: Generación de documentación

Instalación y Ejecución
=======================

Requisitos Previos
------------------

* Python 3.8 o superior
* pip (gestor de paquetes de Python)

Pasos de Instalación
--------------------

1. **Crear entorno virtual**::

    python3 -m venv venv

2. **Activar el entorno virtual**:

   En Linux/Mac::

    source venv/bin/activate

   En Windows::

    venv\Scripts\activate

3. **Instalar dependencias**::

    pip install -r requirements.txt

Ejecución de la Aplicación
--------------------------

Con el entorno virtual activado, ejecutar::

    python3 main.py

La aplicación abrirá una ventana gráfica para gestionar el estacionamiento.

Estructura del Proyecto
=======================

::

    app_estacionameinto/
    ├── main.py           # Punto de entrada
    ├── model.py          # Clases BaseDeDatos y Estacionamiento
    ├── view.py           # Interfaz Tkinter
    ├── controller.py     # Lógica de control
    ├── validaciones.py   # Funciones de validación
    └── docs/             # Documentación Sphinx
        ├── conf.py
        ├── index.rst
        └── modules.rst

Módulos
=======

.. toctree::
   :maxdepth: 2
   :caption: Documentación de Módulos:

   modules

Índices y Tablas
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Autor
=====

* **Alumno:** Leandro Romero
* **DNI:** 33028043

Diplomatura UTN - Python Nivel Intermedio - 2026
