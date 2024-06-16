import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from skimage import io
import numpy as np

vermelho, verde, azul = 1.0, 1.0, 1.0
rotacao_x, rotacao_y = 0.0, 0.0
translacao_x, translacao_y, translacao_z = 0.0, 0.0, 0.0
escalaX, escalaY, escalaZ = 1.0,1.0,1.0


def carrega_textura(imagem):
    try:
        
        superficie_textura = io.imread(imagem)
        
        carrega_textura = np.flipud(superficie_textura).astype(np.uint8).tobytes()
        
        id_textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id_textura)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, superficie_textura.shape[1], superficie_textura.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, carrega_textura)
        
        return id_textura
    except Exception as e:
        print(f"Erro ao carregar a textura: {e}")
        return None
    
def ajusta_rgb(texturas, imagens, vermelho, verde, azul):
    for id_textura, imagem in zip(texturas, imagens):
        glBindTexture(GL_TEXTURE_2D, id_textura)
        superficie_textura = io.imread(imagem)

        ajustar_imagem = np.clip(superficie_textura * [vermelho, verde, azul], 0, 255).astype(np.uint8)
        carrega_textura = np.flipud(ajustar_imagem).tobytes()
        
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, ajustar_imagem.shape[1], ajustar_imagem.shape[0], GL_RGB, GL_UNSIGNED_BYTE, carrega_textura)


def cubo(texturas):
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    superficies = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
    )

    cordenadas_poligono = (
        (1, 0),
        (1, 1),
        (0, 1),
        (0, 0)
    )

    for i, superficie in enumerate(superficies):
        glBindTexture(GL_TEXTURE_2D, texturas[i])
        glBegin(GL_QUADS)
        for j, vertice in enumerate(superficie):
            glTexCoord2fv(cordenadas_poligono[j])
            glVertex3fv(vertices[vertice])
        glEnd()

def piramide(texturas):
    glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    vertices = (
        (0, 1, 0),         
        (-0.5, 0, 0.5),    
        (0.5, 0, 0.5),     
        (0.5, 0, -0.5),    
        (-0.5, 0, -0.5)  
    )

    superficies = (
        (1, 2, 3, 4),  
        (0, 1, 2),     
        (0, 2, 3),     
        (0, 3, 4),     
        (0, 4, 1)    
    )

    cordenadas_poligono_base = (
        (0, 0),   
        (1, 0),    
        (1, 1),   
        (0, 1)    
    )

    cordenadas_poligono_lados = (
        (0.5, 1),  
        (0, 0),    
        (1, 0) 
    )

    for i, superficie in enumerate(superficies):
        glBindTexture(GL_TEXTURE_2D, texturas[i % len(texturas)])
        glBegin(GL_QUADS if i == 0 else GL_TRIANGLES)
        for j, vertice in enumerate(superficie):
            if i == 0:  
                glTexCoord2fv(cordenadas_poligono_base[j])
            else:     
                glTexCoord2fv(cordenadas_poligono_lados[j])
            glVertex3fv(vertices[vertice])
        glEnd()

def octaedro(texturas):
    glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    
    vertices = (
        (0, 1, 0),   
        (0.5, 0, 0.5), 
        (-0.5, 0, 0.5),  
        (0.5, 0, -0.5), 
        (-0.5, 0, -0.5), 
        (0, -1, 0)  
    )

    superficies = (
        (0, 1, 2),  
        (0, 3, 1),  
        (0, 4, 3), 
        (0, 2, 4),  
        (5, 1, 3), 
        (5, 3, 4), 
        (5, 4, 2),  
        (5, 2, 1)   
    )

    cordenadas_poligono = (
        (0.5, 1),  
        (1, 0),    
        (0, 0)     
    )
    
    for i, superficie in enumerate(superficies):
        glBindTexture(GL_TEXTURE_2D, texturas[i % len(texturas)])
        glBegin(GL_TRIANGLES)
        for j, vertice in enumerate(superficie):
            glTexCoord2fv(cordenadas_poligono[j])
            glVertex3fv(vertices[vertice])
        glEnd()

