from kivy.app import App 
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.texture import Texture
import requests
import cv2
from kivy.clock import Clock
from pyzbar.pyzbar import decode
import xlsxwriter

# PARÁMETROS PARA CONEXIÓN CON CÁMARA Y LA API

ip_droidcam = 'http://192.168.1.174:4747'
ip_camara = ip_droidcam + '/mjpegfeed'
ip_api = 'http://127.0.0.1:5000' # Esta es la dirección por defecto

####################################
# POR FAVOR LEER ARCHIVO README.md #
# POR FAVOR LEER ARCHIVO README.md #
# POR FAVOR LEER ARCHIVO README.md #
####################################


# Declara el objeto con información del usuario (Casi descontinuado)
class userdata():
    def __init__(self):
        self.nombre = None
        self.apellidos = []
        self.email = None
        self.rut = None
        self.bip = None
        self.password = None


# Clase de ventana, perteneciente a Kivy, correspondiente al inicio de sesión
class LoginScreen(Screen):

    # Objetos del archivo .kv 
    rut_input = ObjectProperty()
    password_input = ObjectProperty()
    rutlabel = ObjectProperty()
    passwordlabel = ObjectProperty() 
    errorlabel = ObjectProperty()

    # Función para iniciar sesión. 

    def rut_template(self):
        if len(self.rut.text) < 8 or len(self.rut.text) > 12:
            self.rutlabel.text = 'Ingrese un rut válido'
            return False

        if len(self.rut.text) == 9:
            if self.rut.text[2].isnumeric() == True:
                self.rut.text = self.rut.text[:2] + '.' + self.rut.text[2:]

            if self.rut.text[6].isnumeric() == True:
                self.rut.text = self.rut.text[:6] + '.' + self.rut.text[6:]
                
            if self.rut.text[10].isalnum() == True:
                self.rut.text = self.rut.text[:10] + '-' + self.rut.text[10]
            
            if self.rut.text[2] == '.' and self.rut.text[5] == '.' \
                                        and self.rut.text[8] == '-':
                self.rutlabel.text = 'Correcto'
                return True
            else: return False
        elif len(self.rut.text) == 8:
            if self.rut.text[1].isnumeric() == True:
                self.rut.text = self.rut.text[:1] + '.' + self.rut.text[1:]

            if self.rut.text[5].isnumeric() == True:
                self.rut.text = self.rut.text[:5] + '.' + self.rut.text[5:]
                
            if self.rut.text[9].isalnum() == True:
                self.rut.text = self.rut.text[:9] + '-' + self.rut.text[9]
            
            if self.rut.text[1] == '.' and self.rut.text[4] == '.' \
                                        and self.rut.text[7] == '-':
                self.rutlabel.text = 'Correcto'
                return True
            else: return False

    def login(self):

        # Comprueba que el rut sea válido
        self.rut_template()
        if self.rut_template() == False:
            return

        self.passwordlabel.text = ''

        # Manda solicitud a la web API para iniciar sesión
        self.response = requests.post(ip_api + '/login', 
                                      {'rut': self.rut.text, 
                                      'password':self.password_input.text})
        self.response = self.response.json()

        # En base a la respuesta de la wAPI, pasa a la siguiente 
        if self.response['aceptado']== False:
            self.errorlabel.text = self.response['mensaje']
        else:
            if self.response['datos']['type'] == 'conductor':
                self.manager.current = 'workermain'
            elif self.response['datos']['type'] == 'user':

                self.manager.get_screen('usermain').on_login(self.response) 
                self.manager.current = 'usermain'
            elif self.response['datos']['type'] == 'admin':
                self.manager.current = 'adminmain'
        

