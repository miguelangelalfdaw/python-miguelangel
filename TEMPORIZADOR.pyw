import tkinter as tk
import subprocess

COMANDOS = {
    "apagar": "shutdown /s /f /t 0",
    "suspender": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)\"",
    "hibernar": "shutdown /h",
}

segundos_restantes = 0
tarea = None


def iniciar():
    global segundos_restantes
    try:
        total = (int(horas.get()) * 3600
                 + int(minutos.get()) * 60
                 + int(segundos.get()))
    except ValueError:
        etiqueta.config(text="Usa solo números")
        return
    if total <= 0:
        etiqueta.config(text="Pon más de 0 segundos")
        return
    cancelar()
    segundos_restantes = total
    actualizar()


def rapido(h):
    for caja, valor in ((horas, h), (minutos, 0), (segundos, 0)):
        caja.delete(0, "end")
        caja.insert(0, valor)
    iniciar()


def actualizar():
    global segundos_restantes, tarea
    if segundos_restantes <= 0:
        etiqueta.config(text="Ejecutando...")
        subprocess.run(COMANDOS[accion.get()], shell=True)
        return
    h, resto = divmod(segundos_restantes, 3600)
    m, s = divmod(resto, 60)
    etiqueta.config(text=f"{accion.get()} en {h:02d}:{m:02d}:{s:02d}")
    segundos_restantes -= 1
    tarea = ventana.after(1000, actualizar)


def cancelar():
    global tarea
    if tarea is not None:
        ventana.after_cancel(tarea)
        tarea = None
    etiqueta.config(text="Cancelado")


def rueda(evento, caja):
    if evento.delta > 0:
        caja.invoke("buttonup")
    else:
        caja.invoke("buttondown")


def crear_caja(padre, maximo):
    caja = tk.Spinbox(padre, from_=0, to=maximo, wrap=True, width=3,
                      format="%02.0f", font=("Arial", 32), justify="center")
    caja.bind("<MouseWheel>", lambda e, c=caja: rueda(e, c))
    return caja


ventana = tk.Tk()
ventana.title("Gestor de energía")
ventana.geometry("380x470")

accion = tk.StringVar(value="apagar")

tk.Label(ventana, text="¿Qué hacer?", font=("Arial", 14)).pack(pady=5)
for opcion in COMANDOS:
    tk.Radiobutton(ventana, text=opcion.capitalize(), variable=accion,
                   value=opcion, font=("Arial", 14)).pack()

tk.Label(ventana, text="¿En cuánto tiempo?", font=("Arial", 14)).pack(pady=10)

fila_tiempo = tk.Frame(ventana)
fila_tiempo.pack()
horas = crear_caja(fila_tiempo, 23)
minutos = crear_caja(fila_tiempo, 59)
segundos = crear_caja(fila_tiempo, 59)
horas.pack(side="left")
tk.Label(fila_tiempo, text=":", font=("Arial", 32)).pack(side="left")
minutos.pack(side="left")
tk.Label(fila_tiempo, text=":", font=("Arial", 32)).pack(side="left")
segundos.pack(side="left")

tk.Button(ventana, text="Iniciar", font=("Arial", 16),
          command=iniciar).pack(pady=10)

fila_rapida = tk.Frame(ventana)
fila_rapida.pack()
for h in (1, 2, 3):
    tk.Button(fila_rapida, text=f"{h} h", font=("Arial", 12), width=5,
              command=lambda h=h: rapido(h)).pack(side="left", padx=5)

etiqueta = tk.Label(ventana, text="Sin temporizador", font=("Arial", 14))
etiqueta.pack(pady=10)

tk.Button(ventana, text="CANCELAR", font=("Arial", 16, "bold"), bg="tomato",
          command=cancelar).pack(fill="x", padx=20, pady=5)

ventana.mainloop()