from typing import KeysView
import pygame
import random
import math

pygame.font.init()
pygame.mixer.init()

from pygame.locals import *

#Ajustes Ventana
ANCHO = 2800
ALTO = 1400
pantalla =pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Simulacion")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)

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
def crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),dx=0,dy=0, um = 10000000000000,q=1, color = RED):

    particulas.append({'x': x, 'y': y, 'dx': dx, 'dy': dy,'masa': um, 'color': color,'carga':q})

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

            
            
            #Calculo fuerza de gravedad ejercida sobre la particula
            if distancia > 40:

                fgravedad = g * particula['masa']*otraparticula['masa']/distancia**2           
                
                fgravedadx = fgravedad * distx / distancia
                fgravedady = fgravedad * disty / distancia
                
                particula['dx'] += fgravedadx / particula['masa']
                particula['dy'] += fgravedady / particula['masa']
                
            #Calculo fuerzas electromagneticas
            
            if distancia > 22:

                felectrica = (k * particula['carga']*otraparticula['carga'])/distancia**2
            
                felectricax = felectrica * distx / distancia
                felectricay = felectrica * disty / distancia
                
                particula['dx'] -=felectricax / particula['masa']
                particula['dy'] -=felectricay / particula['masa']
                
            
            
                
    particula['x']  += particula['dx']
    particula['y']  += particula['dy']
    

    
    
    
    # Dibujar partícula
    pygame.draw.circle(pantalla, particula['color'], (particula['x'], particula['y']),5,5)
    #for i in range(10,15):
    #    for j in range(10,5,-2):
    #        pygame.draw.rect(pantalla, particula['color'], (particula['x']-5, particula['y']-5, i, j))



# Crear una nueva partícula

#crear_particula(x=ANCHO//2,y=ALTO//2,um = mp, q = qp)
#crear_particula(x=1000,y=ALTO//2, q = qe)
#crear_particula(x=2000,y=ALTO//2, q = qe)
#crear_particula(x=1500,y=180, q = qe)
#crear_particula(color=BLUE,x=ANCHO//2,y=ALTO//2,um = 100000000000000)
for i in range(0,30):
    crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),um = mp, q = qp)
    crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),um = me, q = qe,color=BLUE)
    crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),um = me, q = qe,color=BLUE)
    crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),um = me, q = qe,color=BLUE)
#crear_particula(x=1000,y=500, um=1000000000000,color=BLUE)

#Bucle de la simulacion
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    numerox = + random.randint(-1,2)
    numeroy = + random.randint(-1,2)
    
    
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
    
    #pygame.draw.rect(pantalla,WHITE,(x,y,10,10))
    


    # Mover y dibujar todas las partículas
    for i, particula in enumerate(particulas):
        mover_particula(particula)
    pygame.display.flip()
    
    clock.tick(600)
    