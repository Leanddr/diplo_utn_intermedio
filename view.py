from controller import *
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *


#----------------------
# Vista
#---------------------
def iniciar_app():
    root = Tk()
    root.title("GESTION DE ESTACIONAMIENTO 🚘🛵🛻")
    root.geometry("1210x800")
    root.configure(bg="paleturquoise")
    # titulo = Label(root, text="Menu: ", bg="black", fg="thistle1", height=1, width=0)
    # titulo.grid(row=0, column=0, columnspan=1, padx=1, pady=1, sticky=E)


    # Variables tk - creamos las varibles
    var_patente = StringVar()
    var_vehiculo = StringVar()
    var_nombre_contacto = StringVar()
    var_apellido_contacto = StringVar()
    var_dni = StringVar()
    var_email = StringVar()
    var_fecha = StringVar()
    var_hora_ingreso = StringVar()
    var_hora_egreso = StringVar()
    var_valor_hora = StringVar()
    var_total = StringVar()
    var_estado = StringVar()


    #Agrupo vairables en diccionario para el controlador 
    vars_ui = {
        "patente": var_patente,
        "vehiculo": var_vehiculo,
        "nombre" : var_nombre_contacto,
        "apellido" : var_apellido_contacto,
        "dni" : var_dni,
        "email": var_email,
        "valor_hora" : var_valor_hora
    }

    # VALOR HORA
    Label(root, text="Valor por hora").grid(row=9, column=0)
    Entry(root, textvariable=var_valor_hora).grid(row=9, column=1)

    # Registrar ingreso
    titulo = Label(root, text="Registrar Ingreso", bg="black", fg="thistle1", height=1, )
    titulo.grid(row=1, column=0, columnspan=6, padx=1, pady=1, sticky=W+E)

    # Labels
    patente = Label(root, text="Patente", width=20)
    patente.grid(row=3, column=0, sticky=W+E )
    vehiculo = Label(root, text="Vehiculo", width=20)
    vehiculo.grid(row=4, column=0, sticky=W+E )
    nombre_contacto = Label(root, text="Nombre", width=50)
    nombre_contacto.grid(row=5, column=0, sticky=W+E )
    apellido_contato = Label(root, text="Apellido", width=50)
    apellido_contato.grid(row=6, column=0, sticky=W+E )
    dni = Label(root, text="DNI", width=50)
    dni.grid(row=7, column=0, sticky=W+E )
    email = Label(root, text="Email", width=80)
    email.grid(row=8, column=0, sticky=W+E )

    # Entry
    entry_patente = Entry(root, textvariable=var_patente, width=20)
    entry_patente.grid(row=3, column=1 )
    entry_vehiculo = Entry(root, textvariable=var_vehiculo, width=20)
    entry_vehiculo.grid(row=4, column=1 )
    entry_nombre_contacto = Entry(root, textvariable=var_nombre_contacto, width=20)
    entry_nombre_contacto.grid(row=5, column=1 )
    entry_apellido_contato = Entry(root, textvariable=var_apellido_contacto, width=20)
    entry_apellido_contato.grid(row=6, column=1 )
    entry_dni = Entry(root, textvariable=var_dni, width=20)
    entry_dni.grid(row=7, column=1 )
    entry_email = Entry(root, textvariable=var_email, width=20)
    entry_email.grid(row=8, column=1 )

    # Treeview -Grid
    tree = ttk.Treeview(root)
    tree ["columns"] = ("patente","vehiculo","nombre_contacto","apellido_contacto","dni","email","fecha","hora_ingreso","hora_egreso", "valor_hora" ,"total", "estado") 
    tree.column("#0", width=20, minwidth=20, anchor=W)
    tree.column("patente", width=50, minwidth=80, anchor=W)
    tree.column("vehiculo", width=50, minwidth=100, anchor=W)
    tree.column("nombre_contacto", width=100, minwidth=50, anchor=W)
    tree.column("apellido_contacto", width=100, minwidth=50, anchor=W)
    tree.column("dni", width=50, minwidth=100, anchor=W)
    tree.column("email", width=50, minwidth=100, anchor=W)
    tree.column("fecha", width=50, minwidth=100, anchor=W)
    tree.column("hora_ingreso", width=50, minwidth=100, anchor=W)
    tree.column("hora_egreso", width=50, minwidth=100, anchor=W)
    tree.column("valor_hora", width=50, minwidth=100, anchor=W)
    tree.column("total", width=50, minwidth=100, anchor=W)
    tree.column("estado", width=50, minwidth=100, anchor=W)

    # TreeGrid - Seccion Datos 
    titulo = Label(root, text="Autos estacionados", bg="black", fg="thistle1", height=1, )
    titulo.grid(column=0, row=10, columnspan=6, padx=3, pady=1, sticky=W+E)

    # Head de grilla 
    tree.heading("#0", text="ID")
    tree.heading("patente", text="Patente")
    tree.heading("vehiculo", text="Vehículo")
    tree.heading("nombre_contacto", text="Nombre")
    tree.heading("apellido_contacto", text="Apellido")
    tree.heading("dni", text="DNI")
    tree.heading("email", text="Email")
    tree.heading("fecha", text="Fecha")
    tree.heading("hora_ingreso", text="Hs ingreso")
    tree.heading("hora_egreso", text="Hs egreso")
    tree.heading("valor_hora", text="Valor hora")
    tree.heading("total", text="Total")
    tree.heading("estado", text="Estado")

    # Muestra tabla con datos
    tree.grid(column=0, row=13, columnspan= 6, padx=3, pady=1, sticky=W+E) 

        
    # Control sobre el boton editar 
    def on_editar():
        if ctrl_editar_registros(tree, vars_ui):
            boton_guardar_cambios.config(state=NORMAL)

    # Control sobre el boton guardar cambios 
    def on_guardar_cambios():
        if ctrl_guardar_edicion(tree, vars_ui):
            boton_guardar_cambios.config(state=DISABLED)    

    # [INGRESOS] Receptor de warning - errores - info

    def on_registrar_ingreso():
        resultado = ctrl_registro_de_ingreso(vars_ui, tree)

        if not resultado:
            return
        
        if resultado ["status"] == "error":
            kind = resultado.get("kind")
            if kind == "warning":
                showwarning(resultado["title"], resultado["message"])
            elif kind =="error":
                showerror(resultado["title"],resultado["message"])
        elif resultado["status"] == "ok":
            showinfo(resultado["title"],resultado["message"])

    # [BORRAR REGISTROS] Receptor de warning - errores - info

    def on_borrar_registro():
        resultado = ctrl_borrar_registro(tree)

        if not resultado:
            return
        
        if resultado["status"] == "error":
            kind = resultado.get("kind")
            if kind == "warning":
                showwarning(resultado["status"], resultado["message"])
            elif kind == "error":
                showerror(resultado["title"],resultado["message"])
        elif resultado ["status"] == "ok":
            showinfo(resultado["title"], resultado["message"])

    # [SALIDAS] Receptor de warning - errores - info

    def on_registrar_salida():
        resultado = ctrl_registro_de_salidas(tree)

        if not resultado:
            return
        
        if resultado["status"] =="error":
            kind = resultado.get("kind")
            if kind == "warning":
                showwarning(resultado["title", resultado["message"]])
            elif kind == "error":
                showerror(resultado["title", resultado["message"]])
            return
        if resultado["status"] == "need_confirm":
            confirmar = askyesno(resultado["title"], resultado["message"])
            if not confirmar:
                return
            
            data = resultado["data"]
            resultado_final= ctrl_confirmar_salida(
                data["id_registro"],
                data["total"],
                tree
            )

            if resultado_final and resultado_final["status"] == "ok":
                showinfo(resultado_final["title"],resultado_final["message"])


    # Botones

    boton_ingreso=Button(root, text="Registrar Ingreso", command= on_registrar_ingreso)
    boton_ingreso.grid(row=3, column=5)

    boton_guardar_cambios=Button(root, text="Guardar cambios" , state=DISABLED, command= on_guardar_cambios)
    boton_guardar_cambios.grid(row=8, column=5)

    boton_salidas=Button(root, text="Registrar Salida", command= on_registrar_salida)
    boton_salidas.grid(row=11, column=0, padx=2, pady=4)

    boton_editar=Button(root, text="Editar", command= on_editar)
    boton_editar.grid(row=11, column=1, padx=2, pady=4)

    boton_historial=Button(root, text="Ver Historial", command= lambda: ctrl_obtener_historial(tree))
    boton_historial.grid(row=11, column=3, padx=2, pady=4)

    boton_borrar=Button(root, text="Borrar Registro", command= on_borrar_registro)
    boton_borrar.grid(row=11, column=5, padx=2, pady=4)

    boton_ver_estacionados=Button(root, text="Ver Estacionados", command= lambda: ctrl_cargar_treeview(tree))
    boton_ver_estacionados.grid(row=11, column=4, padx=2, pady=4)


    root.mainloop()