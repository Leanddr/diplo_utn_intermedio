from model import BaseDeDatos, Estacionamiento
from validaciones import aux_email_formato, aux_calcular_total, validar_patente
from tkinter.messagebox import showwarning, showinfo, askyesno, showerror


#-------------------------------------------------------------
# Controlador - Versión POO
#----------------------------------------------------------------
# El controlador ahora usa la CLASE Estacionamiento del modelo
# en lugar de funciones sueltas. Esto cumple con el paradigma POO.
#
# CAMBIOS PRINCIPALES:
# - Creamos una instancia de Estacionamiento para las operaciones
# - Ya no manejamos conexiones manualmente (las clases lo hacen)
# - Se agregó validación de patente con regex
#----------------------------------------------------------------


# Variable global para saber qué registro se está editando
id_seleccionado = None

# Creamos UNA instancia de la clase Estacionamiento
# Esta instancia se usa en todas las funciones del controlador
estacionamiento = Estacionamiento()


# ============================================================
# ALTA  - Registrar ingresos de autos
# ============================================================

def ctrl_registro_de_ingreso(vars_ui, tree):
    """
    Controlador para registrar un nuevo ingreso.
    
    Parámetros:
        vars_ui: diccionario con las StringVar del formulario
        tree: widget Treeview para actualizar la vista
    
    Retorna:
        Diccionario con status, kind, title y message
    """
    # Obtengo datos desde la vista (StringVar)
    patente = vars_ui["patente"].get()
    vehiculo = vars_ui["vehiculo"].get()
    nombre = vars_ui["nombre"].get()
    apellido = vars_ui["apellido"].get()
    dni = vars_ui["dni"].get()
    email = vars_ui["email"].get()
    valor_hora = vars_ui["valor_hora"].get()

    # ---------------------------------------------------------
    # VALIDACIONES
    # ---------------------------------------------------------
    
    # Validar que el valor por hora sea numérico
    if not valor_hora.isdigit():
        return {
            "status": "error",
            "kind": "warning",
            "title": "Atención",
            "message": "El valor por hora debe ser numérico",
        }

    # Validar que todos los campos estén completos
    if patente == "" or vehiculo == "" or nombre == "" or apellido == "" or dni == "" or email == "":
        return {
            "status": "error",
            "kind": "warning",
            "title": "Atención",
            "message": "Todos los campos obligatorios deben estar completos",
        }
    
    # Validar formato de patente (solo alfanuméricos)
    if not validar_patente(patente):
        return {
            "status": "error",
            "kind": "warning",
            "title": "Patente inválida",
            "message": f"La patente '{patente}' no tiene formato válido. Solo se permiten letras y números.",
        }

    # Validar formato de email
    if not aux_email_formato(email):
        return {
            "status": "error",
            "kind": "warning",
            "title": "Formato de email inválido",
            "message": f"El email '{email}' no tiene formato válido",
        }

    # ---------------------------------------------------------
    # OPERACIÓN EN BASE DE DATOS (usando la clase Estacionamiento)
    # ---------------------------------------------------------
    
    # Usamos el método de la clase en lugar de función suelta
    resultado = estacionamiento.registrar_ingreso(
        patente, vehiculo, nombre, apellido, dni, email, float(valor_hora)
    )
    
    # Verificamos si hubo error
    if not resultado:
        return {
            "status": "error",
            "kind": "error",
            "title": "Error",
            "message": "No se pudo registrar el ingreso. Revise la consola.",
        }

    # Limpiar campos del formulario
    for var in vars_ui.values():
        var.set("")

    # Actualizar la vista
    ctrl_cargar_treeview(tree)

    return {
        "status": "ok",
        "kind": "info",
        "title": "Ingreso registrado",
        "message": "El vehículo se registró correctamente.",
    }


# ============================================================
# ACTUALIZAR VISTA - Cargar datos en el Treeview
# ============================================================

