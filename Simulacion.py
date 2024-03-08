from typing import KeysView
import pygame
import random
import math
import time

pygame.font.init()
pygame.mixer.init()

from pygame.locals import *

#Ajustes Ventana
ANCHO = 2500
ALTO = 1400
pantalla =pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Simulacion")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
CIAN = (0,255,255)
PINK = (255,0,128)

BORDER = pygame.Rect(ANCHO//2 - 5, 0, 10, ALTO)

#Posicion pixel
x = ANCHO // 2
y = ALTO // 2

#Control de FPS
clock = pygame.time.Clock()

#Constante Gravitacion
g = 6.67E-11
#Constante de Coulomb
k = 9.98E9
#Carga Proton
qp = 1.6E-19
#Masa Proton
mp = 1.6725E-27
#Carga Electron
qe = -1.6E-19
#Masa Electron
me = 9.1095E-31
#Masa tierra
mt = 5.972E24
#Masa sol
ms = 1.089E30
# Lista para almacenar partículas
particulas = []

# Crear partícula
# Tiene que tener color, masa, coordenadas, velocidades y respecto a cada eje
def crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),dx=0,dy=0, um = 10000000000000,q=1, color = RED,r = 7):

    particulas.append({'xtemp':x,'ytemp':y,'x': x, 'y': y, 'dx': dx, 'dy': dy,'masa': um, 'color': color,'carga':q,'radio':r})

# Mover partículas
def mover_particula(particula):
    
    #Calculo fuerzas
    for otraparticula in particulas:
        if otraparticula != particula:
            
            #Calculo de la distancia euclidiana
            distx = otraparticula['x'] - particula['x']
            disty = otraparticula['y'] - particula['y']
            #Calculo de la distancia euclidiana
            distancia = math.sqrt(distx**2 + disty**2)
            
            if distancia <= particula['radio'] + otraparticula['radio']:
            
                # Calcula las nuevas velocidades
                v1x_new = (particula['dx'] * (particula['masa'] - otraparticula['masa']) + 2 * otraparticula['masa'] * otraparticula['dx']) / (particula['masa'] + otraparticula['masa']) 
                v1y_new = (particula['dy'] * (particula['masa'] - otraparticula['masa']) + 2 * otraparticula['masa'] * otraparticula['dy']) / (particula['masa'] + otraparticula['masa']) 
                
                v2x_new = (otraparticula['dx'] * (otraparticula['masa'] - particula['masa']) + 2 * particula['masa'] * particula['dx']) / (otraparticula['masa'] + particula['masa'])
                v2y_new = (otraparticula['dy'] * (otraparticula['masa'] - particula['masa']) + 2 * particula['masa'] * particula['dy']) / (otraparticula['masa'] + particula['masa'])
                
                # Actualiza las velocidades
                particula['dx'], particula['dy'] = v1x_new, v1y_new
                otraparticula['dx'], otraparticula['dy'] = v2x_new, v2y_new
                
                # Calcula la dirección de empuje para separar las partículas
                dx_norm = distx / distancia
                dy_norm = disty / distancia
                
                # Calcula la cantidad de superposición
                overlap = 1 + (particula['radio'] + otraparticula['radio']) - distancia
                
                # Empuja las partículas en direcciones opuestas proporcionalmente a sus masas
                particula['x'] -= (dx_norm * (overlap * (otraparticula['masa'] / (particula['masa'] + otraparticula['masa'])))) * 0.95
                particula['y'] -= (dy_norm * (overlap * (otraparticula['masa'] / (particula['masa'] + otraparticula['masa'])))) * 0.95
                otraparticula['x'] += (dx_norm * (overlap * (particula['masa'] / (particula['masa'] + otraparticula['masa'])))) * 0.95
                otraparticula['y'] += (dy_norm * (overlap * (particula['masa'] / (particula['masa'] + otraparticula['masa'])))) * 0.95
                
            
            else:
                    fgravedad = g * particula['masa']*otraparticula['masa']/distancia**2
                    
                    fgravedadx = fgravedad * distx / distancia
                    fgravedady = fgravedad * disty / distancia
                    particula['dx'] += fgravedadx / particula['masa']
                    particula['dy'] += fgravedady / particula['masa']
                    
                    
                    
                    felectrica = (k * particula['carga']*otraparticula['carga'])/distancia**2
                
                    felectricax = felectrica * distx / distancia
                    felectricay = felectrica * disty / distancia
                    
                    particula['dx'] -=felectricax / particula['masa']
                    particula['dy'] -=felectricay / particula['masa']
                    
                
            
    
    # Dibujar partícula
    pygame.draw.circle(pantalla, particula['color'], (particula['x'], particula['y']),particula['radio'],particula['radio'])   



# Crear una nueva partícula

#crear_particula(x=ANCHO//2,y=ALTO//2,um = 1200000000000, q = qp, r=40,color=BLUE)
#crear_particula(x=500,y=ALTO//2, q = qe,color=PINK,r=40)
#crear_particula(x=2000,y=ALTO//2, q = qe, color=CIAN,r=40)
#crear_particula(x=1250,y=150, q = qe,color=WHITE)
#crear_particula(color=BLUE,x=ANCHO//2,y=ALTO//2,um = 10000000000000)
for i in range(0,30):
    crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),um = mp, q = qp, r=15, color=PINK)
    crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),um = me, q = qe,color=CIAN)
    
#crear_particula(x=1000,y=500, um=1000000000000,color=BLUE)

#Bucle de la simulacion
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    
    #Teclas
    if keys[pygame.K_LEFT]:
        x -= 1
    if keys[pygame.K_RIGHT]:
        x += 1
    if keys[pygame.K_UP]:
        y -=1
    if keys[pygame.K_DOWN]:
        y +=1
        
    pantalla.fill(BLACK)
    
    
    pygame.draw.circle(pantalla,WHITE,(x,y),10,10)
    
    # Mover y dibujar todas las partículas

    for particula in particulas:
        mover_particula(particula)
    
    for particula in particulas:
        
        
        particula['x']  += particula['dx']
        particula['y']  += particula['dy']
        
    pygame.display.flip()
    
    clock.tick(1000)