# Ventana para el registro de usuarios
class RegistrationScreen(Screen):
    # Objetos de utilidad para el registro y del archivo .kv
    usuario = userdata()
    pass_strength = {0:'Insegura', 1:'Débil', 2:'Moderada', 
                     3:'Fuerte', 4:'Muy fuerte'}
    rut = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    nombre = ObjectProperty(None)
    bip = ObjectProperty(None)
    apellidos = ObjectProperty(None)
    nombrelabel = ObjectProperty()
    apellidoslabel = ObjectProperty(None)
    emaillabel = ObjectProperty(None)
    rutlabel = ObjectProperty(None)
    passwordlabel = ObjectProperty(None)

    # Función para corregir el rut #### ARREGLAR SÓLO SIRVE CON RUT SUPERIOR A
    # 10 MILLONES


    def rut_template(self):
        if len(self.rut.text) < 8 or len(self.rut.text) > 12:
            self.rutlabel.text = 'Ingrese un rut válido'
            return False

        if len(self.rut.text) == 9:
            if self.rut.text[2].isnumeric() == True:
                self.rut.text = self.rut.text[:2] + '.' + self.rut.text[2:]

            if self.rut.text[6].isnumeric() == True:
                self.rut.text = self.rut.text[:6] + '.' + self.rut.text[6:]
                
            if self.rut.text[10].isalnum() == True:
                self.rut.text = self.rut.text[:10] + '-' + self.rut.text[10]
            
            if self.rut.text[2] == '.' and self.rut.text[5] == '.' \
                                        and self.rut.text[8] == '-':
                self.rutlabel.text = 'Correcto'
                return True
        elif len(self.rut.text) == 8:
            if self.rut.text[1].isnumeric() == True:
                self.rut.text = self.rut.text[:1] + '.' + self.rut.text[1:]

            if self.rut.text[5].isnumeric() == True:
                self.rut.text = self.rut.text[:5] + '.' + self.rut.text[5:]
                
            if self.rut.text[9].isalnum() == True:
                self.rut.text = self.rut.text[:9] + '-' + self.rut.text[9]
            
            if self.rut.text[1] == '.' and self.rut.text[4] == '.' \
                                        and self.rut.text[7] == '-':
                self.rutlabel.text = 'Correcto'
                return True

    # Verifica que el email sea válido conteniendo una @
    def email_validation(self):
        if self.email.text == '':
            self.emaillabel.text = 'Rellene esta casilla'
            return False
        if not '@' in list(self.email.text):
            self.emaillabel.text = 'Ingrese un email válido'
            return False
        else:
            self.emaillabel.text = 'Correcto'
            return True

    # Verifica la seguridad de la contraseña
    def password_check(self):
        self.password_score = 0
        if len(self.password.text) >= 8:
            if ('.' or '+' or '&' or '@' or '-' or '_' or '(' or ')' or '$') \
                in list(self.password.text):
                
                self.password_score +=1
            if self.password.text.islower() == False \
                and self.password.text.isupper() == False:
                
                self.password_score +=1
            if len(self.password.text) >= 12:
                self.password_score += 1
            if ('1' or '2' or '3' or '4' 
                or '5' or '6' or '7' or '8' 
                or '9' or '0') in list(self.password.text):
                self.password_score += 1
            self.passwordlabel.text = self.pass_strength[self.password_score]
        else:
            self.passwordlabel.text = 'Muy corta'
            return False

        if self.password_score >= 2:
            return True
        else:
            return False

    # Verifica que todos los datos sean correctos
    def data_check(self):
        valid = True
        if self.nombre.text == '':
            valid = False
            self.nombrelabel.text = 'Rellene esta casilla'
        else:
            self.nombrelabel.text = 'Correcto'

        if self.apellidos.text == '':
            valid = False
            self.apellidoslabel.text = 'Rellene esta casilla'
        else:
            self.apellidoslabel.text = 'Correcto'

        if self.email_validation() == False:
            valid = False
        if self.rut_template() == False:
            valid = False

        if self.bip.text == '':
            valid = False
            self.biplabel.text = 'Rellene esta casilla'
        if self.password_check() == False:
            valid = False

        # Si todos los datos son válidos, prosigue a enviar la solicitud
        # a la webAPI
        if valid == True:
            self.usuario.nombre = self.nombre.text.lower().capitalize()
            apellidos = self.apellidos.text.split()
            for x in range(len(apellidos)):
                self.usuario.apellidos.append(apellidos[x] 
                                              .lower().capitalize())

            self.usuario.email = self.email.text
            self.usuario.rut = self.rut.text
            self.usuario.bip = self.bip.text
            self.usuario.password = self.password.text
            # Datos para el registro
            solicitud_registro = {'nombre':self.usuario.nombre, 
                                 'apellidos':self.usuario.apellidos, 
                                 'email':self.usuario.email, 
                                 'rut': self.usuario.rut, 
                                 'bip':self.usuario.bip, 
                                 'password':self.usuario.password}

            # Solicitud para la api
            response = requests.post(ip_api + '/register',
                                    solicitud_registro)
            response = response.json()
            # Si la wAPI responde afirmativamente, redirige a la ventana
            # de inicio de sesión
            if response['aceptado'] == True:
                self.manager.current = 'login'


# Ventana principal del usuario
class UserMain(Screen):
    bienvenida = ObjectProperty(None)
    # Saluda al usuario que inició sesión usando su nombre
    def on_login(self, response):
        self.current_user = response['datos']

        self.bienvenida.text = 'Hola ' + self.current_user['nombre']


