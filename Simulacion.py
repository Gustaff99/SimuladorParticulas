from typing import KeysView
import pygame
import random


pygame.font.init()
pygame.mixer.init()

from pygame.locals import *

#Ajustes Ventana
ANCHO = 2000
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

# Lista para almacenar partículas
particulas = []

# Crear partícula
# Tiene que tener masa, coordenadas, velocidades, aceleraciones y direcciones/modulos respecto a cada eje
def crear_particula(x=random.randint(0,ANCHO),y=random.randint(0,ALTO),dx=0,dy=0, um = 100000000000, color = RED):

    particulas.append({'x': x, 'y': y, 'dx': dx, 'dy': dy,'masa': um, 'color': color})

# Mover partículas
def mover_particula(particula):
    for otraparticula in particulas:
        if otraparticula != particula:
            
            distx = otraparticula['x'] - particula['x']
            disty = otraparticula['y'] - particula['y']
            #Calculo de la distancia euclidiana
            distancia = (distx**2 + disty**2)**(1/2)

            
            
            #Calculo fuerza aceleracion gravitatoria ejercida sobre la particula
            if distancia > 400:

                fgravedad = g * particula['masa']*otraparticula['masa']/(distancia)**2           
                
                fgravedadx = fgravedad * distx / distancia
                fgravedady = fgravedad * disty / distancia
                
                particula['dx'] += fgravedadx / particula['masa']
                particula['dy'] += fgravedady / particula['masa']
                
    particula['x']  += particula['dx']
    particula['y']  += particula['dy']
    
    # Dibujar partícula
    pygame.draw.rect(pantalla, particula['color'], (particula['x']-5, particula['y']-5, 10, 10))
    #for i in range(10,15):
    #    for j in range(10,5,-2):
    #        pygame.draw.rect(pantalla, particula['color'], (particula['x']-5, particula['y']-5, i, j))



# Crear una nueva partícula

crear_particula(x=400,y=500,um = 1000000000000)
crear_particula(x=1600,y=500,um = 1000000000000)
crear_particula(x=1000,y=0,um = 1000000000000)
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
    
    pygame.draw.rect(pantalla,WHITE,(x,y,10,10))
    


    # Mover y dibujar todas las partículas
    for particula in particulas:
        mover_particula(particula)
    pygame.display.flip()
    
    clock.tick(600)
    