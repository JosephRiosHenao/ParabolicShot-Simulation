# IMPORTAMOS LIBRERIAS
import pyxel    # Libreria grafica de 8bits 
import random   # Generador de nuemeros para los colores
import math     # Facilita el calculo mediante funciones
import time     # Libreria que calcula el tiempo respecto a la inicializacion del programa
import tabulate # Tabula los deatos obtenidos para mayor presentacion
import os       # Determina el sistema operativo para limpiar la cosola
import enum     # Libreria para estados
#---------------------------------------------------------------------------------------------------------------------------------
class TypeSimulator(enum.Enum): # CLASE QUE PERMITE DETERMINAR EL ESTADO DE EJECUCION
    Simulator     = 0 # Estado de simulacion normal
    SimulatorData = 1 # Estado de simulacion mediante entrada en teclado con distancia y angulo
#---------------------------------------------------------------------------------------------------------------------------------
G = 9.81 # Constante de gravedad
#---------------------------------------------------------------------------------------------------------------------------------
class Pixel(): # CLASE QUE ESTABLECE LOS PIXELES DE LA TRAYECTORIA
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self,x,y,col): # CONSTRUCTOR DEL OBJETO, POSICION Y COLOR
        # INICIALIZANDO VARIABLES DE NUESTRO OBJETO
        self.x   = x   # X ubicacion
        self.y   = y   # Y ubicacion
        self.col = col # Color
    #-----------------------------------------------------------------------------------------------------------------------------
    def draw(self): # METODO QUE DIBUJA EL PIXEL
        pyxel.pset(self.x,self.y,self.col) # Dibuja el pixel respecto a su ubicacion y color de creacion
#---------------------------------------------------------------------------------------------------------------------------------
class BallMathV():
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self,x,y,r,col,a,xMax,tTotal): # CONSTRUCTOR DEL OBJETO DE PELOTA RESPECTO A DATOS INSUFICIENTES
        # INICIALIZANDO VARIABLES DE NUESTRO OBJETO
        self.x    = x        # X ubicacion 
        self.xi   = x        # X ubicancion para determinar posicion incial
        self.y    = y        # Y ubicacion 
        self.yi   = y        # Y ubicacion para determinar altura inicial
        self.a    = a        # Angulo
        self.xMax = xMax     # Distancia total recorrida
        self.t    = 0        # Restablecemos tiempo
        self.r    = r        # Radio
        self.col  = col      # Color
        self.tTotal = tTotal # Tiempo total de vuelo
        # INICIALIZANDO OTROS FACTORES INDEPENDIENTES
        self.listPixel      = []                     # Lista de objetos que almacena el recorrido de la trayectoria
        self.starting_point = time.time()            # Calcula el tiempo respecto a la inicializacion del objeto
        self.dif            = pyxel.height - self.yi # Calcula la diferencia del objeto respecto al suelo
        # CALCULAMOS DATOS
        # Velocidad Inicial = hipotenusa o Fuerza lanzamiento respuesta a problema
        self.vi = round((G*self.tTotal)/(2*math.sin(math.radians(self.a))),2)
        # DATOS COMPLEMENTARIOS
        self.viY    = round( math.sin(math.radians(self.a))*self.vi,2 ) # Velocidad Inicial Y - Componente rectangular Y
        self.vX     = round( math.cos(math.radians(self.a))*self.vi,2 ) # Velocidad vector X constante - Componente rectangular X
        self.ts     = round( self.tTotal/2,2 )                          # Tiempo de subida al punto mas alto
        self.yMax   = round( math.pow(self.viY,2)/(2*(G)),2 )           # Altura maxima alcanzada
        self.xTotal = round( self.vX*self.tTotal,2 )                    # Despazamiento en X total
        self.vFy    = round( self.viY-G*self.tTotal,2 )                 # Velocidad final Y - Componente rectangular Y
        self.vF     = round( math.sqrt(math.pow(self.vX,2)+math.pow(self.vFy,2)),2 ) # Velocidad final
    #-----------------------------------------------------------------------------------------------------------------------------
    def update(self): # METODO UPDATE QUE ACTUALIZA LA POSICION RESPECTO AL TIEMPO
        if self.t <= self.tTotal: # CALCULAMOS SI PUEDE CALCULAR MAS TIEMPO, SIMULA LA GRAVEDAD EN FUNCION DEL TIEMPO
            self.elapsed_time = round(time.time()-self.starting_point,2) # Diferencia del tiempo actual con el de inicio
            self.t            = self.elapsed_time                        # Determinamos tiempo actual desde la creacion del balon
            # CALCULAMOS DESPLAZAMIENTO CON RELACION AL TIEMPO
            self.x = self.xi+self.vX*self.t                                                   # Calculando posixion en eje X
            self.y = (self.viY*self.t+(-1/2*G)*math.pow(self.t,2))*-1+(pyxel.height-self.dif) # Calucalndo posicion en eje Y
            # TRAYECTORIA
            self.listPixel.append(Pixel(self.x,self.y,self.col)) # Añade a la lista de objetos la posicion actual de trayectoria
    #-----------------------------------------------------------------------------------------------------------------------------
    def draw(self): # METODO DE DIBUJO DE PROYECTIL Y TRAYECTORIA
        pyxel.circ(self.x,self.y,self.r,self.col) # Dibujando proyectil respecto a la posicion calculada
        for pixel in self.listPixel:              # Iteramos sobre los objetos de la trayectoria    
            pixel.draw()                          # Dibujamos objeto en pantalla
