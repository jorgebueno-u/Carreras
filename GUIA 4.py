import tkinter as tk
from tkinter import ttk, messagebox
import random
import time


ventana = tk.Tk()
ventana.title("Competencia Automovilística")
ventana.geometry("1000x700")
ventana.resizable(False, False)



NUM_VEHICULOS = 10

posiciones = []
direcciones = []
vueltas = []
tiempos = []
finalizados = []

corriendo = False
inicio = 0

apuesta = tk.IntVar(value=1)

numero_vueltas = tk.IntVar(value=3)

velocidad_general = tk.IntVar(value=5)



canvas = tk.Canvas(
    ventana,
    width=900,
    height=450,
    bg="white"
)

canvas.pack(pady=10)


colores = [
    "red",
    "blue",
    "green",
    "orange",
    "purple",
    "brown",
    "pink",
    "cyan",
    "yellow",
    "gray"
]

vehiculos = []

for i in range(NUM_VEHICULOS):

    y = 25 + i * 42

    canvas.create_line(
        30, y + 20,
        850, y + 20,
        fill="black"
    )

    canvas.create_text(
        15, y + 20,
        text=str(i + 1)
    )

    carro = canvas.create_rectangle(
        40, y + 10,
        70, y + 30,
        fill=colores[i]
    )

    vehiculos.append(carro)

    posiciones.append(40)
    direcciones.append(1)
    vueltas.append(0)
    tiempos.append(0)
    finalizados.append(False)



def mover_vehiculo(numero):

    global corriendo

    if not corriendo:
        return

    if finalizados[numero]:
        return

    movimiento = random.randint(5, 15)

    posiciones[numero] += movimiento * direcciones[numero]

    if posiciones[numero] >= 820:

        posiciones[numero] = 820

        direcciones[numero] = -1

    elif posiciones[numero] <= 40:

        posiciones[numero] = 40

        # Cambia dirección
        direcciones[numero] = 1

        vueltas[numero] += 1

        if vueltas[numero] >= numero_vueltas.get():

            finalizados[numero] = True
            tiempos[numero] = time.time() - inicio

            revisar_finalizacion()

            return

    coordenadas = canvas.coords(vehiculos[numero])

    x_actual = posiciones[numero]

    y1 = coordenadas[1]
    y2 = coordenadas[3]

    canvas.coords(
        vehiculos[numero],
        x_actual,
        y1,
        x_actual + 30,
        y2
    )

    valor = velocidad_general.get()

    intervalo = random.randint(30, 100)

    intervalo = int(intervalo / valor * 5)

    if intervalo < 10:
        intervalo = 10

    ventana.after(
        intervalo,
        lambda: mover_vehiculo(numero)
    )


def revisar_finalizacion():

    if all(finalizados):

        terminar_carrera()


def terminar_carrera():

    global corriendo

    corriendo = False

    resultados = []

    for i in range(NUM_VEHICULOS):
        resultados.append(
            (i + 1, tiempos[i])
        )

    resultados.sort(key=lambda x: x[1])

    # Mostrar resultados
    mostrar_resultados(resultados)

    ganador = resultados[0][0]

    if ganador == apuesta.get():

        messagebox.showinfo(
            "Resultado",
            "¡Ganaste la apuesta!\n\n"
            + "El vehículo ganador fue el #" + str(ganador)
        )

    else:

        messagebox.showinfo(
            "Resultado",
            "Perdiste la apuesta.\n\n"
            + "El vehículo ganador fue el #" + str(ganador)
        )


def mostrar_resultados(resultados):

    for item in tabla.get_children():
        tabla.delete(item)

    posicion = 1

    for vehiculo, tiempo in resultados:

        tabla.insert(
            "",
            "end",
            values=(
                posicion,
                "Vehículo " + str(vehiculo),
                round(tiempo, 2)
            )
        )

        posicion += 1


def iniciar():

    global corriendo
    global inicio

    if corriendo:
        return

    for i in range(NUM_VEHICULOS):

        posiciones[i] = 40
        direcciones[i] = 1
        vueltas[i] = 0
        tiempos[i] = 0
        finalizados[i] = False

        y = 25 + i * 42

        canvas.coords(
            vehiculos[i],
            40,
            y + 10,
            70,
            y + 30
        )

    for item in tabla.get_children():
        tabla.delete(item)

    corriendo = True

    inicio = time.time()

    for i in range(NUM_VEHICULOS):
        mover_vehiculo(i)


def reiniciar():

    global corriendo

    corriendo = False

    for i in range(NUM_VEHICULOS):

        posiciones[i] = 40
        direcciones[i] = 1
        vueltas[i] = 0
        tiempos[i] = 0
        finalizados[i] = False

        y = 25 + i * 42

        canvas.coords(
            vehiculos[i],
            40,
            y + 10,
            70,
            y + 30
        )

    for item in tabla.get_children():
        tabla.delete(item)


marco_controles = tk.Frame(ventana)
marco_controles.pack()


tk.Label(
    marco_controles,
    text="Número de vueltas:"
).grid(row=0, column=0, padx=5)

spin_vueltas = tk.Spinbox(
    marco_controles,
    from_=1,
    to=20,
    textvariable=numero_vueltas,
    width=5
)

spin_vueltas.grid(row=0, column=1, padx=5)


tk.Label(
    marco_controles,
    text="Apuesta:"
).grid(row=0, column=2, padx=5)

combo_apuesta = ttk.Combobox(
    marco_controles,
    textvariable=apuesta,
    values=list(range(1, 11)),
    width=5,
    state="readonly"
)

combo_apuesta.grid(row=0, column=3, padx=5)

combo_apuesta.current(0)


tk.Label(
    marco_controles,
    text="Velocidad:"
).grid(row=0, column=4, padx=5)

slider = tk.Scale(
    marco_controles,
    from_=1,
    to=10,
    orient="horizontal",
    variable=velocidad_general
)

slider.grid(row=0, column=5, padx=5)


boton_iniciar = tk.Button(
    marco_controles,
    text="Iniciar carrera",
    command=iniciar,
    bg="lightgreen"
)

boton_iniciar.grid(
    row=0,
    column=6,
    padx=10
)


boton_reiniciar = tk.Button(
    marco_controles,
    text="Reiniciar",
    command=reiniciar
)

boton_reiniciar.grid(
    row=0,
    column=7,
    padx=10
)


tk.Label(
    ventana,
    text="Resultados de la carrera",
    font=("Arial", 14, "bold")
).pack(pady=5)


tabla = ttk.Treeview(
    ventana,
    columns=("posicion", "vehiculo", "tiempo"),
    show="headings",
    height=8
)

tabla.heading(
    "posicion",
    text="Posición"
)

tabla.heading(
    "vehiculo",
    text="Vehículo"
)

tabla.heading(
    "tiempo",
    text="Tiempo (segundos)"
)

tabla.column(
    "posicion",
    width=100,
    anchor="center"
)

tabla.column(
    "vehiculo",
    width=200,
    anchor="center"
)

tabla.column(
    "tiempo",
    width=200,
    anchor="center"
)

tabla.pack()


ventana.mainloop()