# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 12:08:40 2020

@author: diegc
"""

from modelos3D import *
import glfw


class Controller():
    
    def __init__(self):
        self.model = None
        self.position = np.zeros(3)
        self.old_pos = 0, 0
        self.theta = np.pi * 0.5
        self.phi = 0.
        self.w = False
        self.s = False
        
    def set_model(self, m):
        self.model = m
        

    def update_angle(self, dy, dz, dt):
        # multiplo_inicial = self.theta // np.pi

        #self.phi -= dx * dt * self.mouse_sensitivity
        self.phi = dy 
        theta_0 = self.theta

        dtheta = -dz 
        self.theta += dtheta

        if self.theta < 0:
            self.theta = 0.01

        elif self.theta > np.pi:
            self.theta = 3.14159

        else:
            pass

        # if (self.theta + dtheta) // np.pi == multiplo_inicial:
        #     self.theta += dtheta

        return self.phi, self.theta

    #funcion para que el programa reaccione al dar comando con las teclas o clicks
    def on_key(self, window, key, scancode, action, mods):

        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return
        
        if key == glfw.KEY_ESCAPE:
            sys.exit()
    
        elif (action == glfw.PRESS or action == glfw.REPEAT):
            if( key == glfw.KEY_UP):
                if self.model.en_aire:
                    print("cabeceo Arriba")
                    self.model.cabeceo_up = True
                    self.model.moverAvion = True
                    if self.model.cabeceo_angulo >= 0:
                        self.model.move_up = True
                else:
                    print("No se puede maniobrar el avión en tierra")
                
            elif (key == glfw.KEY_DOWN):
                if self.model.en_aire:
                    print("Cabeceo Abajo")
                    self.model.cabeceo_down = True
                    self.model.moverAvion = True
                    if self.model.cabeceo_angulo <= 0:
                        self.model.move_down = True
                else:
                    print("No se puede maniobrar el avión en tierra")

            elif (key == glfw.KEY_RIGHT):
                if self.model.en_aire:
                    if self.model.pos_y > -1:
                        print("Girando Der.")
                        self.model.inclinacion_der = True
                        self.model.moverAvion = True
                        if self.model.angulo_inclinacion >= 0:
                            self.model.move_right = True
                else:
                    print("No se puede maniobrar el avión en tierra")

            elif (key == glfw.KEY_LEFT):
                if self.model.en_aire:
                    if self.model.pos_y < 1:
                        print("Girando Izq.")
                        self.model.inclinacion_izq = True
                        self.moverAvion = True
                        if self.model.angulo_inclinacion <= 0:
                            self.model.move_left = True
                else:
                    print("No se puede maniobrar el avión en tierra")
                    
            elif (key == glfw.KEY_W):
                self.w = True
                self.model.acelerar = True
                if self.model.en_aire:
                    self.model.moverAvion = True
                
            elif (key == glfw.KEY_S):
                self.s = True
                self.model.frenar = True
                if self.model.en_aire:
                    self.model.moverAvion = True
                    
            elif (key == glfw.KEY_J):
                if self.model.prender_apagar_todo == False:    
                    self.model.prender_apagar_todo = not self.model.prender_apagar_todo
                    print("Apagando todo")
                
                
            elif (key == glfw.KEY_K):
                
                if self.model.prender_apagar_motor == False:
                    print("Prendiendo Motor")
                elif self.model.prender_apagar_motor == True:
                    print("Apagando Motor")
                self.model.prender_apagar_motor = not self.model.prender_apagar_motor
                    
            
            elif (key == glfw.KEY_L):
                if self.model.prender_apagar_panel == False:
                    print("Prendiendo Panel")
                elif self.model.prender_apagar_panel == True:
                    print("Apagando Panel")
                self.model.prender_apagar_panel = not self.model.prender_apagar_panel

            elif (key == glfw.KEY_C):
                if self.model.camara1:
                    print("cambiando camara")
                    self.model.camara1 = False
                    self.model.camara2 = True
                elif self.model.camara2:
                    print("cambiando camara")
                    self.model.camara2 = False
                    self.model.camara3 = True
                elif self.model.camara3:
                    print("cambiando camara")
                    self.model.camara3 = False
                    self.model.camara1 = True
                
                
            
            elif (key == glfw.KEY_SPACE):
                
                if self.model.en_aire == True and self.model.velocidad < 50:
                    self.model.aterrizar = True
                    print("Aterrizando avión")
                    
                elif self.model.en_aire == False and self.model.velocidad > 50:
                    self.model.despegar = True
                    print("Despegando avión")
                else: print("ACCIÓN NO PERMITIDA, VERIFIQUE VELOCIDAD")
                    
                
            else:
                print('Unknown key')
        # Si se suelta la tecla el avión vuelve a su rotación inicial.
        elif(action == glfw.RELEASE):
            self.model.pos_inicial()
            self.w = False
            self.s = False
                
        # Cualquier otra tecla no la reconoce    
        else:
            print('Unknown key')

    def move(self, window, viewPos, forward, new_side, dt):
        if self.model.move_right:
            viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))

        elif self.model.move_left:
                viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))

        elif self.w and self.model.acelerar:
            viewPos += forward * 0.001

        elif self.s and self.model.frenar:
            viewPos -= forward * 0.001

        else:
            pass
