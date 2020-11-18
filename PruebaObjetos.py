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

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

from modelos import *
    
#Usamos comando controller para llamar el controlador
#controller = Controlador()



#fundion para que el programa reaccione al dar comando con las teclas o clicks
def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    if key == glfw.KEY_UP:
        controller.moveUp = not controller.moveUp

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')
    


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 900
    height = 900


    window = glfw.create_window(width, height, "Prueba", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()
     
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.2, 0.2, 0.85, 1.0)


    # Creamos nuestros objetos 
    avion = plane()
    cielo = cielo()
    pastito = pasto()
    #nubes = createNubes()
    montanas = createMontanas()
    panel = panel_de_vuelo()
    perilla = perilla_velocimetro()
    indicador = indicadores()
    nube = nubes()
    botones = botones()
    # definimos un tiempo para el movimiento de objetos
    
    t0 = 0
    
    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        
        
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Agregamos lo que ocurrirá en la pantalla en orden
        
        
        cielo.draw(pipeline)
        pastito.draw(pipeline)
        montanas.draw(pipeline)
        avion.draw( pipeline)
        panel.draw(pipeline)
        perilla.draw(pipeline)
        indicador.draw(pipeline)
        nube.draw(pipeline)
        botones.draw(pipeline)
        
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        

    
    glfw.terminate()