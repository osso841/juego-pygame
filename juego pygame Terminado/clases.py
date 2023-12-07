import pygame
from funciones import obtener_superficie_desde_spritesheet
import sqlite3

#CLASES JUEGO


class Rectangulo:
    def __init__(self, x, y, dim_x, dim_y, color):
        self.Rect = pygame.Rect(x, y, dim_x, dim_y)
        self.surface = pygame.Surface((dim_x, dim_y))
        self.surface.fill(color)
        self.posicion_x = x
        self.posicion_y = y
        self.dimencion_x = dim_x
        self.dimencion_y = dim_y

        self.aux_x = x 

    def modificar_posicion_rect(self, posicion_x = 0):
        self.Rect = pygame.Rect(self.posicion_x + posicion_x, self.posicion_y, self.dimencion_x, self.dimencion_y)


    def dibujar(self, screen, posicion_x = 0):
        screen.blit(self.surface, (self.posicion_x + posicion_x, self.posicion_y))


class Personaje(Rectangulo):
    def __init__(self, x, y , dim_x, dim_y, color, path, columnas, escala_x, escala_y):
        super().__init__(x, y, dim_x, dim_y, color)

        self.caminar = obtener_superficie_desde_spritesheet(path, columnas, escala_x, escala_y)
        self.posicion = 0
        self.animacion = self.caminar
        self.imagen = self.caminar[self.posicion]


    def actualizar(self):
        if self.posicion < len(self.animacion)-1:
            self.posicion += 1
        else:
            self.posicion = 0

        self.imagen = self.animacion[self.posicion]


    def detener_personaje(self, path, escala_x, escala_y):
        self.imagen = pygame.image.load(path)
        self.imagen = pygame.transform.scale(self.imagen, (escala_x, escala_y))


    def cambiar_imagen(self, path, columnas, escala_x, escala_y):
        self.caminar =  obtener_superficie_desde_spritesheet(path, columnas, escala_x, escala_y)
        self.animacion = self.caminar
        self.imagen = self.caminar[self.posicion]

    def mostrar_personaje(self, screen:pygame.Surface, centrar_y = 0, posicion_x=None):
        if posicion_x is None:
            screen.blit(self.imagen, (self.posicion_x - 50, self.posicion_y - 30 -centrar_y))
        else:
            screen.blit(self.imagen, (self.posicion_x + posicion_x - 50, self.posicion_y - 30 - centrar_y))

        
class Imagen:
    def __init__(self, path, x, y, scale_x, scale_y):
        self.fondo = pygame.image.load(path)
        self.fondo_escala = pygame.transform.scale(self.fondo, (scale_x, scale_y))
        self.dimension_x = scale_x
        self.posicion_x = x
        self.posicion_y = y


    def dibujar(self, screen:pygame.Surface, posicion_x = None):
        if posicion_x is None:
            screen.blit(self.fondo_escala, (self.posicion_x, self.posicion_y))
        else:
            screen.blit(self.fondo_escala, (posicion_x, self.posicion_y))


#CLASES MENU


class ScoreDB():

    def crear_DB(self):
        with sqlite3.connect("registros.db") as conexion:
            try:
                sentencia = ''' CREATE TABLE score
                                (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    usuario TEXT,
                                    correctas INTEGER,
                                    incorrectas INTEGER,
                                    vidas INTEGER
                                )
                            '''
                conexion.execute(sentencia)
                conexion.commit()
            except sqlite3.OperationalError:
                print("la tabla score ya existe")


    def insertar_registro(self, usuario, correctas, incorrectas, vidas):
        with sqlite3.connect("registros.db") as conexion:
            try:
                sentencia = " INSERT INTO score(usuario, correctas, incorrectas, vidas) VALUES (?,?,?,?)"
                conexion.execute(sentencia, (usuario, correctas, incorrectas, vidas))
                conexion.commit()
            except:
                print("error")


    def seleccionar_registros(self): #devuelve los registros en formato list[tuple]
        with sqlite3.connect("registros.db") as conexion:
            cursor = conexion.execute("SELECT usuario, correctas, incorrectas, vidas FROM score ORDER BY correctas DESC LIMIT 5")
            registros = cursor.fetchall()
            return registros
        

class Menu():
    def __init__(self, x, y, dimx, dimy, path) -> None:
       self.imagen = pygame.image.load(path)
       self.fondo = pygame.transform.scale(self.imagen, (dimx, dimy))
       self.posicion_x = x
       self.posicion_y = y

       
    def mostrar_menu(self, screen:pygame.Surface):
        screen.blit(self.fondo, (self.posicion_x, self.posicion_y))


class Opciones():
    def __init__(self, x, y, path) -> None:
        self.imagen = pygame.image.load(path)
        self.rect_boton = pygame.Rect(x, y, self.imagen.get_width() ,self.imagen.get_height())
        self.posicion_x = x
        self.posicion_y = y

    def mostrar_opciones(self, screen:pygame.Surface):
        screen.blit(self.imagen, (self.posicion_x, self.posicion_y))