def dodecaedro(texturas):
    glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    vertices = [
        (-1.6180, 0, 0.6180), (-1.6180, 0, -0.6180), (1.6180, 0, -0.6180), (1.6180, 0, 0.6180), (0.6180, -1.6180, 0),
        (-0.6180, -1.6180, 0), (-0.6180, 1.6180, 0), (0.6180, 1.6180, 0), (0, 0.6180, -1.6180), (0, -0.6180, -1.6180),
        (0, -0.6180, 1.6180), (0, 0.6180, 1.6180), (-1.0806, -1.0806, 1.0806), (-1.0806, -1.0806, -1.0806),
        (1.0806, -1.0806, -1.0806), (1.0806, -1.0806, 1.0806), (-1.0806, 1.0806, 1.0806), (-1.0806, 1.0806, -1.0806),
        (1.0806, 1.0806, -1.0806), (1.0806, 1.0806, 1.0806)
    ]

    superficies = [
        (0, 12, 10, 11, 16), (1, 17, 8, 9, 13), (2, 14, 9, 8, 18), (3, 19, 11, 10, 15),
        (4, 14, 2, 3, 15), (5, 12, 0, 1, 13), (6, 17, 1, 0, 16), (7, 19, 3, 2, 18),
        (8, 17, 6, 7, 18), (9, 14, 4, 5, 13), (10, 12, 5, 4, 15), (11, 19, 7, 6, 16)
    ]

    cordenadas_poligono = [
        (0.5, 1),  
        (1, 0.75),  
        (0.85, 0), 
        (0.15, 0),  
        (0, 0.75)   
    ]

    for i, superficie in enumerate(superficies):
        glBindTexture(GL_TEXTURE_2D, texturas[i % len(texturas)])
        glBegin(GL_POLYGON)
        for j, vertice in enumerate(superficie):
            glTexCoord2fv(cordenadas_poligono[j % len(cordenadas_poligono)])
            glVertex3fv(vertices[vertice])
        glEnd()
    

def icosaedro(texturas):
    glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    
    vertices = (
        (-0.5257, 0.0, 0.8506), (0.5257, 0.0, 0.8506),
(-0.5257, 0.0, -0.8506), (0.5257, 0.0, -0.8506),
(0.0, 0.8506, 0.5257), (0.0, 0.8506, -0.5257),
(0.0, -0.8506, 0.5257), (0.0, -0.8506, -0.5257),
(0.8506, 0.5257, 0.0), (-0.8506, 0.5257, 0.0),
(0.8506, -0.5257, 0.0), (-0.8506, -0.5257, 0.0)
    )

    
    superficies = (
       (0,4,1), (0,9,4), (9,5,4), (4,5,8), (4,8,1),
(8,10,1), (8,3,10), (5,3,8), (5,2,3), (2,7,3),
(7,10,3), (7,6,10), (7,11,6), (11,0,6), (0,1,6),
(6,1,10), (9,0,11), (9,11,2), (9,2,5), (7,2,11)
    )
    
    cordenadas_poligono = (
        (0.5, 0), 
        (1, 1),   
        (0, 1)     
    )

    for i, superficie in enumerate(superficies):
        glBindTexture(GL_TEXTURE_2D, texturas[i % len(texturas)])
        glBegin(GL_TRIANGLES)
        for j, vertice in enumerate(superficie):
            glTexCoord2fv(cordenadas_poligono[j])
            glVertex3fv(vertices[vertice])
        glEnd()

def reseta():
    global vermelho, verde, azul, rotacao_x, rotacao_y, translacao_x, translacao_y, translacao_z, escalaX, escalaY, escalaZ
    vermelho = 1.0
    verde = 1.0
    azul = 1.0
    translacao_z = 0
    translacao_y = 0
    translacao_x = 0
    escalaX = 1.0
    escalaY = 1.0
    escalaZ = 1.0
    rotacao_x = 0
    rotacao_y = 0