# Ventana para seleccionar la patente a calificar
class UserRatingQR(Screen):
    # key para ignorar los QR no correspondientes
    decryption_key = '0ymJIZkn4SP8Hx1iWlJZdYqzvFdTl7HUnCe8t9JU3WVnaHXrzxCwVqfqcQJWABHzcITAjzbjFHUS6Sn7eU/Ikw=='
    # Fuente de imagen, en este caso utiliza dirección IP de app para cámara
    capture = cv2.VideoCapture(ip_camara)
    fotoqr = ObjectProperty()
    previous = None
    # Función para buscar un código QR en la imagen de la cámara
    def search_qr(self, *args):   
        try:
            ret, frame = self.capture.read()
            for barcode in decode(frame):
                qr = barcode.data.decode('utf-8')
                qr = qr.split()
                for qr_check in qr:
                    if qr_check == self.decryption_key:
                        
                        self.check_patent(qr[1])
                        self.end_camera()
                        


            buffer = cv2.flip(frame, 0).tostring()
            textura = Texture.create(size=(frame.shape[1], frame.shape[0]), 
                                     colorfmt = 'bgr')
            textura.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.fotoqr.texture = textura
        # En caso de que falle la búsqueda de imagen (Por no conectarse
        # a ninguna cámara) apaga la cámara para evitar crasheos
        except:
            self.end_camera()
    # Función para iniciar la cámara en el ciclo interno de kivy
    def start_camera(self):
        self.camera = Clock.schedule_interval(self.search_qr, 1.0/30.0)

    # Función para sacar la cámara del ciclo interno de kivy
    def end_camera(self):
        Clock.unschedule(self.camera)
        self.capture.release()

    # Función para comprobar la validez de la patente
    def check_patent(self, patente):
        # Solicitud a la wAPI para ver si la patente existe
        response = requests.post(ip_api + '/patentcheck',
                                 {'patente':patente})
        response = response.json()
        # En caso de tener respuesta afirmativa, deja de buscar QR e inicia
        # la encuesta
        if response['aceptado'] == True:
            self.end_camera()
            self.manager.current = 'survey'
            self.manager.get_screen('survey').iniciar_encuesta(patente)
            
# Ventana para responder encuesta
class RatingScreen(Screen):
    pregunta1 = ObjectProperty(None)
    pregunta2 = ObjectProperty(None)
    pregunta3 = ObjectProperty(None)
    pregunta4 = ObjectProperty(None)
    pregunta5 = ObjectProperty(None)
    respuesta1 = ObjectProperty(None)
    respuesta2 = ObjectProperty(None)
    respuesta3 = ObjectProperty(None)
    respuesta4 = ObjectProperty(None)
    respuesta5 = ObjectProperty(None)

    # Función para iniciar la encuesta, con la micro para calificar,
    # y utilizando las preguntas obtenidas en el inicio de sesión
    def iniciar_encuesta(self, micro):
        self.micro = micro
        self.info =self.manager.get_screen('login').response['datos']
        self.preguntas = self.info['preguntas']
        self.pregunta1.text = self.preguntas[0]
        self.pregunta2.text = self.preguntas[1]
        self.pregunta3.text = self.preguntas[2]
        self.pregunta4.text = self.preguntas[3]
        self.pregunta5.text = self.preguntas[4]

    # Función para enviar las respuestas
    def enviar_encuesta(self):
        answer_list = []
        rut = self.info['rut']
        password = self.info['password']
        # Información para mandarle a la wAPI
        submit_info = {self.preguntas[0]:int(self.respuesta1.value),
                        self.preguntas[1]:int(self.respuesta2.value),
                        self.preguntas[2]:int(self.respuesta3.value),
                        self.preguntas[3]:int(self.respuesta4.value),
                        self.preguntas[4]:int(self.respuesta5.value),
                        'rut':rut, 
                        'password': password, 
                        'patente':self.micro,
                        'respuestas': answer_list}

        # Manda la solicitud
        response = requests.post(ip_api + '/survey', submit_info)
        response = response.json()

        # En caso de respuesta afirmativa, vuelve al menú inicial
        if response['aceptado'] == True:
            self.manager.current = 'usermain'
            self.manager.get_screen('ratingqr').capture = cv2.VideoCapture(ip_camara)