#---------------------------------------------------------------------------------------------------------------------------------        
class Ball(): # CLASE PROYECTIL CON RESPECTO A VELOCIDAD INICIAL Y ANGULO
    #-----------------------------------------------------------------------------------------------------------------------------
    def __init__(self,x,y,r,col,a,vi): # CONSTRUCTOR, POSICION, TAMAÑO, COLOR, ANGULO Y VELOCIDAD INICAL
        # INICIALIZAMOS DATOS DE CLASE
        self.x   = x   # X ubicacion
        self.xi  = x   # X ubicancion para determinar posicion incial
        self.y   = y   # Y ubicacion
        self.yi  = y   # Y ubicacion para determinar altura inicial
        self.a   = a   # Angulo
        self.vi  = vi  # Velocidad Inicial = hipotenusa - Fuerza lanzamiento
        self.t   = 0   # Determinamos tiempo de creacion como 0
        self.r   = r   # Radio del proyectil
        self.col = col # Color
        # DATOS COMPLEMENTARIO
        self.starting_point = time.time()            # Tiempo de creacion para tomar referencia desde la creacion del programa
        self.dif            = pyxel.height - self.yi # Diferencia respecto al suelo 
        self.listPixel      = []                     # Lista de objetos que almacena la trayectoria
        # CALCULANDO DATOS
        self.viY    = round( (math.sin(math.radians(self.a)))*self.vi,2 ) # Velocidad Inicial Y
        self.vX     = round( (math.cos(math.radians(self.a)))*self.vi,2 ) # Velocidad vector X constante
        self.ts     = round( self.viY/G,2 )                               # Tiempo de subida al punto mas alto
        self.yMax   = round( math.pow(self.viY,2)/(2*(G)),2 )             # Altura maxima alcanzada
        self.tTotal = round( 2*self.ts,2 )                                # Tiempo total de vuelo 
        self.xTotal = round( self.vX*self.tTotal,2 )                      # Despazamiento en X total
        self.vFy    = round( self.viY-G*self.tTotal,2 )                   # Velocidad final Y - Componente rectangular Y
        self.vF     = round( math.sqrt(math.pow(self.vX,2)+math.pow(self.vFy,2)),2 ) # Velocidad final
    #---------------------------------------------------------------------------------------------------------------------------- 
    def update(self): # METODO UPDATE QUE ACTUALIZA LA POSICION
        if self.t <= self.tTotal: # DETERMINA SI ES POSIBLE SEGUIR MOVIENDOLA SIN PASARSE DEL TIEMPO
            # CALCULAMOS TIEMPO
            self.elapsed_time = round(time.time ()-self.starting_point,2) # Difrencia del tiempo actual con el de incio
            self.t            = self.elapsed_time                         # Tiempo desde que se creo el objeto
            # CALCULAMOS POSICION
            self.x = self.xi+self.vX*self.t                                                   # Determinamos la posicion X  
            self.y = (self.viY*self.t+(-1/2)*G*math.pow(self.t,2))*-1+(pyxel.height-self.dif) # Determinamos la posicion Y
            # TRAYECTORIA
            self.listPixel.append(Pixel(self.x,self.y,self.col)) # Almacenamos psicion actual en la trayectoria
    #---------------------------------------------------------------------------------------------------------------------------
    def draw(self): # METODO DRAW DIBUJA LA POSICION Y TRAYECTORIA ALMACENADA
        pyxel.circ(self.x,self.y,self.r,self.col) # Dibuja la posicion actual del proyectil
        for pixel in self.listPixel:              # Itera en la lista de objetos de la trayectoria
            pixel.draw()                          # Dibuja el objeto de la lista de proyectil iterado