def main():
    global vermelho, verde, azul, rotacao_x, rotacao_y, translacao_x, translacao_y, translacao_z, escalaX, escalaY, escalaZ, estado
    estado = 0
    pygame.init()
    display = (1000, 750)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    
    glEnable(GL_TEXTURE_2D)
    imagens = ['cachoro.png', 'gato.png', 'hamster.png', 'peixe.png', 'girafa.png','pantera.png',
                   'pinguin.png','micodourado.png', 
                   'leoneve.png', 'canguru.png','cobra.png', 'lontra.png', 
                   'ornitorrinco.png','picapau.png','leopardo.png', 'pelicano.png', 'camelo.png', 
                   'jacare.png',  'aguia.png','rinoceronte.png'] 
    
    texturas = [carrega_textura(imagem) for imagem in imagens]
    
    glDisable(GL_BLEND)

    glEnable(GL_DEPTH_TEST)

    if None in texturas:
        print("Erro: Alguma(s) textura(s) não pôde(ram) ser carregada(s).")
        return

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   

        if keys[pygame.K_1]:
            vermelho += 0.1
        elif keys[pygame.K_2]:
            vermelho -= 0.1
        elif keys[pygame.K_3]:
            verde += 0.1
        elif keys[pygame.K_4]:
            verde -= 0.1
        elif keys[pygame.K_5]:
            azul += 0.1
        elif keys[pygame.K_6]:
            azul -= 0.1

        if keys[pygame.K_LEFT]:
            rotacao_y += 1
        elif keys[pygame.K_RIGHT]:
            rotacao_y -= 1
        elif keys[pygame.K_UP]:
            rotacao_x += 1
        elif keys[pygame.K_DOWN]:
            rotacao_x -= 1
        
        if keys[pygame.K_w]:
            translacao_y += 0.1
        elif keys[pygame.K_s]:
            translacao_y -= 0.1
        elif keys[pygame.K_a]:
            translacao_x -= 0.1
        elif keys[pygame.K_d]:
            translacao_x += 0.1
        elif keys[pygame.K_e]:
            translacao_z += 0.1
        elif keys[pygame.K_q]:
            if translacao_z > -45.80000000000038:
                translacao_z -= 0.1

        if keys[pygame.K_z]:
            escalaX += 0.1
        elif keys[pygame.K_v]:
            if escalaX > 0.10000000000000014:
                escalaX -= 0.1
        elif keys[pygame.K_x]:
            escalaY += 0.1
        elif keys[pygame.K_b]:
            if escalaY > 0.10000000000000014:
                escalaY -= 0.1      
        elif keys[pygame.K_c]:
            escalaZ += 0.1
        elif keys[pygame.K_n]:
            if escalaZ > 0.10000000000000014:
                escalaZ -= 0.1  
        elif keys[pygame.K_i]:
            reseta()
        elif keys[pygame.K_KP0]:
            reseta()
            estado = 0
        elif keys[pygame.K_KP1]:
            reseta()
            estado = 1
        elif keys[pygame.K_KP2]:
            reseta()
            estado = 2
        elif keys[pygame.K_KP3]:
            reseta()
            estado = 3
        elif keys[pygame.K_KP4]:
            reseta()
            estado = 4 

        ajustar_cor = any(keys[key] for key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_i,
        pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3])
        
        espaco_pressionado = keys[pygame.K_SPACE]
        
        if ajustar_cor:
            
            if vermelho < 0.1:
                vermelho = 0.1
            if verde < 0.1:
                verde = 0.1
            if azul < 0.1:
                azul = 0.1
            
            ajusta_rgb(texturas, imagens, vermelho, verde, azul)
        
        if espaco_pressionado:

            ajusta_rgb(texturas, imagens, 1.0, 1.0, 1.0)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glScalef(escalaX, escalaY, escalaZ)
        glTranslatef(translacao_x, translacao_y, translacao_z)
        glRotatef(rotacao_x, 1, 0, 0)
        glRotatef(rotacao_y,0, 1, 0)  
        if estado == 0:
            cubo(texturas)
        elif estado == 1:
            piramide(texturas)
        elif estado == 2:
            octaedro(texturas)
        elif estado == 3:
            dodecaedro(texturas)
        elif estado == 4:        
            icosaedro(texturas)         
    
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()