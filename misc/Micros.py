import random 
archivo = open('recorridos.txt', 'r')
caracteres = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'P', 'R', 'S', 'T',
             'V', 'W', 'X', 'Y', 'Z']

recorridos = []
for linea in archivo:
    recorridos.append(linea[:-1])

archivo_micros = open('micros.txt', 'w')
buses = []

recorridos_usados = []
patentes = []
creando_micros = True
while creando_micros:
    bus = ''
    patente = ''

    for letra in range(4):
        patente += random.choice(caracteres)

    recorrido_actual = random.choice(recorridos)
    if not recorrido_actual in recorridos_usados:

        recorridos_usados.append(recorrido_actual)
        print(len(recorridos_usados))
        print(len(recorridos))
    patente += str(random.randint(10, 99))

    if not patente in patentes:
        patentes.append(patente)
        bus = patente + ',' + recorrido_actual
        buses.append(bus)


    if len(recorridos) == len(recorridos_usados):
        creando_micros = False

to_text = ''
for micro in buses:
    to_text += micro + '\n'

archivo_micros.write(to_text[:-1])
archivo_micros.close
