import random 
nombres = ['Marcos', 'Ignacio', 'Alfonso', 'Jordi', 'Ricardo', 'Salvador', 
            'Hugo', 'Emilio', 'Guillermo', 'Gabriel', 'Marcos', 'Julio', 
            'Julián', 'Gonzalo', 'José Miguel', 'Tomás', 'Agustín', 'Martín', 
            'José Ramón', 'Nicolás', 'Félix', 'Joan', 'Ismael', 'Cristian', 
            'Samuel', 'Héctor', 'Juan Francisco', 'José', 'Mariano', 'Lucas', 
            'José Carlos', 'Domingo', 'Sebastián', 'Alfredo', 'Álex', 'César', 
            'Felipe', 'Víctor', 'Rodrigo', 'Gregorio', 'Alberto', 'Kaworu', 
            'Sonia', 'Sandra', 'Marina', 'Susana', 'Natalia', 'Yolanda', 
            'Margarita', 'Claudia', 'Eva', 'Carla', 'Esther', 'Phoebe', 
            'Sofía', 'Noelia', 'Verónica', 'Carolina', 'Miriam', 'Inés', 
            'Belén', 'Daniela', 'Martina', 'Ainhoa', 'Faye', 'Misato', 
            'Mai', 'Thais', 'Mikasa', 'Nezuko', 'Miku', 'Chika']

apellidos = ['González', 'Rodríguez', 'Fernández', 'Díaz', 'Pérez', 'Gómez', 
            'Lucero', 'Sosa', 'Quiroga', 'Martínez', 'López', 'Romero', 
            'Sánchez', 'Ruiz', 'Benítez', 'Silva', 'Flores', 'García', 
            'Muñoz', 'Rojas', 'Soto', 'Contreras', 'Sepúlveda', 'Morales', 
            'Fuentes', 'Hernández', 'Torres', 'Araya', 'Flores', 'Espinoza', 
            'Valenzuela', 'Castillo', 'Tapia', 'Reyes', 'Gutiérrez', 'Castro', 
            'Pizarro', 'Álvarez', 'Carrasco', 'Cortés', 'Herrera', 'Núñez', 
            'Jara', 'Vergara', 'Rivera', 'Figueroa', 'Riquelme', 'Miranda', 
            'Bravo', 'Vera', 'Molina', 'Vega', 'Campos', 'Sandoval', 
            'Orellana', 'Cárdenas', 'Olivares', 'Alarcón', 'Gallardo', 
            'Ortiz', 'Garrido', 'Salazar', 'Guzmán', 'Saavedra', 'Navarro', 
            'Aguilera', 'Parra', 'Romero', 'Aravena', 'Vargas', 'Cáceres', 
            'Yáñez', 'Leiva', 'Escobar', 'Valdés', 'Vidal', 'Salinas', 
            'Zúñiga', 'Peña', 'Godoy', 'Lagos', 'Maldonado', 'Bustos', 
            'Medina', 'Palma', 'Pino', 'Moreno', 'Sanhueza', 'Carvajal', 
            'Navarrete', 'Sáez', 'Alvarado', 'Donoso', 'Poblete', 'Bustamante', 
            'Toro', 'Ortega', 'Venegas', 'Guerrero', 'Mendoza', 'Farías', 
            'San Martín']

codigo_verificador = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'K']

def check_email(nombre, apellido1, apellido2, lista_emails, intento):
        if intento < len(apellido2):
            email = nombre + '.' + apellido1 + '.' + apellido2[:intento+1] + '@nashe.cl'
        else:
            email = nombre + '.' + apellido1 + '.' + apellido2 + '.' + str(intento)  + '@nashe.cl'

        if email in lista_emails:
            email = check_email(nombre[0], apellido1, apellido2, lista_emails, intento+1)
        return email

def crear_rut(lista_ruts):
    rut = str(random.randint(6, 19))
    for x in range(2):
        rut += '.'
        for x in range(3):
            rut = rut + str(random.randint(0, 9))
    rut += '-' + random.choice(codigo_verificador)
    if rut in lista_ruts:
        rut = crear_rut(lista_ruts)
    return rut

def crear_celular(lista_celulares):
    celular = '+56 9 '
    for x in range(8):
        celular +=  str(random.randint(0, 9))
    if celular in lista_celulares:
        celular = crear_celular
    return celular
    

def buscar_tildes(palabra):
    palabra = palabra.replace('á', 'a')
    palabra = palabra.replace('é', 'e')
    palabra = palabra.replace('í', 'i')
    palabra = palabra.replace('ó', 'o')
    palabra = palabra.replace('ú', 'u')
    palabra = palabra.replace('ü', 'ü')
    return palabra.lower()

    
emails = []
ruts = []
celulares = []


to_text = ''

for x in range(1962):
    nombre = random.choice(nombres)
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)
    nombre_correo = buscar_tildes(nombre.split()[0])
    apellido1_correo = buscar_tildes(apellido1)
    apellido2_correo = buscar_tildes(apellido2)
    email = nombre_correo + '.' + apellido1_correo + '@nashe.cl'
    if email in emails:
        email = check_email(nombre_correo, apellido1_correo, apellido2_correo, emails, 0)
    
    emails.append(email)

    rut = crear_rut(ruts)
    ruts.append(rut)
    celular = crear_celular(celulares)
    celulares.append(celular)

    to_text += nombre + ',' + apellido1 + ',' + apellido2 + ',' + rut + ',' \
                + email + ',' + celular + ',Testeo123.' + '\n'

archivo = open('conductores.txt', 'w')
archivo.write(to_text)
archivo.close()


    







to_text = ''
    