#--------------------------------------------------------------------------------------------------------------------------------
class Pitagoras(): # CLASE PARA DETERMINAR POSICION RESPECTO A 2 VECTORES, SIENDO UNO DE ELLOS EL MOUSE
    def __init__(self,Ax,Ay): # CONSTRUCTOR DEL OBJETO, POSICION DEL OBJECTO DEL PRIMER VECTOR
        # INICIALIZAMOS DATOS
        # LADOS DEL TRIANGULO
        self.ca = 0 # Adyaciente
        self.co = 0 # Opuesto
        self.h  = 0 # Hipotenusa
        # ANGULO DE TIRO
        self.A = 0 # AnguloHallar
        # POSICION DEL VECTOR 1
        self.Ax = Ax # X Objeto
        self.Ay = Ay # Y Objeto
        # POSICION DEL VECTOR 2
        self.Bx = 0 # X Superior
        self.By = 0 # Y Superor
        # ESTADOS DEL LOS LADOS DEL TRIANGULO A LA VISTA
        self.stateUP   = True # Visibilidad de la hipotenusa 
        self.stateDOWN = True # Visibilidad de la opuesta
        self.stateLEFT = True # Visibilidad de la adyacente
    #-----------------------------------------------------------------------------------------------------------------------------
    def update(self): # METODO UPDATE PARA DETERMINAR VALORES DEL TRIANGULO
        # ACTUALIZAMOS POSICION DEL VECTOR 2
        self.Bx = pyxel.mouse_x # Capturando Posicion MouseX
        self.By = pyxel.mouse_y # Capturando Posicion MouseY
        # CALCULAMOS LADOS DEL TRIANGULO
        self.ca = self.Bx-self.Ax                                                 # Hallar tamaño de cateto adyaciente
        self.co = self.Ay-self.By                                                 # Hallar tamaño de cateto opuesto
        self.h  = round(math.sqrt(math.pow(self.ca, 2) + math.pow(self.co, 2)),2) # Hallar hipotenusa
        # CALCULAMOS ANGULO A HALLAR CON UNA EXEPCION DE ERRORES PARA EL GRADO DE 90°
        try:                                                             # COMPROBAMOS POSIBLIDAD
            self.A = round(math.degrees(math.atan((self.co/self.ca))),2) # Calculamos angulo con razones trigonometricas tan(a)
        except ZeroDivisionError as e:                                   # EN CAOS DE ERROR
            self.A = 90.00                                               # El cateto adyacente es 0, por ende angulo es 90°
        # COMPROBAMOS EL ESTADO DEL TRIANGULO, SEGUN EL TECLADO
        if (pyxel.btnp(pyxel.KEY_UP)):   self.stateUP   = not(self.stateUP)   # Flecha arriba cambiamos estado hipotenusa
        if (pyxel.btnp(pyxel.KEY_LEFT)): self.stateLEFT = not(self.stateLEFT) # Flecha iaquierda cambiamos estado adyacente
        if (pyxel.btnp(pyxel.KEY_DOWN)): self.stateDOWN = not(self.stateDOWN) # Flecha abajo cambiamos estado de opuesto
    #----------------------------------------------------------------------------------------------------------------------------
    def draw(self): # METODO QUE DIBUJA EL TRIANGULO
        if self.stateUP:   pyxel.line(self.Ax,self.Ay,self.Bx,self.By,15) # Dibuja hipotenusa
        if self.stateLEFT: pyxel.line(self.Ax,self.Ay,self.Bx,self.Ay,14) # Dibuja adyacente
        if self.stateDOWN: pyxel.line(self.Bx,self.Ay,self.Bx,self.By,13) # Dibuja opuesto
