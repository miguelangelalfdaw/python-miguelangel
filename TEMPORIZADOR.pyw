import tkinter as tk
import subprocess

COMANDOS = {
    "apagar": "shutdown /s /f /t 0",
    "suspender": "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)\"",
    "hibernar": "shutdown /h",
}

segundos_restantes = 0
tarea = None
modo_oscuro = True  # <--- Iniciamos en modo oscuro por defecto

# Paletas de colores
CLARO = {
    "bg": "#f0f0f0",
    "fg": "#000000",
    "widget_bg": "#ffffff",
    "btn_bg": "#e1e1e1"
}

OSCURO = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "widget_bg": "#2d2d2d",
    "btn_bg": "#3c3c3c"
}

def aplicar_tema():
    tema = OSCURO if modo_oscuro else CLARO
    
    ventana.config(bg=tema["bg"])
    
    for widget in widgets_a_actualizar:
        tipo = widget.winfo_class()
        if tipo in ("Label", "Radiobutton"):
            widget.config(bg=tema["bg"], fg=tema["fg"])
            if tipo == "Radiobutton":
                widget.config(selectcolor=tema["widget_bg"])
        elif tipo == "Button" and widget != btn_cancelar:
            widget.config(bg=tema["btn_bg"], fg=tema["fg"])
        elif tipo == "Frame":
            widget.config(bg=tema["bg"])
            
    btn_modo.config(text="☀️ Modo Claro" if modo_oscuro else "🌙 Modo Oscuro",
                    bg=tema["btn_bg"], fg=tema["fg"])

def alternar_modo():
    global modo_oscuro
    modo_oscuro = not modo_oscuro
    aplicar_tema()

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
ventana.geometry("380x520")

widgets_a_actualizar = []

btn_modo = tk.Button(ventana, text="☀️ Modo Claro", font=("Arial", 10), command=alternar_modo)
btn_modo.pack(anchor="ne", padx=15, pady=10)
widgets_a_actualizar.append(btn_modo)

accion = tk.StringVar(value="apagar")

lbl_que = tk.Label(ventana, text="¿Qué hacer?", font=("Arial", 14))
lbl_que.pack(pady=5)
widgets_a_actualizar.append(lbl_que)

for opcion in COMANDOS:
    rb = tk.Radiobutton(ventana, text=opcion.capitalize(), variable=accion,
                        value=opcion, font=("Arial", 14))
    rb.pack()
    widgets_a_actualizar.append(rb)

lbl_cuanto = tk.Label(ventana, text="¿En cuánto tiempo?", font=("Arial", 14))
lbl_cuanto.pack(pady=10)
widgets_a_actualizar.append(lbl_cuanto)

fila_tiempo = tk.Frame(ventana)
fila_tiempo.pack()
widgets_a_actualizar.append(fila_tiempo)

horas = crear_caja(fila_tiempo, 23)
minutos = crear_caja(fila_tiempo, 59)
segundos = crear_caja(fila_tiempo, 59)

horas.pack(side="left")
lbl_sep1 = tk.Label(fila_tiempo, text=":", font=("Arial", 32))
lbl_sep1.pack(side="left")
widgets_a_actualizar.append(lbl_sep1)

minutos.pack(side="left")
lbl_sep2 = tk.Label(fila_tiempo, text=":", font=("Arial", 32))
lbl_sep2.pack(side="left")
widgets_a_actualizar.append(lbl_sep2)

segundos.pack(side="left")

btn_iniciar = tk.Button(ventana, text="Iniciar", font=("Arial", 16), command=iniciar)
btn_iniciar.pack(pady=10)
widgets_a_actualizar.append(btn_iniciar)

fila_rapida = tk.Frame(ventana)
fila_rapida.pack()
widgets_a_actualizar.append(fila_rapida)

for h in (1, 2, 3):
    b_rap = tk.Button(fila_rapida, text=f"{h} h", font=("Arial", 12), width=5,
                      command=lambda h=h: rapido(h))
    b_rap.pack(side="left", padx=5)
    widgets_a_actualizar.append(b_rap)

etiqueta = tk.Label(ventana, text="Sin temporizador", font=("Arial", 14))
etiqueta.pack(pady=10)
widgets_a_actualizar.append(etiqueta)

btn_cancelar = tk.Button(ventana, text="CANCELAR", font=("Arial", 16, "bold"), bg="tomato", fg="white",
                         command=cancelar)
btn_cancelar.pack(fill="x", padx=20, pady=5)

# Aplicar los estilos oscuros antes de mostrar la ventana
aplicar_tema()

ventana.mainloop()