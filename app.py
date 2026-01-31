import tkinter as tk
import sqlite3

# Conexión a BD
conexion = sqlite3.connect("tarea.db")
cursor = conexion.cursor()



# Ventana
ventana = tk.Tk()
ventana.title("To-Do List")


frame = tk.Frame(ventana)
frame.pack(pady=10)


# Lista de tareas
tareas_vars = []


# Cargar tareas
def cargar_tareas():

    for widget in frame.winfo_children():
        widget.destroy()

    tareas_vars.clear()

    cursor.execute("SELECT * FROM tarea")
    filas = cursor.fetchall()

    for tarea in filas:
        id_tarea = tarea[0]
        Descripcion = tarea[1]
        Estado = tarea[2]

        var = tk.IntVar(value=Estado)

        check = tk.Checkbutton(
            frame,
            text=Descripcion,
            variable=var,
            command=lambda i=id_tarea, v=var: actualizar(i, v)
        )

        if Estado == 1:
            check.config(fg="gray")

        check.pack(anchor="w")

        tareas_vars.append(var)


# Agregar tarea
def agregar():

    texto = entrada.get()

    if texto == "":
        return

    cursor.execute(
        "INSERT INTO tarea (Descripcion, Estado) VALUES (?, 0)",
        (texto,)
    )

    conexion.commit()

    entrada.delete(0, tk.END)

    cargar_tareas()


# Actualizar estado
def actualizar(id_tarea, var):

    Estado = var.get()

    cursor.execute(
        "UPDATE tarea SET Estado=? WHERE id=?",
        (Estado, id_tarea)
    )

    conexion.commit()

    cargar_tareas()


# Entrada
entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=5)


# Botón
btn = tk.Button(ventana, text="Agregar", command=agregar)
btn.pack()


# Cargar al iniciar
cargar_tareas()


ventana.mainloop()
conexion.close()