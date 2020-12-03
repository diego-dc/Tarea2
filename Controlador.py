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
        self.panel = None
        self.perillas = None
        self.botones = None
        self.indicadores = None

        self.position = np.zeros(3)
        self.old_pos = 0, 0
        self.theta = np.pi * 0.5
        self.phi = 0.
        self.w = False
        self.s = False
        
    def set_model(self, m):
        self.model = m
    
    def set_adjuntos(self, panel, perillas, botones, indicadores):
        self.panel = panel
        self.perillas = perillas
        self.botones = botones 
        self.indicadores = indicadores

    def update_angle(self, dy, dz):

        #nuestro Phi será fijo, pues queremos mirar siempre hacia delante
        self.phi = dy 

        #Fijamos un theta inicial, que será como inicia la cámara
        theta_0 = np.pi * 0.5

        #Variamos el theta sólo en ciertos ángulos.
        dtheta = -dz
        if self.theta + dtheta > theta_0 and self.theta + dtheta < theta_0 + 0.18:
            self.theta += dtheta
            self.panel.theta += dtheta
            self.panel.Rotacion.transform = tr.rotationY(self.panel.theta)
            self.perillas.Rotacion.transform = tr.rotationY(self.panel.theta)
            self.indicadores.Rotacion.transform = tr.rotationY(self.panel.theta)
            self.botones.Rotacion.transform = tr.rotationY(self.panel.theta)

        if self.theta < 0:
            self.theta = 0.01
        
        #Esto por si queremos que la camara vuelva a la posición theta_0 una vez se estabiliza.
        #elif self.model.cabeceo_angulo == 0 and theta_0 + 0.1 > self.theta == theta_0:
        #    self.theta -= 0.001

        elif self.theta > np.pi:
            self.theta = 3.14159

        else:
            pass

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
                    if self.model.prender_apagar_motor == False and self.model.prender_apagar_panel == False:
                        print("Ya está todo apagado")
                        self.model.prender_apagar_todo = False
                elif self.model.prender_apagar_todo == True:    
                    self.botones.mover_b1 = False
                    self.model.prender_apagar_panel = False
                    self.model.prender_apagar_motor = False
                    self.model.prender_apagar_todo = False
                
                
                
            elif (key == glfw.KEY_K):
                self.model.prender_apagar_motor = not self.model.prender_apagar_motor
                if self.model.prender_apagar_motor:
                    self.botones.mover_b2 = True
                elif self.model.prender_apagar_motor == False:
                    self.botones.mover_b2 = False
                    self.perillas.apagar = True
                if self.model.prender_apagar_motor == False:
                    print("Prendiendo Motor")
                elif self.model.prender_apagar_motor == True:
                    print("Apagando Motor")
                
                    
            
            elif (key == glfw.KEY_L):
                self.perillas.apagar = not self.perillas.apagar
                self.indicadores.apagar = not self.indicadores.apagar
                self.botones.mover_b3 = not self.botones.mover_b3
                if self.perillas.apagar == False:
                    print("Prendiendo Panel")
                elif self.perillas.apagar == True:
                    print("Apagando Panel")

            elif (key == glfw.KEY_P):
                self.panel.mostrar_panel = not self.panel.mostrar_panel
                
                
            
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

    #Función que moverá la cámara junto al movimiento del avión.
    def move(self, window, viewPos, forward, dt):
        if self.model.move_right:
            if self.model.move_up:
                viewPos[2] += -(0.001 * (self.model.cabeceo_angulo * 0.03))
                self.panel.pos_z += -(0.001 * (self.model.cabeceo_angulo * 0.03))
                self.perillas.pos_z, self.botones.pos_z, self.indicadores.pos_z = viewPos[2], viewPos[2] , viewPos[2] + 0.005 # Esto solo para evitar un pequeño bug al bajar la camara en los indicadores. (Se superponen figuras)
            elif self.model.move_down:
                viewPos[2] -= 0.001 * (self.model.cabeceo_angulo * 0.025 )
                self.panel.pos_z -= 0.001 * (self.model.cabeceo_angulo * 0.025 )
                self.perillas.pos_z, self.botones.pos_z, self.indicadores.pos_z = viewPos[2], viewPos[2] , viewPos[2] + 0.005
            viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))
            self.panel.pos_y -= (0.001 * (self.model.angulo_inclinacion * 0.03))
            self.perillas.pos_y, self.botones.pos_y, self.indicadores.pos_y = viewPos[1], viewPos[1], viewPos[1]

        elif self.model.move_left:
            if self.model.move_up:
                viewPos[2] += -(0.001 * (self.model.cabeceo_angulo * 0.03))
                self.panel.pos_z += -(0.001 * (self.model.cabeceo_angulo * 0.03))
                self.perillas.pos_z, self.botones.pos_z, self.indicadores.pos_z = viewPos[2], viewPos[2] , viewPos[2] + 0.005
            elif self.model.move_down:
                viewPos[2] -= 0.001 * (self.model.cabeceo_angulo * 0.025 )
                self.panel.pos_z -= 0.001 * (self.model.cabeceo_angulo * 0.025 )
                self.perillas.pos_z, self.botones.pos_z, self.indicadores.pos_z = viewPos[2], viewPos[2] , viewPos[2] + 0.005
            viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))
            self.panel.pos_y -= (0.001 * (self.model.angulo_inclinacion * 0.03))
            self.perillas.pos_y, self.botones.pos_y, self.indicadores.pos_y = viewPos[1], viewPos[1], viewPos[1]

        elif self.model.move_up:
            if self.model.move_right:
                viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.panel.pos_y -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.perillas.pos_y, self.botones.pos_y, self.indicadores.pos_y = viewPos[1], viewPos[1], viewPos[1]
            elif self.model.move_left:
                viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.panel.pos_y -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.perillas.pos_y, self.botones.pos_y, self.indicadores.pos_y = viewPos[1], viewPos[1], viewPos[1]
            viewPos[2] += -(0.001 * (self.model.cabeceo_angulo * 0.03))
            self.panel.pos_z += -(0.001 * (self.model.cabeceo_angulo * 0.03))
            self.perillas.pos_z, self.botones.pos_z, self.indicadores.pos_z = viewPos[2], viewPos[2] , viewPos[2] + 0.005

        elif self.model.move_down:
            if self.model.move_right:
                viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.panel.pos_y -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.perillas.pos_y, self.botones.pos_y, self.indicadores.pos_y = viewPos[1], viewPos[1], viewPos[1]
            elif self.model.move_left:
                viewPos[1] -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.panel.pos_y -= (0.001 * (self.model.angulo_inclinacion * 0.03))
                self.perillas.pos_y, self.botones.pos_y, self.indicadores.pos_y = viewPos[1], viewPos[1], viewPos[1]
            viewPos[2] -= 0.001 * (self.model.cabeceo_angulo * 0.025 )
            self.panel.pos_z -= 0.001 * (self.model.cabeceo_angulo * 0.025 )
            self.perillas.pos_z, self.botones.pos_z, self.indicadores.pos_z = viewPos[2], viewPos[2] , viewPos[2] + 0.005

        elif self.w and self.model.acelerar:
            viewPos += forward * 0.0001
            self.panel.pos_x +=  0.0001
            self.perillas.pos_x += 0.0001
            self.indicadores.pos_x += 0.0001
            self.botones.pos_x += 0.0001


        elif self.s and self.model.frenar:
            viewPos -= forward * 0.0001
            self.panel.pos_x -=  0.0001
            self.perillas.pos_x -= 0.0001
            self.indicadores.pos_x -= 0.0001
            self.botones.pos_x -= 0.0001

        else:
            pass
