# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 17:46:23 2020

@author: diegc
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from modelos import *
from Controlador import * 


def simulador_en_mov():
    
     avion.PresionarBotones(perillas, indicadores, botones)
     perillas.perillas_accion(avion, pipeline)
     indicadores.indicadores_accion(avion, pipeline)
     nubes.crear_nubes() #crea nubes aleatoriamente
     montanas.crear_montanas()
     
     
     
     
     cielo.draw(pipeline)
     montanas.DrawMoving_x(pipeline, dt)
     pastito.draw(pipeline)
     nubes.DrawMoving_x(pipeline, dt)
     avion.draw(pipeline)
     panel.draw(pipeline)
     indicadores.draw(pipeline)
     perillas.draw(pipeline)
     botones.presionar_botones(pipeline)
     
def simulador_quieto():
     
     avion.PresionarBotones(perillas, indicadores, botones)
     cielo.draw(pipeline)
     montanas.draw(pipeline)
     pastito.draw(pipeline)
     nubes.draw(pipeline)
     avion.draw(pipeline)
     panel.draw(pipeline)
     indicadores.draw(pipeline)
     perillas.draw(pipeline)
     botones.presionar_botones(pipeline)
     
# Con esta función modificaremos la posición en Y del escenario para simular ascenso o descenso 
def simulador_elevar_descender():
    if avion.despegar:
        
        montanas.en_aire = True
        nubes.en_aire = True
        pastito.update_down()
        nubes.crear_nubes() #crea nubes aleatoriamente
        montanas.crear_montanas()
        
        cielo.draw(pipeline)
        montanas.DrawMovingDown_x_y(pipeline, dt)
        pastito.draw(pipeline)
        nubes.DrawMovingDown_x_y(pipeline, dt)
        avion.draw(pipeline)
        panel.draw(pipeline)
        indicadores.draw(pipeline)
        perillas.draw(pipeline)
        botones.presionar_botones(pipeline)
        
    if avion.aterrizar or avion.caida_libre:
        
        montanas.en_aire = False
        nubes.en_aire = False
        pastito.update_up()
        nubes.crear_nubes() #crea nubes aleatoriamente
        montanas.crear_montanas()
        
        cielo.draw(pipeline)
        montanas.DrawMovingUp_x_y(pipeline, dt)
        pastito.draw(pipeline)
        nubes.DrawMovingUp_x_y(pipeline, dt)
        avion.draw(pipeline)
        panel.draw(pipeline)
        indicadores.draw(pipeline)
        perillas.draw(pipeline)
        botones.presionar_botones(pipeline)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 900
    height = 900


    window = glfw.create_window(width, height, "Simulador de Avión", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    
    
    #definimos el controlador de nuestro modulo
    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
    pipelineTexture = es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.2, 0.2, 0.85, 1.0)


    # Creamos nuestros objetos 
    avion = plane()
    cielo = cielo()
    pastito = pasto()
    nubes = createNubes()
    montanas = createMontanas()
    panel = panel_de_vuelo()
    perillas = perilla_velocimetro()
    indicadores = indicadores()
    botones = botones()
    youdied = you_died()
    
    # definimos un tiempo para el movimiento de objetos
    
    t0 = 0
    
    # Le entregamos el modelo que trabajara el controlador
    controlador.set_model(avion)
    
    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        
        # Calculamos el dt
        v = avion.velocidad
        ti = glfw.get_time()
        dt = (ti - t0) * (v * 0.01)
        t0 = ti
        
        # Using GLFW to check for input events
        glfw.poll_events()
        

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Agregamos lo que ocurrirá en la pantalla en orden
        
        if avion.caida_libre:
            avion.caidaLibre()
            simulador_elevar_descender()
            if avion.youdied:
                glUseProgram(pipelineTexture.shaderProgram)
                youdied.draw(pipelineTexture)
                glUseProgram(pipeline.shaderProgram)
                
        elif avion.despegar:
            avion.despegar_aterrizar(pastito)
            simulador_elevar_descender()
            
        elif avion.aterrizar:
            avion.despegar_aterrizar(pastito)
            simulador_elevar_descender()
                
        elif avion.moverAvion:
                
                avion.Move_right_or_left()
                avion.Move_up_or_down()
                simulador_en_mov()
                if 28 < avion.cabeceo_angulo < 35 or -35 < avion.cabeceo_angulo < -28:
                    print ("CUIDADO. PERDIENDO ESTABILIDAD")
                if 110 < avion.velocidad < 145:
                    print ("CUIDADO. REDUZCA VELOCIDAD; AVIÓN PUEDE SUFRIR DAÑOS")
                if avion.velocidad < 50 and avion.en_aire:
                    print ("PERDIENDO CONTROL")
        
    
        elif avion.velocidad == 0:
            avion.velocidad_avion()
            simulador_quieto()
            
            
        else:
            avion.velocidad_avion()
            simulador_en_mov()
            
        
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
            
        

    
    glfw.terminate()
        