def ctrl_cargar_treeview(tree):
    """
    Carga los estacionamientos en curso en el Treeview.
    
    Parámetros:
        tree: widget Treeview a actualizar
    """
    # Limpio la tabla (borro todas las filas)
    for fila in tree.get_children():
        tree.delete(fila)

    # Obtengo los datos usando el método de la clase
    datos = estacionamiento.obtener_estacionados()

    # Notifico si no hay registros
    if not datos:
        showinfo("Sin registros", "No hay vehículos estacionados actualmente")
        return

    # Inserto cada fila en el treeview
    for fila in datos:
        tree.insert("", "end", text=fila[0], values=fila[1:])


# ============================================================
# REGISTRO DE SALIDAS
# ============================================================

def ctrl_registro_de_salidas(tree):
    """
    Inicia el proceso de registrar la salida de un vehículo.
    Primero pide confirmación al usuario.
    
    Parámetros:
        tree: widget Treeview con la selección
    
    Retorna:
        Diccionario con status y datos necesarios para confirmar
    """
    seleccion = tree.selection()

    if not seleccion:
        return {
            "status": "error",
            "kind": "warning",
            "title": "Atención",
            "message": "Debe seleccionar un vehículo"
        }

    # Obtener el ID del registro seleccionado
    item = seleccion[0]
    id_registro = tree.item(item, "text")
    valores = tree.item(item, "values")

    patente = valores[0]
    vehiculo = valores[1]

    # Obtener datos para calcular el total (usando la clase)
    datos = estacionamiento.obtener_datos_para_salida(id_registro)

    if not datos:
        return {
            "status": "error",
            "kind": "error",
            "title": "Error",
            "message": "No se pudo obtener el ingreso del vehículo",
        }

    # Calcular el total a cobrar
    hora_ingreso, valor_hora = datos
    total = aux_calcular_total(hora_ingreso, valor_hora)

    # Pedir confirmación al usuario
    return {
        "status": "need_confirm",
        "title": "Confirma salida",
        "message": (
            "¿Estás seguro que desea registrar la salida del vehículo?\n\n"
            f"Patente: {patente}\n"
            f"Vehículo: {vehiculo}\n"
            f"Total a cobrar: ${total}\n"
        ),
        "data": {
            "id_registro": id_registro,
            "total": total,
        },
    }


def ctrl_confirmar_salida(id_registro, total, tree):
    """
    Confirma y ejecuta la salida del vehículo.
    Se llama después de que el usuario confirma.
    
    Parámetros:
        id_registro: ID del estacionamiento
        total: monto a cobrar
        tree: widget Treeview a actualizar
    
    Retorna:
        Diccionario con status del resultado
    """
    # Registrar la salida usando la clase
    resultado = estacionamiento.registrar_salida(id_registro, total)
    
    if not resultado:
        return {
            "status": "error",
            "kind": "error",
            "title": "Error",
            "message": "No se pudo registrar la salida.",
        }

    # Actualizar la vista
    ctrl_cargar_treeview(tree)

    return {
        "status": "ok",
        "kind": "info",
        "title": "Salida registrada",
        "message": "La salida del vehículo se registró correctamente.",
    }


# ============================================================
# ELIMINAR REGISTROS
# ============================================================

def ctrl_borrar_registro(tree):
    """
    Elimina el registro seleccionado.
    
    Parámetros:
        tree: widget Treeview con la selección
    
    Retorna:
        Diccionario con status del resultado
    """
    seleccion = tree.focus()

    if not seleccion:
        return {
            "status": "error",
            "kind": "warning",
            "title": "Atención",
            "message": "Debe seleccionar un registro",
        }

    id_registro = tree.item(seleccion, "text")

    # Eliminar usando la clase
    resultado = estacionamiento.eliminar_registro(id_registro)
    
    if not resultado:
        return {
            "status": "error",
            "kind": "error",
            "title": "Error",
            "message": "No se pudo eliminar el registro.",
        }

    # Actualizar la vista
    ctrl_cargar_treeview(tree)

    return {
        "status": "ok",
        "kind": "info",
        "title": "Registro eliminado",
        "message": "El registro se eliminó correctamente",
    }


# ============================================================
# OBTENER HISTORIAL
# ============================================================

