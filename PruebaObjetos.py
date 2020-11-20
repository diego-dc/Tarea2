# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 19:10:48 2020

@author: diegc
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations2 as tr2
import basic_shapes as bs
import scene_graph2 as sg
import easy_shaders as es
from Controlador import * 

from modelos3D import *

def simulador_en_mov():
    
     #avion.PresionarBotones(perillas, indicadores, botones)
     #perillas.perillas_accion(avion, pipeline)
     #indicadores.indicadores_accion(avion, pipeline)
     #nubes.crear_nubes() #crea nubes aleatoriamente
     #montanas.crear_montanas()
     
     
     
     
     #cielo.draw(pipeline)
     #montanas.DrawMoving_x(pipeline, dt)
     #pastito.draw(pipeline)
     #nubes.DrawMoving_x(pipeline, dt)
     avion.prender_apagar_motor = True
     avion.en_aire = True
     avion.draw(pipeline, projection, view)
     montana.draw(pipeline, projection, view)
     #panel.draw(pipeline)
     #indicadores.draw(pipeline)
     #perillas.draw(pipeline)
     #botones.presionar_botones(pipeline)
    
if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Simulador de avión 3D', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Creamos el controlador
    controlador = Controller()

    

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Creating shader programs for textures and for colores
    pipelineTexture = es.SimpleTextureModelViewProjectionShaderProgram()
    pipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creamos los objetos
    axis = Axis()
    avion = plane()
    montana = mountain()

    # Le entregamos el modelo que trabajara el controlador
    controlador.set_model(avion)

    # Creamos la camara y la proyección
    projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Crearemos las posiciones en que estará la cámara
        if avion.camara1:
            cam_y = avion.pos_y *0.1
        elif avion.camara2:
            cam_y = 0.3
        elif avion.camara3:
            cam_y = -0.3

        # Generaremos diversas cámaras.
        view = tr2.lookAt(
            np.array([avion.pos_x - 0.5, cam_y, 1]), # eye
            np.array([avion.pos_x + 0.5, avion.pos_y, avion.pos_z]), # at
            np.array([0,0,1])  # up
        )

        # Dibujamos
        axis.draw(pipeline, projection, view)
        simulador_en_mov()

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