#--------------------------------------------------------------------------------------------------------------------------------
class App(): # CLASE PRINCIPAL DEL PROGRAMA
    def __init__(self): # INICIALIZACION
        # INICIALIZACION DE ESTADO
        self.clearConsole()                                        # Borramos consola
        inputState = input("Desea usar el simulador? y/n:  ")      # Preguntamos estado
        if inputState == "y": self.state = TypeSimulator.Simulator # Asignamos estado de simulacion
        else: self.state = TypeSimulator.SimulatorData             # Asignamos estado de simulacion mediante datos
        # INICIALIZAR VENTANA
        pyxel.init( width      = 192,              # Ancho de ventana
                    height     = 128,              # Altura de ventana
                    caption    = "ParabolicShot",  # Titulo de la ventana
                    fps        = 200,              # FPS del programa
                    fullscreen = False,            # Estado de pantalla inicial
                    scale      = 4)                # Eyscala de la ventana inicial
        # INICIALIZACION DE VARIBALES
        self.listBalls = []                # Lista de objetos con proyectiles
        self.Triangulo = Pitagoras(10,120) # Cracion del triangulo respecto al vector 1 (X,Y)
        # INICIALIZACION DE NOMBRES DE COLUMNAS EN LA BD
        self.Data = [["a","V0 (m/s)","V0y (m/s)","V0x (m/s)","Ymax (m)","Ts (seg)","Tmax (seg)","Xmax (m)","Vf (m/s)","Vfy (m/s)"]]               
        pyxel.run(self.update,self.draw) # Asignamos los metodos de actualizacion para logica y dibujo
    #-----------------------------------------------------------------------------------------------------------------------------
    def update(self): # METODOD DE LOGICA
        self.checkInput() # Comprueba la pulsacion de teclas
        if self.state == TypeSimulator.Simulator: self.Triangulo.update() # Si esta en modo simulacion ejecuta el triangulo
        for ball in self.listBalls: # Iteramos en la lista de proyectiles
            ball.update()           # Actualizamos la posicion de los proyectiles
    #-----------------------------------------------------------------------------------------------------------------------------
    def draw (self): # MEOTODO DE DIBUJO
        pyxel.cls(0)                # Color de fondo
        for ball in self.listBalls: # Iteramos en la lista de proyectiles
            ball.draw()             # Actualizamos posicion en pantalla
        if self.state == TypeSimulator.Simulator: # Comprobamos el estado en simulacion
            self.Triangulo.draw()                 # Dibujar triangulo
            pyxel.text(5,5,"Angulo: "+str(self.Triangulo.A)+"°",15)    # Dibujamos angulo del triangulo
            pyxel.text(5,10,"Fuerza: "+str(self.Triangulo.h)+"m/s",15) # Dibujamos fuerza de disparo - hipotenusa
    #----------------------------------------------------------------------------------------------------------------------------
    def checkInput(self): # METODO COMPROBADOR DE ENTRADA DEL TECLADO
        if (pyxel.btnp(pyxel.KEY_SPACE)): # Comprobacion de tecla espacio
            if self.state == TypeSimulator.SimulatorData: # Si esta en modo simulacion con entrada
                self.clearConsole()                       # Ejecutamos el metodo para borrar consola
                self.aInput = float(input("Digite el angulo de disparo: "))          # Pregunta angulo
                self.XmaxInput = float(input("Digite la distancia(m): "))            # Pregunta distancia
                self.tTotalInput = float(input("Digite el tiempo total de vuelo: ")) # Pregunta tiempo de vuelo
            self.generateBall()                                                      # Genera el proyectil
        if (pyxel.btnp(pyxel.KEY_R)): self.clearListBall() # R -> Resetear todo
    #----------------------------------------------------------------------------------------------------------------------------
    def generateBall(self): # METODO PARA GENERAR PROYECTIL
        # AGREGAR PROYECTIL A LA LISTA
        color = random.randint(1, 14) # Genera un color para el proyectil
        if self.state == TypeSimulator.Simulator: # Compreuba estado de simulacion
            self.listBalls.append(Ball(10,120,2,color,self.Triangulo.A,self.Triangulo.h))           
        else:                                     # Si no es segun la entrada del teclado
            self.listBalls.append(BallMathV(10,120,2,color,self.aInput,self.XmaxInput,self.tTotalInput))
        # AGREGA DATOS A LA BASE DE DATOS
        if len(self.listBalls)==0: # Comprueba la longitud de la lista
            self.Data.append([self.listBalls[0].a,self.listBalls[0].vi,self.listBalls[0].viY,self.listBalls[0].vX,
                            self.listBalls[0].yMax,self.listBalls[0].ts,self.listBalls[0].tTotal,
                            self.listBalls[0].xTotal,self.listBalls[0].vF,self.listBalls[0].vFy]) 
        else:                      # Si no entonces agrega el ultimo dato agregado
            self.Data.append([self.listBalls[-1].a,self.listBalls[-1].vi,self.listBalls[-1].viY,self.listBalls[-1].vX,
                            self.listBalls[-1].yMax,self.listBalls[-1].ts,self.listBalls[-1].tTotal,
                            self.listBalls[-1].xTotal,self.listBalls[-1].vF,self.listBalls[-1].vFy])
        # IMPRIMIR BASE DE DATO
        self.clearConsole() # Borra consola y la imprime
        print(tabulate.tabulate(self.Data,headers="firstrow",showindex=True,tablefmt="fancy_grid",numalign="center"))
    #----------------------------------------------------------------------------------------------------------------------------
    def clearListBall(self): # METODO, REINICIA LA BD, LISTAS Y PANATALLA
        self.listBalls.clear() # Limpia la lista de proyectiles
        self.Data.clear()      # Limpia la base de datos
        self.clearConsole()    # Limpia consola y agrega nombres a las columnas e imprime
        self.Data = [["a","V0 (m/s)","V0y (m/s)","V0x (m/s)","Ymax (m)","Ts (seg)","Tmax (seg)","Xmax (m)","Vf (m/s)","Vfy (m/s)"]]
        print(tabulate.tabulate(self.Data,headers="firstrow",showindex=True,tablefmt="fancy_grid",numalign="center"))
    #----------------------------------------------------------------------------------------------------------------------------
    def clearConsole(self):    # METODO DE LIMPIAR CONSOLA
        if os.name == "nt":    # Comprueba el tipo de sistema operativo
            os.system("cls")   # Limpia con comando cls
        else:                  # Si no 
            os.system("clear") # Limpia con comando clear
#--------------------------------------------------------------------------------------------------------------------------------
App() # EJECUTAMOS PROGRAMA