def ctrl_obtener_historial(tree):
    """
    Muestra el historial de estacionamientos finalizados.
    
    Parámetros:
        tree: widget Treeview a actualizar
    """
    # Limpio la vista
    for fila in tree.get_children():
        tree.delete(fila)

    # Obtengo datos del historial usando la clase
    datos = estacionamiento.obtener_historial()

    # Verifico si hay datos
    if not datos:
        showinfo("Historial vacío", "No hay registros con estado finalizados")
        return

    # Cargo los datos en la vista
    for fila in datos:
        tree.insert("", "end", text=fila[0], values=fila[1:])


# ============================================================
# EDITAR REGISTROS - Solo los que están en curso
# ============================================================

def ctrl_editar_registros(tree, vars_ui):
    """
    Carga los datos del registro seleccionado en el formulario para editarlos.
    
    Parámetros:
        tree: widget Treeview con la selección
        vars_ui: diccionario con las StringVar del formulario
    
    Retorna:
        True si se cargaron los datos, False si hubo error
    """
    global id_seleccionado

    # Controlo si hay un item seleccionado
    seleccion = tree.focus()
    if not seleccion:
        showwarning("Atención", "Debes seleccionar un registro para editarlo")
        return False

    valores = tree.item(seleccion, "values")
    estado = valores[11]  # Columna Estado

    # Verifico si el estado es "En curso"
    if estado != "En curso":
        showwarning(
            "Edición no permitida",
            "Solo se pueden editar estacionamientos en curso"
        )
        return False

    # Guardo el ID del registro que se está editando
    id_seleccionado = tree.item(seleccion, "text")

    # Cargo el formulario con los datos del registro seleccionado
    vars_ui["patente"].set(valores[0])
    vars_ui["vehiculo"].set(valores[1])
    vars_ui["nombre"].set(valores[2])
    vars_ui["apellido"].set(valores[3])
    vars_ui["dni"].set(valores[4])
    vars_ui["email"].set(valores[5])
    vars_ui["valor_hora"].set(valores[9])

    return True


# ============================================================
# GUARDAR EDICIÓN
# ============================================================

def ctrl_guardar_edicion(tree, vars_ui):
    """
    Guarda los cambios del registro que se está editando.
    
    Parámetros:
        tree: widget Treeview a actualizar
        vars_ui: diccionario con las StringVar del formulario
    
    Retorna:
        True si se guardó correctamente, False si hubo error
    """
    global id_seleccionado

    # Verifico que haya un registro en edición
    if id_seleccionado is None:
        showwarning("Atención", "No hay registros en edición")
        return False

    # Obtengo datos desde la vista
    patente = vars_ui["patente"].get()
    vehiculo = vars_ui["vehiculo"].get()
    nombre = vars_ui["nombre"].get()
    apellido = vars_ui["apellido"].get()
    dni = vars_ui["dni"].get()
    email = vars_ui["email"].get()
    valor_hora = vars_ui["valor_hora"].get()

    # Verifico que todos los campos estén completos
    if "" in (patente, vehiculo, nombre, apellido, dni, email, valor_hora):
        showwarning("Atención", "Complete todos los campos")
        return False
    
    # Validar formato de patente
    if not validar_patente(patente):
        showwarning("Patente inválida", 
                    f"La patente '{patente}' no tiene formato válido")
        return False

    # Verifico formato de email
    if not aux_email_formato(email):
        showwarning("Formato de email inválido",
                    f"El email '{email}' no tiene formato válido")
        return False

    # Pido confirmación
    confirmar = askyesno(
        "Confirmar edición",
        "¿Está seguro que desea guardar los cambios?"
    )

    if not confirmar:
        return False

    # Guardar usando la clase
    resultado = estacionamiento.editar_registro(
        id_seleccionado, patente, vehiculo, nombre, apellido, dni, email, valor_hora
    )
    
    if not resultado:
        showwarning("Error", "No se pudo guardar la edición")
        return False

    # Limpiar el formulario
    for var in vars_ui.values():
        var.set("")

    id_seleccionado = None
    
    # Actualizar la vista
    ctrl_cargar_treeview(tree)

    return True
    