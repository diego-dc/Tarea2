# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 12:07:55 2020

@author: diegc
"""
from OpenGL.GL import *
import glfw
import numpy as np
import sys

import transformations2 as tr
import easy_shaders as es
import scene_graph2 as sg
import basic_shapes as bs


# Acá crearemos todos nuestros modelos como clases para despues utilizarlos en el modulo principal



class cielo(object):
    def __init__(self):
        
        gpuCieloAzul = es.toGPUShape(bs.createSky(-1,0.5))
        
        cielo1 = sg.SceneGraphNode("cielo")
        cielo1.childs += [gpuCieloAzul]
        
        self.model = cielo1
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
        
class pasto(object):
    def __init__(self):
        
        gpuPastoVerde = es.toGPUShape(bs.createSuelo(-0.2,0,0.8,0.1))
        
        pastito = sg.SceneGraphNode("pastito")
        pastito.childs += [gpuPastoVerde]
        
        self.pos_y = 0
        self.elevar = False
        self.descender = False 
        self.model = pastito
        
        
    def draw(self, pipeline):
        #self.model.transform = tr.translate(0, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
    def update_up(self):
        if self.pos_y <= 0:
            self.pos_y += 0.002
            self.model.transform = tr.translate(0, self.pos_y, 0)
        else: 
            self.model.transform = tr.translate(0, self.pos_y, 0)
        
    def update_down(self):
        if self.pos_y >= -0.2:
            self.pos_y -= 0.002
            self.model.transform = tr.translate(0, self.pos_y, 0)
        else:
            self.model.transform = tr.translate(0, self.pos_y, 0)

#creamos el grafo para un objeto que hace un avión 
class plane(object):
    def __init__(self):
        
        gpuCuboBlanco = es.toGPUShape(bs.createColorCube(1,1,1))
        gpuPiramideBlanco = es.toGPUShape(bs.createColorPyramid(0.5,0.5,0.5))
        gpuCuboCeleste = es.toGPUShape(bs.createColorCube(0.2,0.8,0.9))
    
        #la idea es realizar una avioneta
        #definimos primero las partes que necesitaran tamaños distintos
    
    
        #realizamos el cuerpo del avion
        cuerpo = sg.SceneGraphNode("cuerpo")
        cuerpo.transform = tr.scale(0.8, 0.4, 0.3)
        cuerpo.childs += [gpuCuboBlanco]
    
        #realizamos la parte delantera del avion 
        cara = sg.SceneGraphNode("cara")
        cara.transform = tr.scale(0.8, 0.3, 0.2)
        cara.childs += [gpuCuboBlanco]
    
        #Una ventana para que parezca más avión
        ventana = sg.SceneGraphNode("ventana")
        ventana.transform = tr.scale(0.15, 0.41, 0.1)
        ventana.childs += [gpuCuboCeleste]
    
        #la punta del avión
        tamPunta = sg.SceneGraphNode("tamPunta")
        tamPunta.transform = tr.scale(0.2, 0.3, 0.3)
        tamPunta.childs += [gpuPiramideBlanco]
    
        #la ala trasera
        tamAlatrasera = sg.SceneGraphNode("tamAlatrasea")
        tamAlatrasera.transform = tr.scale(0.3, 0.25, 0.5)
        tamAlatrasera.childs += [gpuPiramideBlanco]
    
        #Esta será parte de la ala trasera también 
        tamAleta = sg.SceneGraphNode("tamAleta")
        tamAleta.transform = tr.scale(0.2, 0.1, 0.5)
        tamAleta.childs += [gpuPiramideBlanco]

        #Esta será parte de la ala trasera también
        tamAleta2 = sg.SceneGraphNode("tamAleta2")
        tamAleta2.transform = tr.scale(0.2, 0.1, 0.5)
        tamAleta2.childs += [gpuPiramideBlanco]
    
        #Esta será la ala que se visualizará por un costado del avión
        tamAla = sg.SceneGraphNode("tamAla")
        tamAla.transform = tr.scale(0.7,0.1,0.9)
        tamAla.childs += [gpuPiramideBlanco]


        #Esta será la otra ala que se visualizará por un costado del avión
        tamAla2 = sg.SceneGraphNode("tamAla")
        tamAla2.transform = tr.scale(0.7,0.1,0.9)
        tamAla2.childs += [gpuPiramideBlanco]
    

        #ahora realizamos las rotaciones para que cada pieza quede mirando a donde debería
        punta = sg.SceneGraphNode("punta")
        punta.transform = tr.rotationY(np.radians(90))
        punta.childs += [tamPunta]
    
    
        alaTrasera = sg.SceneGraphNode("alaTrasera")
        alaTrasera.transform = tr.rotationY(np.radians(-90))
        alaTrasera.childs += [tamAlatrasera]
    
    
        aleta = sg.SceneGraphNode("aleta")
        aleta.transform = tr.rotationX(np.radians(270))
        aleta.childs += [tamAleta]


        aleta2 = sg.SceneGraphNode("aleta2")
        aleta2.transform = tr.rotationX(np.radians(90))
        aleta2.childs += [tamAleta2]
    
    
        ala = sg.SceneGraphNode("ala")
        ala.transform = tr.rotationX(np.radians(270))
        ala.childs += [tamAla]


        ala2 = sg.SceneGraphNode("ala2")
        ala2.transform = tr.rotationX(np.radians(90))
        ala2.childs += [tamAla2]
    

        #Finalmente realizamos las traslaciones para que las piezas en conjunto se vean como un avión
    
        posCara = sg.SceneGraphNode("posCara")
        posCara.transform = tr.translate(0.3, 0, 0)
        posCara.childs += [cara]
    
        posVentana = sg.SceneGraphNode("ventana")
        posVentana.transform = tr.translate(0.41, 0, 0.11)
        posVentana.childs += [ventana]
    
    
        posPunta = sg.SceneGraphNode("posPunta")
        posPunta.transform = tr.translate(0.85,0, 0)
        posPunta.childs += [punta]
    
    
        posAlatrasera = sg.SceneGraphNode("posAlatrasea")
        posAlatrasera.transform = tr.translate(-0.65,0,0)
        posAlatrasera.childs += [alaTrasera]
    
    
        posAleta = sg.SceneGraphNode("posAleta")
        posAleta.transform = tr.translate(-0.65,0.3,0)
        posAleta.childs += [aleta]


        posAleta2 = sg.SceneGraphNode("posAleta2")
        posAleta2.transform = tr.translate(-0.65,-0.3,0)
        posAleta2.childs += [aleta2]
    
    
        posAla = sg.SceneGraphNode("posAla")
        posAla.transform = tr.translate(0,0.6,0)
        posAla.childs += [ala]


        posAla2 = sg.SceneGraphNode("posAla2")
        posAla2.transform = tr.translate(0,-0.6,0)
        posAla2.childs += [ala2]
    

        #creamos la raiz de todos los nodos y lo que será nuestro avión
    
        Avion = sg.SceneGraphNode("Avion")
        Avion.childs += [cuerpo]
        Avion.childs += [posCara]
        Avion.childs += [posPunta]
        Avion.childs += [posAlatrasera]
        Avion.childs += [posAleta]
        Avion.childs += [posAleta2]
        Avion.childs += [posAla]
        Avion.childs += [posAla2]
        Avion.childs += [posVentana]
        
        # Con la raiz de el avión completa, creamos nodos para moverlo y darle escala adecuada
        
        cabeceo_nodo = sg.SceneGraphNode("cabeceo_nodo")
        cabeceo_nodo.childs += [Avion]
        
        inclinacion_avion = sg.SceneGraphNode("inclinacion_avion")
        inclinacion_avion.childs += [cabeceo_nodo]
        
        scaledPlane = sg.SceneGraphNode("Avion")
        scaledPlane.transform = tr.uniformScale(0.1)
        scaledPlane.childs += [inclinacion_avion]
        
        
        AvionEnPantalla = sg.SceneGraphNode("AvionEnPantalla")  
        AvionEnPantalla.childs += [scaledPlane]  

        self.model = AvionEnPantalla
        self.cabeceo_nodo = cabeceo_nodo
        self.inclinacion_lateral = inclinacion_avion
        
        self.angulo_inclinacion = 0
        self.inclinacion_izq = False
        self.inclinacion_der = False

        self.cabeceo_angulo = 0
        self.cabeceo = False
        self.cabeceo_up = False
        self.cabeceo_down = False
        
        self.pos_x = -0.5
        self.pos_y = 0
        self.pos_z = 0

        self.moverAvion = False
        self.move_up = False
        self.move_down = False
        self.move_right = False
        self.move_left = False
        
        self.velocidad = 0
        self.acelerar = False
        self.frenar = False
        
        self.en_aire = False
        self.despegar = False
        self.aterrizar = False
        
        self.prender_apagar_motor = False
        self.prender_apagar_panel = False
        self.prender_apagar_todo = False

        self.camara1 = True
        self.camara2 = False
        self.camara3 = False
        
        self.caida_libre = False
        self.youdied = False
        
        
    # Acá definimos funciones que permitirán la manipulcaión del avión
    
    # Esta función restaura la rotación del avión para que se vea derecho
    def pos_inicial(self):
        if self.cabeceo_up == True:
            self.cabeceo_up = False
            if  0 <= np.radians(self.cabeceo_angulo) < 0.25:
                self.move_up = False
                self.move_down = False
                self.moverAvion = False
                self.cabeceo_angulo = 0
                self.cabeceo_nodo.transform = tr.rotationZ(np.radians(0))
            self.update(self.pos_x, self.pos_y, self.pos_z)

        elif self.cabeceo_down == True:
            self.cabeceo_down = False
            if  -0.25 < np.radians(self.cabeceo_angulo) <= 0:
                self.move_down = False
                self.move_up = False
                self.moverAvion = False
                self.cabeceo_angulo = 0
                self.cabeceo_nodo.transform = tr.rotationZ(np.radians(0))
            self.update(self.pos_x, self.pos_y, self.pos_z)

        elif self.move_right or self.move_left:
            self.inclinacion_izq = False
            self.inclinacion_der = False
            
            if  0 <= np.radians(self.angulo_inclinacion) < 0.5 or -0.5 < np.radians(self.angulo_inclinacion) <= 0:
                print("xd")
                self.move_right = False
                self.move_left = False
                self.moverAvion = False
                self.angulo_inclinacion = 0
                self.inclinacion_lateral.transform = tr.rotationZ(np.radians(0))

        elif self.acelerar or self.frenar :
            self.moverAvion = False
            self.acelerar = False
            self.frenar = False
            self.move_right = False
            self.move_left = False
    
    # Con esta función actualizaremos la posición del avión para cuando se mueva
    def update(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z
        self.model.transform = tr.translate(self.pos_x, self.pos_y, self.pos_z)
    
    # Produce la rotación del avión para el efecto de cabeceo       
    def Cabeceo(self):
        # definimos lo que ocurre en eventos especiales
        if self.despegar == True:
            self.cabeceo_nodo.transform = tr.rotationY(np.radians(25))
        elif self.aterrizar == True:
            self.cabeceo_nodo.transform = tr.rotationY(np.radians(-25))
        elif self.caida_libre:
            self.cabeceo_nodo.transform = tr.rotationY(np.radians(-45))
        # y lo que ocurre en vuelo normal
        else:
            if self.inclinacion_der and np.radians(self.angulo_inclinacion) < 1.1:
                self.angulo_inclinacion += 0.3
                self.inclinacion_lateral.transform = tr.rotationX(np.radians(self.angulo_inclinacion))
            if self.inclinacion_izq and np.radians(self.angulo_inclinacion) > -1.1:
                self.angulo_inclinacion -= 0.3
                self.inclinacion_lateral.transform = tr.rotationX(np.radians(self.angulo_inclinacion))
            if self.cabeceo_up and np.radians(self.cabeceo_angulo) > -0.8:
                self.cabeceo_angulo -= 0.3
                self.cabeceo_nodo.transform = tr.rotationY(np.radians(self.cabeceo_angulo))
                #if self.cabeceo_angulo > 35.5:
                    #self.caida_libre = True
            if self.cabeceo_down and np.radians(self.cabeceo_angulo) < 0.8:
                self.cabeceo_angulo += 0.3
                self.cabeceo_nodo.transform = tr.rotationY(np.radians(self.cabeceo_angulo))
                #if self.cabeceo_angulo < -35.5:
                     #self.caida_libre = True
            if self.inclinacion_der == False and self.inclinacion_izq == False:
                if self.angulo_inclinacion > 0:
                    self.angulo_inclinacion -= 0.1
                    self.inclinacion_lateral.transform = tr.rotationX(np.radians(self.angulo_inclinacion))
                elif self.angulo_inclinacion < 0: 
                    self.angulo_inclinacion += 0.1
                    self.inclinacion_lateral.transform = tr.rotationX(np.radians(self.angulo_inclinacion))

            else:
                self.cabeceo_nodo.transform = tr.rotationY(np.radians(self.cabeceo_angulo))    
                
    # Nos actualiza el valor de verdad del cabeceo y movimiento cuando se quiera mover el avion hacia arriba
    # Nos actualiza el valor de verdad del cabeceo y movimiento cuando se quiera mover el avion hacia abajo
    # Nos actualiza el valor de verdad del movimiento cuando se quiera mover el avion hacia la derecha 
    # Nos actualiza el valor de verdad del movimiento cuando se quiera mover el avion hacia la izquierda
    # También cuando se acelera o se frena  
    def Move_plane(self):
        if self.move_up or self.move_down:
            self.Cabeceo()
            self.posAvion()
        elif self.acelerar or self.frenar:
            self.posAvion()
        elif self.move_right or self.move_left:
            if self.pos_y < -1:
                self.inclinacion_izq = False
                self.inclinacion_der = False
                self.move_right = False
                self.pos_y = -1
                self.angulo_inclinacion = 0
                self.inclinacion_lateral.transform = tr.rotationX(np.radians(self.angulo_inclinacion))
            elif self.pos_y > 1:
                self.inclinacion_izq = False
                self.inclinacion_der = False
                self.move_left = False
                self.pos_y = 1
                self.angulo_inclinacion = 0
                self.inclinacion_lateral.transform = tr.rotationX(np.radians(self.angulo_inclinacion))
            self.Cabeceo()
            self.posAvion()
        else:
            self.Cabeceo()
        
        
    # La función que permitirá que el avión se mueva actualizando el movimiento del avión     
    def posAvion(self):
        # Acá lo que pasa en eventos especiales
        if self.despegar == True:
            self.pos_z += 0.002
            self.update(self.pos_x, self.pos_y, self.pos_z)
        elif self.aterrizar == True:
            self.pos_z -= 0.002
            self.update(self.pos_x, self.pos_y, self.pos_z)
        elif self.caida_libre:
            self.pos_z -= 0.005
            self.update(self.pos_x, self.pos_y, self.pos_z)

        # Acá lo que pasa en vuelo normal
        elif self.move_up:
            if self.move_left and self.pos_y <= 1:
                self.pos_y += -(0.001 * (self.angulo_inclinacion * 0.03))
            elif self.move_right and self.pos_y >= -1:
                self.pos_y -= 0.001 * (self.angulo_inclinacion * 0.03 )
            self.pos_z += -(0.001 * (self.cabeceo_angulo * 0.03))
            self.update(self.pos_x, self.pos_y, self.pos_z)
            #if self.pos_z >= 0.8:
                #self.caida_libre = True
        elif self.move_down:
            if self.move_left and self.pos_y <= 1:
                self.pos_y += -(0.001 * (self.angulo_inclinacion * 0.03))
            elif self.move_right and self.pos_y >= -1:
                self.pos_y -= 0.001 * (self.angulo_inclinacion * 0.03)
            self.pos_z -= 0.001 * (self.cabeceo_angulo * 0.03 )
            self.update(self.pos_x, self.pos_y, self.pos_z)
            #if self.pos_z <= -0.12 and self.en_aire:
                #self.caida_libre = True
        elif self.acelerar == True and self.prender_apagar_motor == True:
            self.pos_x += 0.0008
            self.velocidad += 0.1
            self.update(self.pos_x, self.pos_y, self.pos_z)
            #if self.velocidad > 145:
                #self.caida_libre = True
        elif self.frenar == True and self.prender_apagar_motor == True:
            self.pos_x -= 0.0008
            self.velocidad -= 0.1
            self.update(self.pos_x, self.pos_y, self.pos_z)
            #if self.velocidad < 30 and self.en_aire:
                #self.caida_libre = True
        elif self.move_right and self.pos_y >= -1:
            self.pos_y -= 0.001 * (self.angulo_inclinacion * 0.03)
            self.update(self.pos_x, self.pos_y, self.pos_z)
        elif self.move_left and self.pos_y <= 1:
            self.pos_y += -(0.001 * (self.angulo_inclinacion * 0.03))
            self.update(self.pos_x, self.pos_y, self.pos_z)
        else:
            self.model.transform = tr.translate(self.pos_x, self.pos_y, self.pos_z)
    
    def velocidad_avion(self):
        if self.pos_y > 0.1:
            self.pos_x -=0.00005
            self.velocidad -= 0.02
            self.update(self.pos_x, self.pos_y)
            if self.velocidad < 30 and self.en_aire:
                self.caida_libre = True
        if self.acelerar and self.prender_apagar_motor:
            self.velocidad += 0.1
            self.pos_x += 0.0008
            self.update(self.pos_x, self.pos_y)
            if self.velocidad > 145:
                self.caida_libre = True
        elif self.frenar and self.prender_apagar_motor:
            self.velocidad -= 0.1
            self.pos_x -= 0.0008
            self.update(self.pos_x, self.pos_y)
            if self.velocidad < 30 and self.en_aire:
                self.caida_libre = True
        
        
    def despegar_aterrizar(self, objeto):
        if self.despegar and self.prender_apagar_motor == True:
            if self.pos_y <= 0.2:
                self.move_up = True
                self.Move_up_or_down()
            else:
                self.despegar = False
                self.move_up = False
                self.en_aire = True
                self.cabeceo_angulo = 0
                self.cabeceo_nodo.transform = tr.rotationZ(np.radians(0))
        if self.aterrizar and self.prender_apagar_motor == True:    
            if self.pos_y >= -0.175:
                self.move_down = True
                self.Move_up_or_down()
            elif objeto.pos_y <0 :
                self.pos_y = self.pos_y
            else:
                self.aterrizar = False
                self.move_down = False
                self.en_aire = False
                self.cabeceo_angulo = 0
                self.cabeceo_nodo.transform = tr.rotationZ(np.radians(0))
        if self.prender_apagar_motor == False:
            self.aterrizar = False
            self.despegar = False
            print("Prenda el motor para realizar esta acción")
    
    
    def PresionarBotones(self, perillas, indicadores, botones):
        self.P_A_todo(perillas, indicadores, botones)
        self.P_A_motor(perillas, indicadores, botones)
        self.P_A_panel(perillas, indicadores, botones)
        
        
    def P_A_todo(self,perillas, indicadores, botones):
        if self.prender_apagar_todo:
            if self.prender_apagar_motor == False and self.prender_apagar_panel == False:
                print("Ya está todo apagado")
                self.prender_apagar_todo = False
            elif self.prender_apagar_todo == True:    
                botones.mover_b1 = False
                self.prender_apagar_panel = False
                self.prender_apagar_motor = False
                self.prender_apagar_todo = False
                
                
    def P_A_motor(self,perillas, indicadores, botones):
        if self.prender_apagar_motor:
            botones.mover_b2 = True
        elif self.prender_apagar_motor == False:
            botones.mover_b2 = False
            perillas.apagar = True
    
    def P_A_panel(self,perillas, indicadores, botones):
        if self.prender_apagar_panel:
            perillas.apagar = False
            indicadores.apagar = False
            botones.mover_b3 = True
        
        elif self.prender_apagar_panel == False:
            perillas.apagar = True
            indicadores.apagar = True
            botones.mover_b3 = False
            
    def caidaLibre(self):
        self.move_up = False
        if self.pos_y > -0.175:
                self.move_down = True
                self.Move_up_or_down()
        if self.pos_y <= -0.175:
            self.youdied = True
    
    
    def draw(self, pipeline, projection, view):
        self.Move_plane()
        self.model.transform = tr.translate(self.pos_x, self.pos_y, self.pos_z)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline)
        
class holes(object):
    def __init__(self):
        gpuCuboBlanco = es.toGPUShape(bs.createColorCube(1,1,1))

        prisma = sg.SceneGraphNode("prisma")
        prisma.transform = tr.scale(0.1, 0.1, 0.6)
        prisma.childs += [gpuCuboBlanco]

        prisma_rot = sg.SceneGraphNode("prisma_rot")
        prisma_rot.transform = tr.rotationX(np.radians(90))
        prisma_rot.childs += [prisma]

        superior = sg.SceneGraphNode("superior")
        superior.transform = tr.translate(0, 0, 0.3)
        superior.childs += [prisma_rot]

        inferior = sg.SceneGraphNode("inferior")
        inferior.transform = tr.translate(0, 0, -0.3)
        inferior.childs += [prisma_rot]

        lado_izq = sg.SceneGraphNode("lado_izq")
        lado_izq.transform = tr.translate(0, 0.3, 0)
        lado_izq.childs += [prisma]

        lado_der = sg.SceneGraphNode("lado_der")
        lado_der.transform = tr.translate(0, -0.3, 0)
        lado_der.childs += [prisma]

        hole = sg.SceneGraphNode("hole")
        hole.transform = tr.translate(0, 0, 0.2)
        hole.childs += [superior, inferior, lado_izq, lado_der]

        hole_complete = sg.SceneGraphNode("hole_complete")
        hole.transform = tr.scale(0.4, 0.4, 0.4)
        hole_complete.childs += [hole]

        self.model = hole_complete


    def draw(self, pipeline, projection, view):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline)

        
class Axis(object):

    def __init__(self):
        self.model = es.toGPUShape(bs.createAxis(1))
        self.show = True

    def toggle(self):
        self.show = not self.show

    def draw(self, pipeline, projection, view):
        if not self.show:
            return
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'model'), 1, GL_TRUE, tr.identity())
        pipeline.drawShape(self.model, GL_LINES)
        
#importamos ramdom para que aparezcan de forma aleatoria las nubes
import random 
    
class nubes(object):
    def __init__(self):
        gpuCuadradoBlanco = es.toGPUShape(bs.createColorQuad(1,1,1))
        
        nube = sg.SceneGraphNode("nube")
        nube.transform = tr.scale(0.2, 0.15 ,1) #0.2, 0.15,1
        nube.childs += [gpuCuadradoBlanco]
        
        nube_tr = sg.SceneGraphNode("nube_tr")
        nube_tr.childs += [nube]
        
        
        # Definimos posición del objeto para poder manipularlo luego
        # Queremos que aparezcan en ciertos y's de nuestra pantalla (el cielo)
        self.pos_x = 1.2
        self.pos_y_random = random.choice([0.1, 0.3, 0.5, 0.7, 0.8, 1])
        self.pos_y = 0
        self.model = nube_tr
        self.elevar = False
        self.descender = False
        
        
    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x, self.pos_y + self.pos_y_random, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    # Le asignamos un dt para que sea posible su desplazamiento
    def update_x(self, dt):
        self.pos_x -= dt
        
    def update_y(self):
        if self.elevar:
            self.pos_z_random += 0.002
            self.model.transform = tr.translate(self.pos_x, self.pos_y_random, 0)
        elif self.descender:
            self.pos_y_random -= 0.002
            self.model.transform = tr.translate(self.pos_x, self.pos_y_random, 0)
    
# esto para que reconosca la lista
from typing import List

# Creamos una clase que nos permitirá mostrar nubes aleatorias en la pantalla pasando de der a izq para dar la impresion de avanzar
class createNubes(object):
    
    
    def __init__(self):
        self.creador_nubes = []
        self.en_aire = False
    
    def crear_nubes(self):
        nubess = nubes()
        if self.en_aire == True:
            if (random.random() < 0.005):
                nubess.pos_y = -0.2
                self.creador_nubes.append(nubes())
        elif self.en_aire == False:
            if (random.random() < 0.005):
                nubess.pos_y = 0.2
                self.creador_nubes.append(nubes())
                
                
    def draw(self, pipeline):
        for j in self.creador_nubes:
            j.draw(pipeline)
               
    def clean(self):
        x = 0
        for j in self.creador_nubes:
            if j.pos_x < -1.3:
                self.creador_nubes.pop(x)
                x += 1
            else:
                x += 1
            
    def pos_inicial(self):
        for j in self.creador_nubes:
            j.elevar = False
            j.descender = False
    
    def update_elevar(self):
        for j in self.creador_nubes:
            j.elevar = True
            
    def update_descender(self):
        for j in self.creador_nubes:
            j.descender = True
    
    def update(self, dt):
        for j in self.creador_nubes:
            j.update_x(dt)
            j.update_y()
            
    def DrawMoving_x(self, pipeline, dt):
        self.pos_inicial()
        self.update(dt)
        self.draw(pipeline)
        self.clean()
 
        
    def DrawMovingUp_x_y(self, pipeline, dt):
        self.update_elevar()
        self.update(dt)
        self.draw(pipeline)
        
    def DrawMovingDown_x_y(self, pipeline, dt):
        self.update_descender()
        self.update(dt)
        self.draw(pipeline)


# Creamos el objeto de las montañas con nieve.
class mountain(object):
    def __init__(self):
        gpuTrianguloCafe = es.toGPUShape(bs.createColorPyramid(0.7,0.4,0))
        #gpuTrianguloBlanco = es.toGPUShape(bs.createColorTriangle(1,1,1))
        
        # El fondo que será café, lo ajustamos y trasladamos
        montana_fondo = sg.SceneGraphNode("montana_fondo")
        montana_fondo.transform = tr.uniformScale(0.8)
        montana_fondo.childs += [gpuTrianguloCafe]
        
        montana_tras = sg.SceneGraphNode("montana_tras")
        montana_tras.transform = tr.translate(0,0,0)
        montana_tras.childs += [montana_fondo]
        
        #la nieve: TAMAÑO
       # nieve1 = sg.SceneGraphNode("nieve1")
       # nieve1.transform = tr.uniformScale(0.4)
       # nieve1.childs += [gpuTrianguloBlanco]
        
       # nieve2 = sg.SceneGraphNode("nieve2")
       # nieve2.transform = tr.uniformScale(0.2)
       # nieve2.childs += [gpuTrianguloBlanco]
        
       # nieve3 = sg.SceneGraphNode("nieve3")
       # nieve3.transform = tr.uniformScale(0.15)
      #  nieve3.childs += [gpuTrianguloBlanco]
        
       # nieve4 = sg.SceneGraphNode("nieve4")
       # nieve4.transform = tr.uniformScale(0.15)
       # nieve4.childs += [gpuTrianguloBlanco]
        
        # la nieve: ROTACION
      #  nieve2_rot = sg.SceneGraphNode("nieve2_rot")
       # nieve2_rot.transform = tr.rotationZ(np.radians(180))
       # nieve2_rot.childs += [nieve2]
        
       # nieve3_rot = sg.SceneGraphNode("nieve3_rot")
      #  nieve3_rot.transform = tr.rotationZ(np.radians(180))
       # nieve3_rot.childs += [nieve3]
        
       # nieve4_rot = sg.SceneGraphNode("nieve4_rot")
       # nieve4_rot.transform = tr.rotationZ(np.radians(180))
       # nieve4_rot.childs += [nieve4]
        
        # la nieve: TRASLACION
      #  nieve1_tras = sg.SceneGraphNode("nieve1_tras")
      #  nieve1_tras.transform = tr.translate(0, 0.4, 0)
      #  nieve1_tras.childs += [nieve1]
        
       # nieve2_tras = sg.SceneGraphNode("nieve2_tras")
      #  nieve2_tras.transform = tr.translate(0, 0.1, 0)
      #  nieve2_tras.childs += [nieve2_rot]
        
      #  nieve3_tras = sg.SceneGraphNode("nieve3_tras")
       # nieve3_tras.transform = tr.translate(0.125, 0.125, 0)
      #  nieve3_tras.childs += [nieve3_rot]
        
       # nieve4_tras = sg.SceneGraphNode("nieve4_tras")
       # nieve4_tras.transform = tr.translate(-0.125, 0.125, 0)
       # nieve4_tras.childs += [nieve4_rot]
        
        montana = sg.SceneGraphNode("montana")
        montana.childs += [montana_tras]
        
        montana_tam = sg.SceneGraphNode("montana_tam")
        montana_tam.transform = tr.scale(1.1,random.choice([1.2, 0.9,0.8,0.7,0.6,0.5,0.4]),1)
        montana_tam.childs += [montana]
        
        #montana_pos = sg.SceneGraphNode("montana_pos")
        #montana_pos.transform = tr.translate(0,-0.2,0)
        #montana_pos.childs += [montana_pos]
        
        montana_final = sg.SceneGraphNode("montana_final")
        montana_final.childs += [montana_tam]
        
        self.model = montana
        #Le asignamos posición para poder modificarla
        self.pos_x = 0
        self.pos_y = 0
        self.elevar = False
        self.descender = False
        
        
    # Le asignamos un dt para que sea posible su desplazamiento
    def update_x(self, dt):
        self.pos_x -= dt
        
    def update_y(self):
        if self.elevar and self.pos_y <= -0.2:
            self.pos_y += 0.002
            self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        elif self.descender and self.pos_y >= -0.4:
            self.pos_y -= 0.002
            self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        
    def draw(self, pipeline, projection, view):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline)
        
    
class createMontanas(object):
    
    
    def __init__(self):
        self.creador_montanas = []
        self.en_aire = False
    
    def crear_montanas(self):
        montaña = mountain()
        if self.en_aire == True:
            if (random.random() < 0.005):
                montaña.pos_y = -0.4
                self.creador_montanas.append(montaña)
        elif self.en_aire == False:
            if (random.random() < 0.005):
                montaña.pos_y = -0.2
                self.creador_montanas.append(montaña)
    
    def draw(self, pipeline):
        for j in self.creador_montanas:
            j.draw(pipeline)
            
    def clean(self):
        x = 0
        for j in self.creador_montanas:
            if j.pos_x < -1.3 :
                self.creador_montanas.pop(x)
                x += 1
            else:
                x += 1
            
    def pos_inicial(self):
        for j in self.creador_montanas:
            j.elevar = False
            j.descender = False
    
    def update_elevar(self):
        for j in self.creador_montanas:
            j.elevar = True
            
    def update_descender(self):
        for j in self.creador_montanas:
            j.descender = True
            
    def update(self, dt):
        for j in self.creador_montanas:
            j.update_x(dt) 
            j.update_y()

    def DrawMoving_x(self, pipeline, dt):
        self.pos_inicial()
        self.update(dt)
        self.draw(pipeline)
        self.clean()
 
        
    def DrawMovingUp_x_y(self, pipeline, dt):
        self.update_elevar()
        self.update(dt)
        self.draw(pipeline)
        
    def DrawMovingDown_x_y(self, pipeline, dt):
        self.update_descender()
        self.update(dt)
        self.draw(pipeline)
 
    
class panel_de_vuelo(object):
    def __init__(self):
        gpuWhiteCircle = es.toGPUShape(bs.createColorCircle(30, 1, 1, 1, 1))
        gpuCuadradoverde = es.toGPUShape(bs.createColorQuad(0,1,0))
        gpuCuadradoAzul = es.toGPUShape(bs.createColorQuad(0,0,1))
        gpuCuadradoAmarillo = es.toGPUShape(bs.createColorQuad(0.9,1,0))
        gpuCuadradoRojo = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpuCuadradoBlanco = es.toGPUShape(bs.createColorQuad(1,1,1))
        gpuMesaDeControl = es.toGPUShape(bs.createSuelo(-0.4,0.8,0.8,0.8))
        gpuCuadradoGris = es.toGPUShape(bs.createColorQuad(0.6,0.6,0.7))
        gpuCuadradoNegro = es.toGPUShape(bs.createColorQuad(0.2,0.2,0.2))
        
        # Creamos el fondo de lo que sera la mesa de control
        Mesa_control = sg.SceneGraphNode("Mesa_control")
        Mesa_control.childs += [gpuMesaDeControl]
        
        
        # Este será el velocimetro.
        velocimetro_circ = sg.SceneGraphNode("velocimetro_circ")
        velocimetro_circ.transform = tr.uniformScale(0.8)
        velocimetro_circ.childs += [gpuWhiteCircle]
        
        indicadores_azules = sg.SceneGraphNode("indicadores_azules")
        indicadores_azules.transform = tr.scale(0.03, 0.2, 0)
        indicadores_azules.childs += [gpuCuadradoAzul]
        
        indicadores_verdes = sg.SceneGraphNode("indicadores_verdes")
        indicadores_verdes.transform = tr.scale(0.03, 0.2, 0)
        indicadores_verdes.childs += [gpuCuadradoverde]
        
        indicadores_amarillo = sg.SceneGraphNode("indicadores_amarillo")
        indicadores_amarillo.transform = tr.scale(0.03,0.2,0)
        indicadores_amarillo.childs += [gpuCuadradoAmarillo]
        
        indicadores_rojos = sg.SceneGraphNode("indicadores_rojos")
        indicadores_rojos.transform = tr.scale(0.03, 0.2, 0)
        indicadores_rojos.childs += [gpuCuadradoRojo]
        
        
        
        indicadores_azul_tras = sg.SceneGraphNode("indicadores_azul_tras")
        indicadores_azul_tras.transform = tr.translate(0, 0.65, 0)
        indicadores_azul_tras.childs += [indicadores_azules]
        
        indicadores_verde_tras = sg.SceneGraphNode("indicadores_verde_tras")
        indicadores_verde_tras.transform = tr.translate(0, 0.65, 0)
        indicadores_verde_tras.childs += [indicadores_verdes]
        
        indicadores_amarillos_tras = sg.SceneGraphNode("indicadores_amarillos_tras")
        indicadores_amarillos_tras.transform = tr.translate(0, 0.65, 0)
        indicadores_amarillos_tras.childs += [indicadores_amarillo]
        
        indicadores_rojo_tras = sg.SceneGraphNode("indicadores_rojo_tras")
        indicadores_rojo_tras.transform = tr.translate(0, 0.65, 0)
        indicadores_rojo_tras.childs += [indicadores_rojos]
        
        
        
        
        I_azul1 = sg.SceneGraphNode("I_azul1")
        I_azul1.transform = tr.rotationZ(np.radians(0))
        I_azul1.childs += [indicadores_azul_tras]
        
        I_azul2 = sg.SceneGraphNode("I_azul2")
        I_azul2.transform = tr.rotationZ(np.radians(-20))
        I_azul2.childs += [indicadores_azul_tras]
        
        I_azul3 = sg.SceneGraphNode("I_azul3")
        I_azul3.transform = tr.rotationZ(np.radians(-40))
        I_azul3.childs += [indicadores_azul_tras]
        
        I_azul4 = sg.SceneGraphNode("I_azul4")
        I_azul1.transform = tr.rotationZ(np.radians(-60))
        I_azul1.childs += [indicadores_azul_tras]
        
        
        I_azul5 = sg.SceneGraphNode("I_azul5")
        I_azul5.transform = tr.rotationZ(np.radians(-80))
        I_azul5.childs += [indicadores_azul_tras]
        
        I_verde1 = sg.SceneGraphNode("I_verde1")
        I_verde1.transform = tr.rotationZ(np.radians(-100))
        I_verde1.childs += [indicadores_verde_tras]
        
        I_verde2 = sg.SceneGraphNode("I_verde2")
        I_verde2.transform = tr.rotationZ(np.radians(-120))
        I_verde2.childs += [indicadores_verde_tras]
        
        I_verde3 = sg.SceneGraphNode("I_verde3")
        I_verde3.transform = tr.rotationZ(np.radians(-140))
        I_verde3.childs += [indicadores_verde_tras]
        
        
        I_amarillo1 = sg.SceneGraphNode("I_amarillo1")
        I_amarillo1.transform = tr.rotationZ(np.radians(-160))
        I_amarillo1.childs += [indicadores_amarillos_tras]
        
        I_amarillo2 = sg.SceneGraphNode("I_amarillo2")
        I_amarillo2.transform = tr.rotationZ(np.radians(-180))
        I_amarillo2.childs += [indicadores_amarillos_tras]
        
        I_amarillo3 = sg.SceneGraphNode("I_amarillo3")
        I_amarillo3.transform = tr.rotationZ(np.radians(-200))
        I_amarillo3.childs += [indicadores_amarillos_tras]
        
        I_amarillo4 = sg.SceneGraphNode("I_amarillo4")
        I_amarillo4.transform = tr.rotationZ(np.radians(-220))
        I_amarillo4.childs += [indicadores_amarillos_tras]
        
        I_rojo1 = sg.SceneGraphNode("I_rojo1")
        I_rojo1.transform = tr.rotationZ(np.radians(-240))
        I_rojo1.childs += [indicadores_rojo_tras]
        
        I_rojo2 = sg.SceneGraphNode("I_rojo2")
        I_rojo2.transform = tr.rotationZ(np.radians(-260))
        I_rojo2.childs += [indicadores_rojo_tras]
        
        I_rojo3 = sg.SceneGraphNode("I_rojo3")
        I_rojo3.transform = tr.rotationZ(np.radians(-280))
        I_rojo3.childs += [indicadores_rojo_tras]
        
        I_rojo4 = sg.SceneGraphNode("I_rojo4")
        I_rojo4.transform = tr.rotationZ(np.radians(-300))
        I_rojo4.childs += [indicadores_rojo_tras]
        
        
        velocimetro_tam = sg.SceneGraphNode("velocimetro_tam")
        velocimetro_tam.transform = tr.uniformScale(0.3)
        velocimetro_tam.childs += [ velocimetro_circ , I_azul1, I_azul2, I_azul3, I_azul4, I_azul5, I_verde1, I_verde2,
                                    I_verde3, I_amarillo1, I_amarillo2, I_amarillo3, I_amarillo4, I_rojo1, I_rojo2, I_rojo3, I_rojo4]
        
        velocimetro_tras = sg.SceneGraphNode("velocimetro_tras")
        velocimetro_tras.transform = tr.translate(-0.7, -0.7, 0)
        velocimetro_tras.childs += [velocimetro_tam]
        
        
        # Este será el medidor de revoluciones del motor.
        velocimetro_circ = sg.SceneGraphNode("velocimetro_circ")
        velocimetro_circ.transform = tr.uniformScale(0.8)
        velocimetro_circ.childs += [gpuWhiteCircle]
        
        indicadores_negros = sg.SceneGraphNode("indicadores_negros")
        indicadores_negros.transform = tr.scale(0.03, 0.2, 0)
        indicadores_negros.childs += [gpuCuadradoNegro]
        
        indicadores_negro_tras = sg.SceneGraphNode("indicadores_negro_tras")
        indicadores_negro_tras.transform = tr.translate(0, 0.65, 0)
        indicadores_negro_tras.childs += [indicadores_negros]
        
        
        I_n1 = sg.SceneGraphNode("I_n1")
        I_n1.transform = tr.rotationZ(np.radians(0))
        I_n1.childs += [indicadores_negro_tras]
        
        I_n2 = sg.SceneGraphNode("I_n2")
        I_n2.transform = tr.rotationZ(np.radians(-20))
        I_n2.childs += [indicadores_negro_tras]
        
        I_n3 = sg.SceneGraphNode("I_n3")
        I_n3.transform = tr.rotationZ(np.radians(-40))
        I_n3.childs += [indicadores_negro_tras]
        
        I_n4 = sg.SceneGraphNode("I_n4")
        I_n4.transform = tr.rotationZ(np.radians(-60))
        I_n4.childs += [indicadores_negro_tras]
        
        I_n5 = sg.SceneGraphNode("I_n5")
        I_n5.transform = tr.rotationZ(np.radians(-80))
        I_n5.childs += [indicadores_negro_tras]
        
        I_n6 = sg.SceneGraphNode("I_n6")
        I_n6.transform = tr.rotationZ(np.radians(-100))
        I_n6.childs += [indicadores_negro_tras]
        
        I_n7 = sg.SceneGraphNode("I_n7")
        I_n7.transform = tr.rotationZ(np.radians(-120))
        I_n7.childs += [indicadores_negro_tras]
        
        I_n8 = sg.SceneGraphNode("I_n8")
        I_n8.transform = tr.rotationZ(np.radians(-140))
        I_n8.childs += [indicadores_negro_tras]
        
        I_n9 = sg.SceneGraphNode("I_n9")
        I_n9.transform = tr.rotationZ(np.radians(-160))
        I_n9.childs += [indicadores_negro_tras]
        
        I_n10 = sg.SceneGraphNode("I_n10")
        I_n10.transform = tr.rotationZ(np.radians(-180))
        I_n10.childs += [indicadores_negro_tras]
        
        I_n11 = sg.SceneGraphNode("I_n11")
        I_n11.transform = tr.rotationZ(np.radians(-200))
        I_n11.childs += [indicadores_negro_tras]
        
        I_n12 = sg.SceneGraphNode("I_n12")
        I_n12.transform = tr.rotationZ(np.radians(-220))
        I_n12.childs += [indicadores_negro_tras]
        
        I_n13 = sg.SceneGraphNode("I_n13")
        I_n13.transform = tr.rotationZ(np.radians(-240))
        I_n13.childs += [indicadores_negro_tras]
        
        I_n14 = sg.SceneGraphNode("I_n14")
        I_n14.transform = tr.rotationZ(np.radians(-260))
        I_n14.childs += [indicadores_negro_tras]
        
        I_n15 = sg.SceneGraphNode("I_n15")
        I_n15.transform = tr.rotationZ(np.radians(-280))
        I_n15.childs += [indicadores_negro_tras]
        
        I_n16 = sg.SceneGraphNode("I_n16")
        I_n16.transform = tr.rotationZ(np.radians(-300))
        I_n16.childs += [indicadores_negro_tras]
        
        
        med_rps_motor_tam = sg.SceneGraphNode("med_rps_motor_tam")
        med_rps_motor_tam.transform = tr.uniformScale(0.3)
        med_rps_motor_tam.childs += [ velocimetro_circ , I_n1, I_n2, I_n3, I_n4, I_n5, I_n6, I_n7,
                                    I_n8, I_n9, I_n10, I_n11, I_n12, I_n13, I_n14, I_n15, I_n16]
        
        med_rps_motor_tras = sg.SceneGraphNode("med_rps_motor_tras")
        med_rps_motor_tras.transform = tr.translate(0, -0.7, 0)
        med_rps_motor_tras.childs += [med_rps_motor_tam]
        
        # El medidor de altura.
        med_altura_tam = sg.SceneGraphNode("med_altura_tam")
        med_altura_tam.transform = tr.scale(0.15, 0.4, 0)
        med_altura_tam.childs += [gpuCuadradoGris]
        
        medidores = sg.SceneGraphNode("medidores")
        medidores.transform = tr.scale(0.075, 0.01, 0)
        medidores.childs += [gpuCuadradoNegro]
        
        medidor1 = sg.SceneGraphNode("medidor1")
        medidor1.transform = tr.translate(0, -0.15, 0)
        medidor1.childs += [medidores]
        
        medidor2 = sg.SceneGraphNode("medidor2")
        medidor2.transform = tr.translate(0, -0.075, 0)
        medidor2.childs += [medidores]
        
        medidor3 = sg.SceneGraphNode("medidor3")
        medidor3.transform = tr.translate(0, 0, 0)
        medidor3.childs += [medidores]
        
        medidor4 = sg.SceneGraphNode("medidor4")
        medidor4.transform = tr.translate(0, 0.075, 0)
        medidor4.childs += [medidores]
        
        medidor5 = sg.SceneGraphNode("medidor5")
        medidor5.transform = tr.translate(0, 0.15, 0)
        medidor5.childs += [medidores]
        
        
        med_altura= sg.SceneGraphNode("med_altura")
        med_altura.childs += [med_altura_tam, medidor1, medidor2, medidor3, medidor4, medidor5]
        
        med_altura_tras = sg.SceneGraphNode("med_altura_tras")
        med_altura_tras.transform = tr.translate(-0.35, -0.7, 0)
        med_altura_tras.childs += [med_altura]
        
        
        # Por último realizamos el medidor de cabeceo.
        
        med_cabeceo_tam = sg.SceneGraphNode("med_cabeceo_tam")
        med_cabeceo_tam.transform = tr.scale(0.45, 0.25, 0)
        med_cabeceo_tam.childs += [gpuCuadradoGris]
        
        lineas_Negras = sg.SceneGraphNode("lineas_Negras")
        lineas_Negras.transform = tr.scale(0.28, 0.0085, 0)
        lineas_Negras.childs += [gpuCuadradoNegro]
        
        linea1 = sg.SceneGraphNode("linea1")
        linea1.transform = tr.translate(0, -0.075, 0)
        linea1.childs += [lineas_Negras]
        
        linea2 = sg.SceneGraphNode("linea2")
        linea2.transform = tr.translate(0, 0.075, 0)
        linea2.childs += [lineas_Negras]
        
        linea3 = sg.SceneGraphNode("linea3")
        linea3.transform = tr.translate(0, 0, 0)
        linea3.childs += [lineas_Negras]
        
        med_cabeceo = sg.SceneGraphNode("med_cabeceo")
        med_cabeceo.transform = tr.translate(0.5, -0.7, 0)
        med_cabeceo.childs += [med_cabeceo_tam, linea1, linea2, linea3]
        
        
        # Juntamos las piezas del panel de control
        panel_de_control = sg.SceneGraphNode("panel_de_control")
        panel_de_control.childs += [Mesa_control, velocimetro_tras, med_altura_tras, med_rps_motor_tras, med_cabeceo]
        
        self.model = panel_de_control
    
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')


class perilla_velocimetro(object):
    
    def __init__(self):
        
        gpuTrianguloNegro = es.toGPUShape(bs.createColorTriangle(0.1,0.1,0.1))
    
        perilla_forma = sg.SceneGraphNode("perilla_forma")
        perilla_forma.transform = tr.scale(0.1, 1, 0)
        perilla_forma.childs += [gpuTrianguloNegro]

        perilla_tam = sg.SceneGraphNode("perilla_tam")
        perilla_tam.transform = tr.uniformScale(0.35)
        perilla_tam.childs += [perilla_forma]

        perilla_rot = sg.SceneGraphNode("perilla_rot")
        perilla_rot.childs += [perilla_tam]

        perilla_tras = sg.SceneGraphNode("perilla_tras")
        perilla_tras.transform = tr.translate(-0.7, -0.7, 0)
        perilla_tras.childs += [perilla_rot]
        
        perilla2_forma = sg.SceneGraphNode("perilla2_forma")
        perilla2_forma.transform = tr.scale(0.1, 1, 0)
        perilla2_forma.childs += [gpuTrianguloNegro]

        perilla2_tam = sg.SceneGraphNode("perilla_tam")
        perilla2_tam.transform = tr.uniformScale(0.35)
        perilla2_tam.childs += [perilla2_forma]

        perilla2_rot = sg.SceneGraphNode("perilla_rot")
        perilla2_rot.childs += [perilla2_tam]

        perilla2_tras = sg.SceneGraphNode("perilla_tras")
        perilla2_tras.transform = tr.translate(0, -0.7, 0)
        perilla2_tras.childs += [perilla2_rot]
    
        perilla = sg.SceneGraphNode("perilla")
        perilla.childs += [perilla_tras, perilla2_tras]
    
        self.model = perilla
        self.perilla_rot = perilla_rot
        self.perilla2_rot = perilla2_rot
        self.rotation1 = 0
        self.rotation2 = 0
        self.angulo = 0
        self.apagar = True
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
    
    def perillas_accion(self, objeto, pipeline):
        self.perilla1(objeto, pipeline)
        self.perilla2(objeto,pipeline)
        self.draw(pipeline)
        
    def perilla1(self, objeto, pipeline):
        # La rotación 1 será dependiente de la velocidad del avión, pues sera nuestro velocimetro
        if self.apagar == False and self.rotation1 < 2 * objeto.velocidad:
            self.rotation1 += 1
            self.perilla_rot.transform = tr.rotationZ(np.radians(-self.rotation1))
            
        elif self.apagar == False:
            self.rotation1 = 2 * objeto.velocidad
            self.perilla_rot.transform = tr.rotationZ(np.radians(-self.rotation1))
    def perilla2(self, objeto, pipeline):
        # Para las revoluciones del motor implementamos un angulo que aumentará acorde la velocidad
        # Con esto se logra el efecto de aumento de revoluciones cuando se acelera y reducción de estas cuando no se utiliza el motor
        if objeto.acelerar == True and self.apagar == False:
            if objeto.prender_apagar_motor == True:
                if self.rotation2 < 270:
                    self.rotation2 += 0.5
                    self.angulo += 0.0016
                    self.perilla2_rot.transform = tr.rotationZ(np.radians(-(self.rotation2 + self.angulo)))
                else:
                    self.perilla2_rot.transform = tr.rotationZ(-self.rotation2 + self.angulo)
        elif objeto.frenar ==  True and self.apagar == False:
            if objeto.prender_apagar_motor == True:
                if self.rotation2 > 0:
                    self.rotation2 -= 0.5
                    self.angulo -= 0.0016
                    self.perilla2_rot.transform = tr.rotationZ(np.radians(-(self.rotation2 + self.angulo)))
                else:
                    self.perilla2_rot.transform = tr.rotationZ(np.radians(-(self.rotation2 + self.angulo)))        
        elif self.apagar == True:
            if self.rotation1 > 0 and self.rotation2 > 0:
                if self.rotation1 > 0:
                    self.rotation1 -= 3 
                
                self.rotation2 -= 3
                self.angulo = 0
                self.perilla_rot.transform = tr.rotationZ(np.radians(-self.rotation1))
                self.perilla2_rot.transform = tr.rotationZ(np.radians(-self.rotation2))  
        elif objeto.acelerar == False and objeto.frenar == False:
            if self.apagar == False:
                if (1.75 * objeto.velocidad) < self.rotation2 :
                    self.rotation2 -= 0.5
                    self.angulo -= 0.0016
                    self.perilla2_rot.transform = tr.rotationZ(np.radians(-self.rotation2))
                elif (1.75 * objeto.velocidad) > self.rotation2:
                    self.rotation2 += 0.5
                    self.angulo += 0.0016
                    self.perilla2_rot.transform = tr.rotationZ(np.radians(-self.rotation2))
        elif self.apagar == True:
            if self.rotation1 > 0 and self.rotation2 > 0:
                if self.rotation1 > 0:
                    self.rotation1 -= 3 
                elif self.rotation > 0:
                    self.rotation2 -= 3
                self.angulo = 0
                self.perilla_rot.transform = tr.rotationZ(np.radians(-self.rotation1))
                self.perilla2_rot.transform = tr.rotationZ(np.radians(-self.rotation2))  
        
class indicadores(object):
    def __init__(self):
        gpuCuadradoRojo = es.toGPUShape(bs.createColorQuad(1,0,0))
        
        indicador_forma = sg.SceneGraphNode("indicador_forma")
        indicador_forma.transform = tr.scale(1, 0.8, 0)
        indicador_forma.childs += [gpuCuadradoRojo]

        indicador_tam = sg.SceneGraphNode("indicador_tam")
        indicador_tam.transform = tr.uniformScale(0.08)
        indicador_tam.childs += [indicador_forma]

        indicador_tras = sg.SceneGraphNode("indicador_tras")
        indicador_tras.transform = tr.translate(-0.35, -0.85, 0)
        indicador_tras.childs += [indicador_tam]
        
        indicador2_forma = sg.SceneGraphNode("indicador2_forma")
        indicador2_forma.transform = tr.scale(1, 0.7, 0)
        indicador2_forma.childs += [gpuCuadradoRojo]

        indicador2_tam = sg.SceneGraphNode("indicador2_tam")
        indicador2_tam.transform = tr.uniformScale(0.07)
        indicador2_tam.childs += [gpuCuadradoRojo]

        indicador2_tras = sg.SceneGraphNode("indicador2_tras")
        indicador2_tras.transform = tr.translate(0.5, -0.7, 0)
        indicador2_tras.childs += [indicador2_tam]
        
        
        indicador = sg.SceneGraphNode("indicador")
        indicador.childs += [indicador_tras]
        
        indicador2 = sg.SceneGraphNode("indicador2")
        indicador2.childs += [indicador2_tras]
        
        indicadores = sg.SceneGraphNode("indicadores")
        indicadores.childs += [indicador, indicador2]
        
        
        
        self.model = indicadores
        self.indicador = indicador
        self.indicador2 = indicador2
        self.altura = 0
        self.cabeceo = 0
        self.apagar = True
        
        
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
    def indicadores_accion(self, objeto , pipeline):
        
        self.altura = objeto.pos_y + 0.175
        if 0.175 < self.altura < 1 and self.apagar == False:
            self.indicador.transform = tr.translate(0,self.altura * 0.3,0)
        self.cabeceo = objeto.cabeceo_angulo
        if -35.5 < self.cabeceo < 35.5 and self.apagar == False:
            self.indicador2.transform = tr.translate(0, self.cabeceo * 0.0025, 0)
        else:
            self.altura = 0
            self.indicador.transform = tr.translate(0,self.altura * 0.3,0)
        
        self.draw(pipeline)
        
        
class you_died(object):
    def __init__(self):
        gpuCuadradoRojo = es.toGPUShape(bs.createTextureQuad("images/youdied.jpg"), GL_CLAMP_TO_EDGE, GL_NEAREST)
        
        fondo_rojo = sg.SceneGraphNode("fondo_rojo")
        fondo_rojo.transform = tr.uniformScale(2)
        fondo_rojo.childs += [gpuCuadradoRojo]
        
        self.model = fondo_rojo
        
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
class botones(object):
    def __init__(self):
        gpuCuadradoGris = es.toGPUShape(bs.createColorQuad(0.6,0.6,0.7))
        gpuCuadradoRojo = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpuCuadradoNegro = es.toGPUShape(bs.createColorQuad(0.2,0.2,0.3))
        
        barra_tam = sg.SceneGraphNode("barra_tam")
        barra_tam.transform = tr.scale(0.15, 0.05, 0)
        barra_tam.childs += [gpuCuadradoNegro]
        
        barra_1 = sg.SceneGraphNode("barra_1")
        barra_1.transform = tr.translate(0.9, -0.5, 0)
        barra_1.childs += [barra_tam]
        
        barra_2 = sg.SceneGraphNode("barra_2")
        barra_2.transform = tr.translate(0.9, -0.7, 0)
        barra_2.childs += [barra_tam]
        
        barra_3 = sg.SceneGraphNode("barra_3")
        barra_3.transform = tr.translate(0.9, -0.9, 0)
        barra_3.childs += [barra_tam]
        
        boton_rojo = sg.SceneGraphNode("boton_rojo")
        boton_rojo.transform = tr.uniformScale(0.1)
        boton_rojo.childs += [gpuCuadradoRojo]
        
        boton_gris = sg.SceneGraphNode("boton_gris")
        boton_gris.transform = tr.uniformScale(0.1)
        boton_gris.childs += [gpuCuadradoGris]
        
        boton1 = sg.SceneGraphNode("boton1")
        boton1.transform = tr.translate(0.85, -0.5, 0)
        boton1.childs += [boton_rojo]
        
        boton2 = sg.SceneGraphNode("boton2")
        boton2.transform = tr.translate(0.85, -0.7, 0)
        boton2.childs += [boton_gris]
        
        boton3 = sg.SceneGraphNode("boton3")
        boton3.transform = tr.translate(0.85, -0.9, 0)
        boton3.childs += [boton_gris]
        
        boton1_mov = sg.SceneGraphNode("boton1_mov")
        boton1_mov.childs += [boton1]
        
        boton2_mov = sg.SceneGraphNode("boton2_mov")
        boton2_mov.childs += [boton2]
        
        boton3_mov = sg.SceneGraphNode("boton3_mov")
        boton3_mov.childs += [boton3]
        
        botones = sg.SceneGraphNode("botones")
        botones.childs += [barra_1, barra_2, barra_3, boton1_mov, boton2_mov , boton3_mov]
        
        self.model = botones
        self.boton1_mov = boton1_mov
        self.boton2_mov = boton2_mov
        self.boton3_mov = boton3_mov
        self.pos_inicial1 = 0
        self.pos_inicial2 = 0
        self.pos_inicial3 = 0
        self.mover_b1 = False
        self.mover_b2 = False
        self.mover_b3 = False
        
        
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')
        
        
    def b1(self):
        if self.mover_b2 and self.mover_b3:
            self.mover_b1 = True
            self.boton1_mov.transform = tr.translate(0.1, 0, 0)
            self.pos_inicial1 = -0.05
        elif self.mover_b1 == False:
            self.boton1_mov.transform = tr.translate(self.pos_inicial1, 0, 0)
        
    def b2(self):
        if self.mover_b2:
            self.boton2_mov.transform = tr.translate(0.1, 0, 0)
            self.pos_inicial2 = -0.05
        elif self.mover_b2 == False:
            self.boton2_mov.transform = tr.translate(self.pos_inicial2, 0, 0)
            
    def b3(self):
        if self.mover_b3:
            self.boton3_mov.transform = tr.translate(0.1, 0, 0)
            self.pos_inicial3 = -0.05
        elif self.mover_b3 == False:
            self.boton3_mov.transform = tr.translate(self.pos_inicial3, 0, 0)
        
        
        
        
    def presionar_botones(self, pipeline):
        self.b1()
        self.b2()
        self.b3()
        self.draw(pipeline)
        
            
            