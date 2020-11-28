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
     montanas.crear_montanas()
     
     
     
     
     #cielo.draw(pipeline)
     montanas.DrawMoving_x(pipeline, projection, view, dt)
     #pastito.draw(pipeline)
     #nubes.DrawMoving_x(pipeline, dt)
     avion.prender_apagar_motor = True
     avion.en_aire = True
     avion.draw(pipeline, projection, view)
     #montana.draw(pipeline, projection, view)
     holes.draw(pipeline, projection, view)
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
    montanas = createMontanas()
    holes = holes()

    # Le entregamos el modelo que trabajara el controlador
    controlador.set_model(avion)

    # Creamos la camara y la proyección
    #projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    # Initializing first variables 
    t0 = glfw.get_time()
    at = np.zeros(3)
    z0 = 0.
    y0 = 0.
    phi = np.pi * 0.25
    theta = 0
    up = np.array((0., 0., 1.))
    # Donde estará la cámara:
    viewPos = np.zeros(3)
    viewPos[0] = avion.pos_x - 0.8
    viewPos[2] = 0.3

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

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        y1 = avion.pos_y
        z1 = avion.pos_z

        dt2 = t1 - t0
        t0 = t1

        dz = z1 - z0
        z0 = z1

        dy = y1 - y0
        y0 = y1

        # update angles
        phi, theta = controlador.update_angle(dy, dz, dt)

        # Setting up the view transform

        # Where do we look at?
        # A good way to understand this is that we would like
        # to see in fron of us in each possible angle.
        # This is what we do using spherical coordinates
        
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

        # Side vector, this helps us define 
        # our sideway movement
        new_side = np.array([
                0,
                 avion.pos_y,
                0
            ])

        # We have to redefine our at and forward vectors
        # Now considering our character's position.
        new_at = at + viewPos
        forward = new_at - viewPos

        # Move character according to the given parameters
        controlador.move(window, viewPos, forward, new_side, dt)
        
        # Setting camera look.
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
