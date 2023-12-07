import pygame
from variables import *
from funciones import *

running = True
while running:
    screen.fill((100, 100, 100))
    pygame.time.delay(10)

    #RENDER JUEGO
    etiqueta_segundos = font.render(str(segundos), True, (255,255,255))
    etiqueta_vidas = font.render('vidas: ' + str(vidas) , True, (255,255,255))
    etiqueta_cantidad_errores = font.render(str(contador_errores), True, (255,255,255))
    etiqueta_correctas = font.render(str(palabras_correctas), True, (255,255,255))
    etiqueta_palabra = font.render(ingreso, True, (255,255,255))
    centrar_posicion = int(640 - etiqueta_palabra.get_width()*0.5)
    etiqueta_palabra_ataque = font.render(palabra, True, (255, 255, 255))
    ingreso_nombre_usuario_etiqueta = font_usuario.render(str(ingreso_nombre_usuario), True, (0, 0, 0))

    #RESTABLECE LOS VALORES EN CASO DE COMPLETAR TIEMPO O SALIR
    if ingresar_menu_tiempo or ingresar_menu_escape:
        if ingresar_menu_tiempo:
            puntuacion_base_datos.insertar_registro(ingreso_nombre_usuario, palabras_correctas, contador_errores, vidas)
        comenzar_juego = False
        ingresar_menu_tiempo = False
        ingresar_menu_escape = False
        segundos = TIEMPO_JUEGO
        vidas = 5
        contador_errores = 0
        palabras_correctas = 0
        x_mapa = 0
        ingreso = ''
        tiempo_incremento_velocidad_enemigo = 0
        enemigo.posicion_x = 1100
        enemigo.modificar_posicion_rect(0)

    #--------------------------------------------------------------------------  
    presionar_tecla = pygame.key.get_pressed()
    if comenzar_juego: #MOVIMIENTO PERSONAJE JUEGO(FONDO)
        if True in presionar_tecla: #movimiento del personaje
            if presionar_tecla[K_3]:
                posicion_derecha = False
                x_mapa = mover_izquierda_personaje(x_mapa, personaje)  
            if presionar_tecla[K_9]:
                posicion_derecha = True
                x_mapa = mover_derecha_personaje(x_mapa, personaje) 
        else: #establece la posicion estatica del personajes si no se toca ninguna tecla
            colocar_personaje_estatico(posicion_derecha, personaje)

    #EVENTOS
    for event in pygame.event.get():
        #EVENTO QUIT
        running = verificar_evento_QUIT(event)
        if comenzar_juego: #CONTROL EVENTO JUEGO
            #EVENTO KEYDOWN
            ingresar_menu_escape, ingreso = verificar_evento_KEYDOWN(event, lista_key, ingreso)

            #TEMPORIZADOR
            segundos, tiempo_incremento_velocidad_enemigo, ingresar_menu_tiempo = verificar_evento_tiempo(event, tiempo_incremento_velocidad_enemigo, segundos)
        else: #CONTROL EVENTOS MENU

            if event.type == pygame.MOUSEBUTTONDOWN:
                sonido_click_menu.play()
                if boton_comenzar.rect_boton.collidepoint(event.pos):
                    if not entrar_score and not ingreso_menu_usuario:
                        comenzar_juego = True

                elif not entrar_score and not ingreso_menu_usuario:
                    if boton_registro.rect_boton.collidepoint(event.pos):
                        entrar_score = True

                    if boton_configuracion.rect_boton.collidepoint(event.pos):
                        ingreso_menu_usuario = True
                        ingreso_nombre_usuario = ''
                else:
                    if boton_volver.rect_boton.collidepoint(event.pos):
                        entrar_score = False
                        ingreso_menu_usuario = False

            if event.type == pygame.KEYDOWN:
                if not comenzar_juego:
                    if ingreso_menu_usuario == True:
                        sonido_click_usuario.play() #sonido
                        ingreso_nombre_usuario, ingreso_menu_usuario = verificar_evento_menu_KEYDOWN(event, ingreso_nombre_usuario)

    #--------------------------------------------------------------------------  

    #VERIFICACIONES DE JUEGO
    if comenzar_juego:
        saltar, contador_salto = verificar_evento_salto(saltar, contador_salto, presionar_tecla, personaje)
        #--------------------------------------------------------------------------
        #VERIFICACIONES
        #VALIDACION Y CAMBIO DE PALABRA
        if ingreso == palabra:
            sonido_golpe_personaje.play()
            palabras_correctas += 1
            palabra = random.choice(palabras).lower()
            ingreso = ''
            print(f'palabras_correctas: {palabras_correctas}' )

            #reaccion enemigo si se acierta la palabra
            if mapa_derecha.Rect.colliderect(enemigo.Rect):
                if pantalla.Rect.contains(enemigo.Rect):
                    enemigo.posicion_x += 150
            elif mapa_izquierda.Rect.colliderect(enemigo.Rect):
                if pantalla.Rect.contains(enemigo.Rect):
                    enemigo.posicion_x -= 150

        #VERIFICACION DE LETRA
        pos=0
        for letra in ingreso:
            if letra in palabra[pos]:
                pos += 1
            else:
                contador_errores += 1
                print(f"posicion incorrecta: {letra}", f'te equivocaste: {contador_errores} veces')
                ingreso = ingreso[:-1]

        #MOVIMIENTO ENEMIGO RELATIVO TIEMPO
        if not personaje.Rect.colliderect(enemigo.Rect):
            if mapa_derecha.Rect.colliderect(enemigo.Rect):#enemigo por derecha
                enemigo.actualizar()
                enemigo.cambiar_imagen('imagenes\\movimiento_enemigo_izquierda1.png', 11, 1747, 178)

                if cambio_posicion_derecha:
                    tiempo_incremento_velocidad_enemigo  = 0
                    cambio_posicion_derecha = False
                    cambio_posicion_izquierda = True 

                if tiempo_incremento_velocidad_enemigo > 10:
                    enemigo.posicion_x -= 8
                    
                if ((segundos * 100) // TIEMPO_JUEGO) < 25:
                    enemigo.posicion_x -= 6
                elif ((segundos * 100) // TIEMPO_JUEGO) < 50:
                    enemigo.posicion_x -= 5
                elif((segundos * 100) // TIEMPO_JUEGO) < 75:
                    enemigo.posicion_x -= 4
                else:
                    enemigo.posicion_x -= 2
            elif mapa_izquierda.Rect.colliderect(enemigo.Rect):#enemigo por izquierda
                enemigo.actualizar()
                enemigo.cambiar_imagen('imagenes\\movimiento_enemigo_derecha.png', 11, 1747, 178)
                if cambio_posicion_izquierda:
                    tiempo_incremento_velocidad_enemigo = 0
                    cambio_posicion_izquierda = False 
                    cambio_posicion_derecha = True

                #aumento velocidad enemigo
                if tiempo_incremento_velocidad_enemigo > 10:
                    enemigo.posicion_x += 8

                #aumento velocidad por avance del tiempo
                if 0 <((segundos * 100) // TIEMPO_JUEGO) < 25:
                    enemigo.posicion_x += 6
                elif ((segundos * 100) // TIEMPO_JUEGO) < 50:
                    enemigo.posicion_x += 5
                elif((segundos * 100) // TIEMPO_JUEGO) < 75:
                    enemigo.posicion_x += 4
                else:
                    enemigo.posicion_x += 2
            primer_contacto = True
        
        #mientras el enemigo no se encuentre dentro del mapa
        if not mapa_derecha.Rect.contains(enemigo.Rect) and not mapa_izquierda.Rect.contains(enemigo.Rect):
            if mapa_derecha.Rect.colliderect(enemigo.Rect) and mapa_izquierda.Rect.colliderect(enemigo.Rect):
                pass
            else:
                if presionar_tecla[K_9]:
                    enemigo.posicion_x += 10
                elif presionar_tecla[K_3]:
                    enemigo.posicion_x -= 10

        #acciones si hay contacto enemigo con personaje
        if personaje.Rect.colliderect(enemigo.Rect) and primer_contacto:
            sonido_golpe_enemigo.play()
            print('contacto con el personaje')
            vidas -= 1
            print(f'vidas_restantes: {vidas}')
            if vidas == 0:
                ingresar_menu_escape = True
            primer_contacto = False
    #VERIFICACIONES DE MENU     
    else:
        if entrar_score:
            if ingreso_base_datos:
                lista_scores = []
                primeros_puntajes = puntuacion_base_datos.seleccionar_registros()#seleccion de base de datso
                for jugadores in primeros_puntajes:
                    salida_registro = f"jugador: {jugadores[0]}.  palabras correctas: {jugadores[1]}.  letras incorrectas: {jugadores[2]}.  vidas restantes: {jugadores[3]}."
                    font_registro = font.render(salida_registro, True, (0, 0, 0))
                    lista_scores.append(font_registro)
                ingreso_base_datos = False
                print(lista_scores)
        else:
            ingreso_base_datos = True

    #--------------------------------------------------------------------------     
    #BLITEOS JUEGO 
    if comenzar_juego:
        enemigo.modificar_posicion_rect(x_mapa)

        #BLITEOS
        # bliteo fondo
        x_relativa = x_mapa % bosque_fondo.dimension_x
        bosque_fondo.dibujar(screen, x_relativa - bosque_fondo.dimension_x)
        if x_relativa < 1280:
            bosque_fondo.dibujar(screen, x_relativa)

        #palabras-enemigos
        screen.blit(etiqueta_palabra_ataque, (enemigo.posicion_x - etiqueta_palabra_ataque.get_width()/2 + 20 + x_mapa, enemigo.posicion_y - 90))


        #recuadro-palabra
        etiqueta_recuadro.dibujar(screen)
        screen.blit(etiqueta_palabra, (centrar_posicion,100))

        #temporizador
        screen.blit(etiqueta_segundos, (300, 60))
        Etiqueta_tiempo.dibujar(screen)

        #vidas
        screen.blit(etiqueta_vidas, (20, 650))

        #palabras correctas e incorrectas
        screen.blit(etiqueta_correctas, (1130, 65))
        etiqueta_palabras_correctas.dibujar(screen)
        screen.blit(etiqueta_cantidad_errores, (1100, 125))
        etiqueta_incorrectas.dibujar(screen)

        personaje.mostrar_personaje(screen)
        enemigo.mostrar_personaje(screen, 25, x_mapa)
    # BLITEOS MENU
    else:
        
        if entrar_score:
            menu_score.mostrar_menu(screen)
            boton_volver.mostrar_opciones(screen)
            posicion_x_registro = 350
            for pos in range(len(lista_scores)):
                screen.blit(lista_scores[pos], (50, posicion_x_registro))
                posicion_x_registro += 50
        elif ingreso_menu_usuario:
            menu_ingresar_usuario.mostrar_menu(screen)
            boton_volver.mostrar_opciones(screen)
            screen.blit(ingreso_nombre_usuario_etiqueta,(510, 335))
        else:
            mi_menu.mostrar_menu(screen)
            boton_comenzar.mostrar_opciones(screen)
            boton_registro.mostrar_opciones(screen)
            boton_configuracion.mostrar_opciones(screen)
    pygame.display.flip()
pygame.quit()