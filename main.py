# IMPORTAMOS LIBRERIAS
import pyxel    # Libreria grafica de 8bits 
import random   # Generador de nuemeros para los colores
import math     # Facilita el calculo mediante funciones
import time     # Libreria que calcula el tiempo respecto a la inicializacion del programa
import tabulate # Tabula los deatos obtenidos para mayor presentacion
import os       # Determina el sistema operativo para limpiar la cosola
import enum     # Libreria para estados
from keyboardController import KeyboardInput
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
        # INICIALIZAR VENTANA
        pyxel.init( width      = 192,              # Ancho de ventana
                    height     = 128,              # Altura de ventana
                    caption    = "ParabolicShot",  # Titulo de la ventana
                    fps        = 200,              # FPS del programa
                    fullscreen = True,            # Estado de pantalla inicial
                    scale      = 8)                # Eyscala de la ventana inicial
        self.game = False
        # INICIALIZACION DE VARIBALES
        self.listBalls = []                # Lista de objetos con proyectiles
        self.Triangulo = Pitagoras(10,120) # Cracion del triangulo respecto al vector 1 (X,Y)
        # INICIALIZACION DE NOMBRES DE COLUMNAS EN LA BD
        self.Data = [["a","V0 (m/s)","V0y (m/s)","V0x (m/s)","Ymax (m)","Ts (seg)","Tmax (seg)","Xmax (m)","Vf (m/s)","Vfy (m/s)"]]               
        self.target = Target(random.randint(10,40))
        pyxel.load("ScreensResources.pyxres")
        pyxel.mouse(True)
        self.scene = Scene()
        self.next = Bottom(155,100,15,10,11,"->",True)
        self.back = Bottom(20,100,15,10,11,"<-",True)
        self.mouse = MouseCheckLocation(1,1)
        self.menuLocation = -1 # Menu Principal
        
        self.inputUsermame = KeyboardInput()
        self.inputPass = KeyboardInput()
        self.squareInputUser = Bottom(30,50,40,10,7,"",False);
        self.squareInputPass = Bottom(30,75,40,10,7,"",False);
        pyxel.run(self.update,self.draw) # Asignamos los metodos de actualizacion para logica y dibujo
    #-----------------------------------------------------------------------------------------------------------------------------
    def update(self): # METODOD DE LOGICA
        if (self.game):
            pyxel.mouse(False)
            self.checkInput() # Comprueba la pulsacion de teclas
            self.Triangulo.update() #  Si esta en modo simulacion ejecuta el triangulo
            for ball in self.listBalls: # Iteramos en la lista de proyectiles
                ball.update()           # Actualizamos la posicion de los proyectiles
                self.target.checkColision(ball)
                if (self.target.clean):
                    self.target.clean = False
                    self.clearListBall()
        else:
            self.mouse.update()
            self.nextButtonState()
            self.backButtonState()
            if (self.menuLocation == -1): 
                self.squareInputUser.visible = True;
                self.squareInputPass.visible = True;
                self.inputUsermame.update()
                self.inputPass.update()
                self.squareInputUser.text = self.inputUsermame.storage;
                self.squareInputPass.text = self.inputPass.storage;
                if (self.mouse.IsColliding(self.squareInputUser)):
                    if (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
                        self.inputUsermame.active = True;
                        self.inputPass.active = False;
                if (self.mouse.IsColliding(self.squareInputPass)):
                    if (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
                        self.inputUsermame.active = False;
                        self.inputPass.active = True;    
                self.squareInputUser.update();
                self.squareInputPass.update();  
#-----------------------------------------------------------------------------------------------------------------------------
    def draw (self): # MEOTODO DE DIBUJO
        if (self.game):
            pyxel.cls(0)                # Color de fondo
            for ball in self.listBalls: # Iteramos en la lista de proyectiles
                ball.draw()             # Actualizamos posicion en pantalla
            self.Triangulo.draw()                 # Dibujar triangulo
            pyxel.text(5,5,"Angulo: "+str(self.Triangulo.A)+"°",7)    # Dibujamos angulo del triangulo
            pyxel.text(5,15,"Fuerza: "+str(self.Triangulo.h)+"m/s",7) # Dibujamos fuerza de disparo - hipotenusa
            self.target.draw()
        else:
            pyxel.cls(0)                # Color de fondo
            self.scene.draw()
            pyxel.text(8,3,"BallisticGames",9)
            if self.menuLocation == -1:
                pyxel.text(30,20,"Pantalla de login",10)
                pyxel.text(30,40,
                    "USUARIO\n"
                    +"\n"
                    +"\n"
                    +"\n"
                    +"CONTRASENIA\n"
                    +"\n"
                    +"\n",10)
                self.squareInputUser.draw();
                self.squareInputPass.draw();
            if self.menuLocation == 0:
                pyxel.text(30,20,"Menu principal",10)
                pyxel.text(30,40,
                    "- Descripcion\n"
                    +"- Objetivos\n"
                    +"- Introduccion\n"
                    +"- Areas academicas\n"
                    +"- Introduccion\n"
                    +"- Simulacion",10)
            if self.menuLocation == 1:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Descripcion",10)
                pyxel.text(20,40,"""
Desarrollar un prototipo que represente
el movimiento parabólico de un proyectil 
utilizando diferentes mecanismos para 
impulsarlo.
    """,10)
            if self.menuLocation == 2:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Descripcion",10)
                pyxel.text(20,40,"""
Se pretende en este proyecto que los
estudiantes simulen la situacion fisica
descrita anteriormente con la ayuda de 
un lenguaje de programación que le 
permita desarrollar sus habilidades, en 
el que dada unas condiciones iniciales 
tales como el angulo de salida y el 
    """,10)
            if self.menuLocation == 3:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Descripcion",10)
                pyxel.text(20,40,"""
alcance máximo, un objeto dibuje la 
trayectoria del tiro parabólico que 
realiza. 

Con el análisis de este movimiento 
se podrán obtener varios parámetros
como son: velocidad inicial de 
    """,10)
            if self.menuLocation == 4:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Descripcion",10)
                pyxel.text(20,40,"""
lanzamiento, altura máxima (distancia)
y el tiempo total de vuelo (t).
Además, se busca integrar relaciones
o modelos funcionales entre variables
e identificar y analizar propiedades 
físicas, químicas y matemáticas entre
variables.
    """,10)
            if self.menuLocation == 5:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Objetivo Ciencias Naturales",10)
                pyxel.text(20,40,"""
Relacionar grupos funcionales con las 
propiedades físicas y químicas de las 
sustancias. o Explicar reacciones 
químicas presentes en la vida diaria, 
considerando: Representación y la 
velocidad de las reacciones químicas 
y los factores que la afectan.
    """,10)
            if self.menuLocation == 6:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Objetivo Fisica",10)
                pyxel.text(20,40,"""
Identificar las fuerzas que actúan
sobre un cuerpo, aplicando las Leyes 
de Newton.
    """,10)
            if self.menuLocation == 7:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Objetivo Matematicas",10)
                pyxel.text(20,40,"""
Identificar y comprender conceptos de 
geometría analítica relacionados a la 
línea recta, para ser aplicados en el 
movimiento parabólico de un objeto
    """,10)
            if self.menuLocation == 8:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Objetivo Informatica",10)
                pyxel.text(20,40,"""
Conocer y aplicar la herramienta de 
App Inventor o Scratch en la solución
de problemas relacionados con los 
sistemas de información.
    """,10)
            if self.menuLocation == 9:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Introduccion",10)
                pyxel.text(20,40,"""
Con la barra espaciadora disparas
los proyectiles y regulas la 
velocidad y angulo con el mouse
    """,10)
            if self.menuLocation == 10:
                pyxel.text(8,3,"BallisticGames",9)
                pyxel.text(20,20,"Areas academicas",10)
                pyxel.text(20,40,"""
* Ciencias Naturales
* Fisica
* Matematicas
* Informatica
    """,10)
            self.next.draw()
            self.back.draw()
    def nextButtonState(self):
        if self.mouse.IsColliding(self.next):
            self.next.col = 7
            if (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
                
                if (self.menuLocation == -1):
                    if (self.inputPass.storage == "ADMIN" and self.inputUsermame.storage == "ADMIN"):
                        self.menuLocation = 0;
                    else:
                        print("error en login!! @$%^sfe@")
                else:
                    self.next.col = 3
                    if self.menuLocation<=10: self.menuLocation += 1 
                    if self.menuLocation==11: self.game = True
                    
                
        else:
            self.next.col = 11
    def backButtonState(self):
        if self.mouse.IsColliding(self.back):
            self.back.col = 7
            if (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
                self.back.col = 3
                if self.menuLocation>=0: self.menuLocation -=1
        else:
            self.back.col = 11
        
    #----------------------------------------------------------------------------------------------------------------------------
    def checkInput(self): # METODO COMPROBADOR DE ENTRADA DEL TECLADO
        if (pyxel.btnp(pyxel.KEY_SPACE)): self.generateBall()                                                      # Genera el proyectil
        if (pyxel.btnp(pyxel.KEY_R)): self.clearListBall() # R -> Resetear todo
    #----------------------------------------------------------------------------------------------------------------------------
    def generateBall(self): # METODO PARA GENERAR PROYECTIL
        # AGREGAR PROYECTIL A LA LISTA
        color = random.randint(1, 14) # Genera un color para el proyectil
        self.listBalls.append(Ball(10,120,2,color,self.Triangulo.A,self.Triangulo.h))           
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
class Scene:
    def __init__(self):
        self.tm = 0
        self.u = 0
        self.v = 0
        self.w = 24
        self.h = 16
        
    def draw(self):
        pyxel.bltm(0,0,self.tm,self.u,self.v,self.w,self.h,0)
        
class Bottom:
    def __init__(self,x,y,w,h,col,text,visible):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        self.text = text
        self.visible = visible
    def update (self):
        if ((len(self.text)+1)*pyxel.FONT_WIDTH > self.w):
            self.w = (len(self.text)+1)*pyxel.FONT_WIDTH;
    def draw(self):
        if self.visible:
            pyxel.rectb(self.x,self.y,self.w,self.h,self.col)
            pyxel.text(self.x+3,self.y+3,self.text,self.col)
            
class MouseCheckLocation:
    def __init__(self,w,h):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
        self.w = w
        self.h = h
    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
    def IsColliding(self, other):
        return self.x < other.x + other.w and \
            self.x + self.w > other.x and \
            self.y < other.y + other.h and \
            self.y + self.h > other.y

class Target():
    def __init__(self,r):
        self.r = r
        self.randomPosition()
        self.points = Points(0)
        self.clean = False
    def randomPosition(self):
        self.x = random.randint(0,pyxel.width)
        self.y = random.randint(0,pyxel.height-30)
        while (self.x < pyxel.width/2):
            self.x = random.randint(0,pyxel.width)
        self.r = random.randint(5,10)
    def checkColision(self,otherCicle):
        distancia = math.sqrt( (self.x - otherCicle.x)*(self.x - otherCicle.x) + (self.y - otherCicle.y)*(self.y - otherCicle.y) );
        if ( distancia < self.r + otherCicle.r ):
            self.points.updatePoints(10)
            self.randomPosition()
            self.clean = True
    def draw(self):
        self.col = 7
        for i in range(self.r):
            pyxel.circb(self.x,self.y,self.r-i,self.col)
            self.col = 14 if self.col == 7 else 7
        self.points.draw()
class Points():
    def __init__(self,initialPoints):
        self.points  = initialPoints
    def updatePoints(self,points):
        self.points += points
    def draw(self):
        pyxel.text((pyxel.width/2)-(pyxel.FONT_WIDTH*len("POINTS")/2),10,"POINTS",7)
        pyxel.text((pyxel.width/2)-(pyxel.FONT_WIDTH*len(str(self.points))/2),20,str(self.points),7)
        

App() # EJECUTAMOS PROGRAMA