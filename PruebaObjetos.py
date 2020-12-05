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

    montanas.DrawMoving_x(pipeline, projection, view, dt)
    pastito.draw(pipeline, projection, view)
    avion.en_aire = True
    avion.draw(pipeline, projection, view)
    if avion.velocidad != 0:
        montanas.crear_montanas()
        holes.crear_holes(pipeline, projection, view, dt)

    if panel.mostrar_panel:
        panel.draw(pipeline,projection, view)
        perillas.draw(pipeline, projection, view, avion)
        indicadores.draw(pipeline, projection, view, avion)
        botones.presionar_botones(pipeline, projection, view)
     
    
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
    glClearColor(0, 0.6, 1, 1.0) # Usamos un color cielo

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creamos los objetos
    
    #escenario
    axis = Axis()
    montanas = createMontanas()
    holes = create_holes()
    pastito = pasto()
    

    #Avion
    avion = plane()
    panel = panel_de_vuelo()
    perillas = perilla_velocimetro()
    botones = botones()
    indicadores = indicadores()

    # Le entregamos el modelo que trabajara el controlador
    controlador.set_model(avion)
    controlador.set_adjuntos(panel, perillas, botones, indicadores)

    # Creamos la camara y la proyección
    #projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    # inicializamos algunas variables que usaremos 
    t0 = glfw.get_time()
    at = np.zeros(3)
    z0 = 0.
    y0 = 0.
    phi = np.pi * 0.25
    theta = 0
    up = np.array((0., 0., 1.))
    # Donde estará la cámara:
    viewPos = np.zeros(3)
    viewPos[0] = avion.pos_x - 0.8 # Definimos un x inicial más atrás que el avión.
    viewPos[2] = -0.8 #Definimos una vista desde la altura, un z más alto.

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Calculamos el dt
        v = avion.velocidad
        ti = glfw.get_time()
        dt = (ti - t0) * (v * 0.01)
        t0 = ti

        # Variables que nos servirán para el calculo de los ángulos de la cámara.
        y1 = avion.pos_y
        z1 = avion.pos_z

        dz = (z1 - z0) * 0.5
        z0 = z1

        dy = y1 - y0
        y0 = y1

        # Actualizamos los angulos
        phi, theta = controlador.update_angle(dy, dz)
        
        # REMAINDER:
        #  x = cos(phi) * sin(theta)
        #  y = sin(phi) * sin(theta)
        #  z = cos(theta)
        at = np.array([
                np.cos(phi) * np.sin(theta),    # x
                np.sin(phi) * np.sin(theta),    # y
                np.cos(theta)                   # z
            ])

        phi_side = phi + np.pi * 0.5 # Simple correction

        # We have to redefine our at and forward vectors
        # Now considering our character's position.
        new_at = at + viewPos
        forward = new_at - viewPos

        # Move character according to the given parameters
        controlador.move(window, viewPos, forward, dt)
        
        # Definimos la configuración de la cámara.
        view = tr.lookAt(
            viewPos,            # Eye
            at + viewPos,       # At
            up                  # Up
        )

        # Dibujamos
        axis.draw(pipeline, projection, view)
        simulador_en_mov()

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