# Ventana del trabajador
class WorkerMain(Screen):

    # Variables utilizadas
    contador_hora = ObjectProperty(None)
    boton_contador = ObjectProperty(None)
    tiempo = 0
    contando = False

    # Función para contar el tiempo transcurrido
    def contador_tiempo(self, dt):
        self.tiempo += 1
        hora = str(self.tiempo//3600)
        if self.tiempo//3600 <= 9:
            hora = '0' + str(self.tiempo//3600)
        minutos = str(self.tiempo//60)
        if self.tiempo//60 <= 9:
            minutos = '0' + str(self.tiempo//60)
        segundero = str(self.tiempo % 60)
        if self.tiempo % 60 <= 9:
            segundero = '0' + str(self.tiempo % 60)

        self.hora = f'{hora}:{minutos}:{segundero}'


        self.contador_hora.text = self.hora

    # Función para actualizar el botón y activar el conteo
    # de tiempo
    def boton(self):
        if self.contando == False:
            self.contador = Clock.schedule_interval(self.contador_tiempo, 1.0)
            self.contando = True
            self.boton_contador.text = 'Pausar trabajo'

        else:
            Clock.unschedule(self.contador)
            self.contando = False
            self.boton_contador.text = 'Reanudar trabajo'




class AdministratorMain(Screen):
    # Función para generar informes
    def report(self):
        # Solicitud de información a la API
        usuario = self.manager.get_screen('login').response['datos']
        solicitud_informe = {'rut': usuario['rut'], 
                            'password': usuario['password'],
                            'action': 'general_report'}

        # Solicitud para la api
        response = requests.post(ip_api + '/reports',
                                solicitud_informe)
        response = response.json()
        # Si la wAPI responde afirmativamente, comienza
        # a crear el archivo excel
        if response['aceptado'] == True:
            drivers_data = response['datos']

            drivers_data_list = []
            info_columnas = ['Rut', 'Nombre', 'Apellidos', 
                            'Correo electrónico', 'Promedio']

            # Crea una lista con la información de
            # todos los conductores para ser
            # colocada en las columnas
            for conductor in drivers_data:
                conductor = drivers_data[conductor]
                temp_list = []
                temp_list.append(conductor['rut'])
                temp_list.append(conductor['nombre'])
                apellidos = ''
                for apellido in conductor['apellidos']:
                    apellidos += apellido + ' '
                temp_list.append(apellidos[:-1])
                temp_list.append(conductor['email'])
                if conductor['score']['promedio'] == None:
                    temp_list.append('Sin información')

                else:
                    temp_list.append(conductor['score']['promedio'])
                drivers_data_list.append(temp_list)

            # Crea el archivo excel y lo configura
            workbook = xlsxwriter.Workbook('Informe General.xlsx')
            worksheet = workbook.add_worksheet()
            worksheet.set_column(0, 0, 12)
            worksheet.set_column(1, 1, 15)
            worksheet.set_column(2, 2, 40)
            worksheet.set_column(3, 3, 60)
            worksheet.set_column(4, 4, 8)

            columna = 0
            fila = 0
            # Escribe la información en el archivo excel
            for item in info_columnas:
                worksheet.write(fila, columna, item)
                columna += 1

            fila += 1
            columna = 0

            for conductor in drivers_data_list:
                for categoria in conductor:
                    worksheet.write(fila, columna, categoria)
                    columna += 1
                columna = 0

                fila += 1

            # Cierra el archivo excel
            workbook.close()

# Ventanas sin utilizar
class WorkerSurveyCheck(Screen):
    pass
class UserReport(Screen):
    pass



# Ventana sin utilizar, easteregg de gatitos temporalmente
class Transpuntos(Screen):
    catito = ObjectProperty(None)
    image = None
    def get_cat_image(self):
        headers = {'x-api-key':'7b0b9b09-ac95-4cd1-91cd-f4fed056d066'}
        response = requests.get(url=
                                'https://api.thecatapi.com/v1/images/search?',
                                 headers=headers)
        response = response.json()
        self.catito.source = response[0]['url']
    



# Construcción de la aplicación a través de Screen Manager
class KivyApp(App):
    def build(self):
        self.sm = ScreenManager()
        
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(Transpuntos(name='lol'))
        self.sm.add_widget(RegistrationScreen(name='register'))
        self.sm.add_widget(UserMain(name='usermain'))
        self.sm.add_widget(UserRatingQR(name='ratingqr'))
        self.sm.add_widget(RatingScreen(name='survey'))
        self.sm.add_widget(WorkerMain(name='workermain'))
        self.sm.add_widget(AdministratorMain(name='adminmain'))
        
        return self.sm
    

# Corre la aplicación
if __name__ == '__main__':

    KivyApp().run()
