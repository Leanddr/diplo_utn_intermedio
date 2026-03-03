Módulos de la Aplicación
========================

Este documento contiene la documentación técnica de cada módulo,
generada automáticamente desde los **docstrings** del código fuente.

.. contents:: Contenido
   :local:

Módulo: model
-------------

Contiene las clases para el acceso a la base de datos SQLite usando **Peewee ORM**.

Clase EstacionamientoModel
~~~~~~~~~~~~~~~~~~~~~~~~~~

Modelo Peewee que representa la tabla ``estacionamientos`` en la base de datos.
Define la estructura de campos y mapeo ORM.

.. autoclass:: model.EstacionamientoModel
   :members:
   :undoc-members:
   :show-inheritance:

Clase BaseDeDatos
~~~~~~~~~~~~~~~~~

Maneja la conexión a la base de datos. Implementa el patrón *context manager*
para uso con la sentencia ``with``.

.. autoclass:: model.BaseDeDatos
   :members:
   :undoc-members:
   :show-inheritance:

Clase Estacionamiento
~~~~~~~~~~~~~~~~~~~~~

Implementa las operaciones CRUD sobre los registros de estacionamiento.
Utiliza Peewee ORM para las consultas a la base de datos.

.. autoclass:: model.Estacionamiento
   :members:
   :undoc-members:
   :show-inheritance:


Módulo: controller
------------------

Contiene las funciones que coordinan la interacción entre la vista y el modelo.

.. automodule:: controller
   :members:
   :undoc-members:
   :show-inheritance:


Módulo: validaciones
--------------------

Contiene funciones auxiliares para validación de datos y cálculos.

.. automodule:: validaciones
   :members:
   :undoc-members:
   :show-inheritance:


Módulo: view
------------

Contiene la interfaz gráfica desarrollada con Tkinter.

.. automodule:: view
   :members:
   :undoc-members:
   :show-inheritance:


Módulo: main
------------

Punto de entrada de la aplicación.

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:
