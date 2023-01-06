from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
micros = []
database = {'ruts': {},
            'bips':[], 
            'buses':{}, 
            'recorridos':{},
            'encuesta':['¿Cuán cordial es el conductor?', 
            '¿El conductor se detiene correctamente en los paraderos?',
            '¿El conductor espera correctamente el ingreso de los pasajeros?', 
            '¿El conductor maneja de manera segura?',
            '¿El conductor maneja sin distractores?']}


archivo_rutas = open('recorridos.txt', 'r')
archivo_micros = open('micros.txt', 'r')
archivo_conductores = open('conductores.txt', 'r')

# Usuario tipo administrador
class admin():
    def __init__(self, nombre, apellidos, rut, password):
        self.type = 'admin'
        self.nombre = nombre
        self.apellidos = apellidos
        self.rut = rut
        self.password = password
        self.infodict = {'type':self.type, 'nombre':self.nombre, 
                        'apellidos':self.apellidos, 'email':None,
                        'password': self.password, 
                        'rut':self.rut, 'bip':None, 
                        'transpuntos':None, 'micro':None}

    # Funciones para entregar la información de todos los 
    # usuarios, tanto en conjunto como por separado
    def get_user_info(self, user):
        usuario = database['ruts'][user]
        if usuario.type == 'conductor':
            usuario.update_data()
            return usuario.infodict


    def get_all_info(self):
        return_dict = {}
        for usuario in database['ruts']:
            usuario = database['ruts'][usuario]
            if usuario.type == 'conductor':
                usuario.update_data()
                return_dict[usuario.rut] = usuario.infodict

        return return_dict



## Define el objeto de usuario con la información útil para el programa
class user():
    def __init__(self, nombre, apellidos, email, rut, bip, password):
        self.type = 'user'
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.rut = rut
        self.bip = bip
        self.password = password
        self.transpuntos = 0
        self.infodict = {'type':self.type, 'nombre':self.nombre, 
                        'apellidos':self.apellidos, 'email':self.email, 
                        'rut':self.rut, 'bip':self.bip, 
                        'password':self.password,
                        'transpuntos':self.transpuntos, 
                        'preguntas': database['encuesta']}


    ## Actualiza el infodict con la información actual
    def update_data(self):
        self.infodict = {'type':self.type, 'nombre':self.nombre, 
                        'apellidos':self.apellidos, 'email':self.email, 
                        'rut':self.rut, 'bip':self.bip, 'password':self.password,
                        'transpuntos':self.transpuntos, 'preguntas': database['encuesta']}


# Define el objeto bus, con la información de la micro, y agregándose a si
# mismo en la lista de micros de su recorrido
class bus():
    def __init__(self, patente, recorrido):
        self.patente = patente 
        self.conductor = None
        self.recorrido = recorrido
        self.reclamos = None
        database['recorridos'][recorrido].buses.append(patente)

# Define el objeto correspondiente al chofer de micro, con sus datos
# personales, y el diccionario para mandarle a la app
class busdriver():
    def __init__(self, nombre, apellidos, rut,
                email, celular, password, micro=None):
        self.type = 'conductor'
        self.rut = rut
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.celular = celular
        self.micro = micro
        if micro != None:
            database['buses'][micro].conductor = rut
        self.password = password
        self.score = {'promedio': None, 'puntajes':{}}
        self.infodict = {'type':self.type, 'nombre':self.nombre, 
                        'apellidos':self.apellidos, 'email':self.email, 
                        'rut':self.rut, 'bip':None, 
                        'transpuntos':None, 'micro':self.micro, 
                        'score':self.score}

        # Automáticamente crea datos de respuesta para la encuesta
        # guardada en el sistema
        for pregunta in database['encuesta']:
            self.score['puntajes'].setdefault(pregunta, {'promedio': 0, 
                                                        'respuestas':0, 
                                                        'puntaje':0})

    # Función para actualizar la información del objeto, para posteriormente
    # mandarla a la aplicación 
    # Actualiza los promedios y el infodict que se le manda al usuario
    def update_data(self):

        for pregunta in self.score['puntajes']:
            pregunta = self.score['puntajes'][pregunta]
            if pregunta['respuestas'] != 0:
                pregunta['promedio'] = pregunta['puntaje'] \
                                        / pregunta['respuestas']


        total = 0
        descuentos = 0
        for promedio_pregunta in self.score['puntajes']:
            if self.score['puntajes'][promedio_pregunta]['promedio'] == 0:
                descuentos += 1
            total += self.score['puntajes'][promedio_pregunta]['promedio']
        
        if descuentos != len(self.score['puntajes']):

            self.score['promedio'] = total / (len(self.score['puntajes'])
                                                 - descuentos)
            
            print(self.score)
        self.infodict = {'type':self.type, 'nombre':self.nombre, 
                        'apellidos':self.apellidos, 'email':self.email, 
                        'rut':self.rut, 'bip':None, 
                        'transpuntos':None, 'micro':self.micro, 
                        'score':self.score}

# Define el objeto recorrido, que va a tener su reputación y sus buses

class recorrido():
    def __init__(self, code):
        self.code = code
        self.buses = []
        self.reputacion = 'Sin información'
        self.totalincidentes = 0

    def update_reputacion(self):
        self.totalincidentes = 0
        for bus in self.buses:
            self.totalincidentes += len(database['buses'][bus].incidentes)





# Recurso para registrar usuarios

class register(Resource):
    def post(self):
        data = request.form

        ## Segunda verificación de datos
        if data['nombre'] == ('' or None):
            return {'aceptado': False, 
                    'motivo': 'El nombre no puede estar vacío'}
        if data['apellidos'] == ('' or None):
            return {'aceptado': False, 
                    'motivo': 'El apellido no puede estar vacío'}
        if not '@' in list(data['email']):
            return {'aceptado': False, 
                    'motivo': 'El email debe ser válido'}
        if len(data['bip']) != 9 or data['bip'] in database['bips']:
            return {'aceptado': False, 
                    'motivo': 'El código bip que ingresó ya está registrado'}
        if data['rut'] in database['ruts']:
            return {'aceptado': False, 
                    'motivo': 'El rut que ingresó ya está registrado'}

        # Agrega un usuario a la base de datos
        database['ruts'][data['rut']] = user(data['nombre'], 
                                            data['apellidos'], data['email'],
                                            data['rut'], data['bip'], 
                                            data['password'])
        database['bips'].append(data['bip'])
        # Retorna aceptado a la aplicación
        return {'aceptado': True}


# Recurso para inicio de sesión
class login(Resource):
    def post(self):
        data = request.form
        # Comprueba que los datos coincidan con los presentes en la database
        if data['rut'] in database['ruts']:
            if data['password'] == database['ruts'][data['rut']].password:
                if database['ruts'][data['rut']].type != 'admin':
                    database['ruts'][data['rut']].update_data()
                return {'aceptado': True, 
                        'datos':database['ruts'][data['rut']].infodict}
            else:
                return {'aceptado':False, 
                        'mensaje': 
                        'La contraseña no coincide con el rut entregado'}
        else:
            return {'aceptado': False, 
                    'mensaje': 'El rut entregado no está registrado'}

        

# Recurso para revisar patentes
class patentcheck(Resource):
    def post(self):
        data = request.form
        # Confirma que la patente exista en la base de datos
        if data['patente'] in database['buses']:
            return {'aceptado': True}
        else:
            return {'aceptado': False, 
                    'mensaje': 'La patente entregada no está registrada'}

# Recurso para subir respuestas de encuestas al sistema
class surveyanswers(Resource):
    def post(self):
        data = request.form
        # Comprueba que los datos sean correctos
        if not data['rut'] in database['ruts']:
            return {'aceptado': False}
        if database['ruts'][data['rut']].password != data['password']:
            return {'aceptado': False}
        if not data['patente'] in database['buses']:
            return {'aceptado': False}
        patente = data['patente']
        conductor = database['ruts'][database['buses'][patente].conductor]
        
        print(data)

        # Revisa la lista entregada para asignar los puntos
        # correspondientes a cada pregunta
        for elemento in database['encuesta']:
            
            puntos = int(data[elemento])
            if elemento in conductor.score['puntajes']:
                
                conductor.score['puntajes'][elemento]['puntaje'] += puntos
                conductor.score['puntajes'][elemento]['respuestas'] += 1
            else:
                conductor.score['puntajes'][elemento]['puntaje'] = puntos
                conductor.score['puntajes'][elemento]['respuestas'] = 1


        print(conductor.score)
        return {'aceptado': True}

# Recurso para devolver información de informes
class reports(Resource):
    def post(self):
        data = request.form
        if data['rut'] in database['ruts']:
            if database['ruts'][data['rut']].type == 'admin':
                if database['ruts'][data['rut']].password == data['password']:
                    if data['action'] == 'user_report':
                        return {'aceptado': True, 
                        'datos':database['ruts'][data['rut']].get_user_info(data['driver'])}

                    else:
                        datos = database['ruts'][data['rut']].get_all_info()
                        return {'aceptado': True, 'datos':datos}
                else:
                    return {'aceptado': False}
            else:
                return {'aceptado': False}
        else:
            return {'aceptado': False}
                

api.add_resource(register, "/register")
api.add_resource(login, '/login')
api.add_resource(patentcheck, '/patentcheck')
api.add_resource(surveyanswers, '/survey')
api.add_resource(reports, '/reports')






##############################################

# Sección con datos artificiales para testeo

##############################################

# Agrega recorridos a la base de datos
for ruta in archivo_rutas:
    database['recorridos'][ruta[:-1]] = recorrido(ruta[:-1])

# Agrega buses a la base de datos
for micro in archivo_micros:
    patente, ruta = micro.split(',')
    if ruta[-1] == '\n':
        ruta = ruta[:-1]
    database['buses'][patente] = bus(patente, ruta)
    micros.append(patente)

# agrega conductores a la base de datos

for x in range(1962):
    datos = archivo_conductores.readline()
    datos = datos.split(',')
    nombre = datos[0]
    apellidos = [datos[1], datos[2]]
    rut = datos[3]
    email = datos[4]
    celular = datos[5]
    password = datos[6][:-1]

    database['ruts'][rut] = busdriver(nombre, apellidos, rut, email, celular, 
                                      password, micro=micros[x])


database['ruts']['20.946.887-5'] = admin('Ignacio', ['Lara', 'Vidal'],
                                        '20.946.887-5', 'Testeo123.')

# Corre la aplicación
if __name__ == '__main__':
    app.run(debug=True)
    