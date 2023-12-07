import pygame
from pygame.locals import K_SPACE

def obtener_superficie_desde_spritesheet(path, columnas, escala_x, escala_y) ->list[pygame.Surface]:
    """ Carga una hoja de sprites desde un archivo, escala la imagen y devuelve una lista de superficies
        correspondientes a cada fotograma.

        param:
            path (str): La ruta al archivo de la hoja de sprites.
            columnas (int): El número de columnas en la hoja de sprites.
            escala_x (int): La dimensión de escala horizontal para la imagen.
            escala_y (int): La dimensión de escala vertical para la imagen.

        return:
            Una lista de pygame.Surface, donde cada superficie representa un fotograma de la hoja de sprites.
    """
    lista = []
    superficie_imagen = pygame.image.load(path)
    superficie_imagen = pygame.transform.scale(superficie_imagen, (escala_x, escala_y))
    fotograma_ancho = int(superficie_imagen.get_width()/columnas)
    fotograma_alto = int(superficie_imagen.get_height())

    for columna in range(columnas):
        x = fotograma_ancho * columna
        superficie_fotograma = superficie_imagen.subsurface(x, 0, fotograma_ancho, fotograma_alto)
        lista.append(superficie_fotograma)

    return lista


def mover_izquierda_personaje(movimiento:int, personaje:object) ->int: #movimiento izquierda personaje principal
    """Mueve el personaje hacia la izquierda y actualiza su animación.

    param:
        movimiento (int): La posición actual del personaje en el eje horizontal.
        personaje (object): Instancia del objeto que representa al personaje.

    return:
        Un entero que representa la nueva posición del personaje después de moverlo hacia la izquierda.
    """
    movimiento += 10
    personaje.actualizar() #actualiza la animacion
    personaje.cambiar_imagen('imagenes\\personaje izquierda.png', 6, 750, 150)
    return movimiento


def mover_derecha_personaje(movimiento:int, personaje:object) ->int: #movimiento derecho personaje principal
    """
    Mueve el personaje hacia la derecha y actualiza su animación.

    param:
        movimiento (int): La posición actual del personaje en el eje horizontal.
        personaje (object): Instancia del objeto que representa al personaje.

    return:
        Un entero que representa la nueva posición del personaje después de moverlo hacia la derecha.
    """
    movimiento -= 10
    personaje.actualizar() #actualiza la animacion
    personaje.cambiar_imagen('imagenes\\personaje derecha.png', 6, 750, 150)
    return movimiento


def colocar_personaje_estatico(posicion:bool, personaje:object) -> None: #personaje estatico derecho e izquierdo
    """Coloca al personaje en una posición estática.

    param:
        posicion (bool): Indica la posición del personaje. False para la izquierda, True para la derecha.
        personaje (object): Instancia del objeto que representa al personaje.
    """
    if not posicion:
        personaje.detener_personaje('imagenes\\estatica izquierda.png', 93, 144)
    else:
        personaje.detener_personaje('imagenes\\estatica derecha.png', 93, 144)


def verificar_evento_QUIT(event:pygame.event.Event) -> bool: #asignar evento QUIT
    """Verifica si se ha recibido el evento QUIT.

    param:
        event (pygame.event.Event): Objeto de evento de pygame.

    return:
        bool: True si el evento es QUIT, False de lo contrario.
    """
    continuar = True
    if event.type == pygame.QUIT:
        continuar = False
    return continuar


def verificar_evento_KEYDOWN(event:pygame.event.Event, lista_key:list, ingreso:str) -> tuple: #verifica el ingreso al menu y palabras de juego
    """Verifica si se ha presionado una tecla y maneja el ingreso al menú y las palabras del juego.

    param:
        event (pygame.event.Event): Objeto de evento de pygame.
        lista_key (list): Lista de teclas permitidas.
        ingreso (str): Cadena que almacena el ingreso del usuario.

    return:
        tuple[bool, str]: Una tupla donde el primer elemento indica si se debe ingresar al menú y el segundo elemento es la cadena actualizada de ingreso.
    """
    ingresar_menu = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            ingresar_menu = True

        elif not event.key in lista_key : #and not bloquear_texto
            # Agrega caracteres a la entrada del usuario
            ingreso += event.unicode
    return ingresar_menu, ingreso


def verificar_evento_tiempo(event:pygame.event.Event, tiempo_incremento_velocidad_enemigo:int, segundos:int) -> tuple: #verificar evento tiempo
    """
        Verifica el evento de tiempo y realiza acciones correspondientes.

        param:
            event (pygame.event.Event): Objeto de evento de pygame.
            tiempo_incremento_velocidad_enemigo (int): Contador para el incremento de velocidad del enemigo.
            segundos (int): Contador de segundos.

        return:
            tuple[int, int, bool]: Una tupla con el nuevo valor de segundos, tiempo_incremento_velocidad_enemigo actualizado y un indicador para ingresar al menú.
    """
    ingresar_menu = False
    if event.type == pygame.USEREVENT:
        tiempo_incremento_velocidad_enemigo += 1
        if segundos != 0:
            segundos = segundos - 1
        else:
            ingresar_menu = True
            
    return  segundos, tiempo_incremento_velocidad_enemigo, ingresar_menu


def verificar_evento_salto(saltar:bool, contador_salto: int, presionar_tecla:pygame.key, personaje: object) -> tuple[bool, int]: #evneto salto
    """Verifica el evento de salto del personaje y actualiza su posición en consecuencia.

        param:
            saltar (bool): Indica si el personaje está en proceso de salto.
            contador_salto (int): Contador para el control del salto.
            presionar_tecla (pygame.key): Estado de las teclas presionadas.
            personaje (object): Objeto del personaje cuya posición se modificará.

        return:
        - tuple[bool, int]: Una tupla con el nuevo valor de 'saltar' y 'contador_salto'.

    """
    
    if not(saltar):
        if presionar_tecla[K_SPACE]:
            saltar = True
    elif contador_salto >= -10:
        personaje.posicion_y -= (contador_salto * abs(contador_salto)) * 0.5
        contador_salto -= 0.5
        personaje.modificar_posicion_rect()
    else:
        contador_salto = 10
        saltar = False

    return saltar, contador_salto


def verificar_evento_menu_KEYDOWN(event, ingreso): #MENU KEYDOWNS
    """
    Verifica el evento de teclado durante la entrada en el menú.

    param:
        event (pygame.event): Evento de teclado.
        ingreso (str): Cadena de texto actual.

    return:
        tuple[str, bool]: Una tupla con la cadena de texto actualizada ('ingreso') y un indicador ('verificar_evento').
    """
    verificar_evento = True
    if event.key == pygame.K_BACKSPACE:
        ingreso = ingreso[:-1]
    elif event.key == pygame.K_RETURN:
        verificar_evento = False
    else:
        if len(ingreso) < 10:
            ingreso += str(event.unicode)
            print(f"ingreso: {ingreso}" )

    return ingreso, verificar_evento
