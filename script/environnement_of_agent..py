import pygame
import random
import numpy as np
from SyPathfinder import AgentPathfinder

# Initialisation de Pygame
pygame.init()

class Hider:
    def __init__(self, x, y, longeur, largeur) -> None:
        self.x = x
        self.y = y
        self.longeur = longeur
        self.largeur = largeur
      
    def born(self):
        return  pygame.Rect(self.x,self.y,self.longeur, self.largeur)
    
    def shit(self, j1, j2):
        if j1.colliderect(j2):
            valeur = 700
            while valeur >= 550 and valeur <= 850:
                valeur = random.randint(150, 1200)
                valeur2 = random.randint(100, 550)
            j2.x, j2.y = valeur, valeur2  # Réinitialise la position de l'ordinateur
    def move(self, player, speed):
        deplacement_x = random.randint(-speed, speed)
        deplacement_y = random.randint(-speed, speed)
        player.x += deplacement_x
        player.y += deplacement_y
        
    def display(self, disp, color, player):
        pygame.draw.rect(disp, color, player)
    

        
# Paramètres du jeu
largeur, hauteur = 1350, 670
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Cache-cache")

# Couleurs
blanc = (255, 255, 255)
bleu = (0, 0, 255)
rouge = (255, 0, 0)
gray = (232,232,232)
pink = (240, 210,239)
color_of_seeker = '#FF6CBA'
color_of_hider = '#38FF7D'
gray_balck = '#FFF200'
color_of_wall = '#B8B8B8'

# Avatars
#joueur_image = pygame.image.load("hider.png")  
joueur = pygame.Rect(250, 200, 40, 40)

model = Hider(700, 500, 40, 40)
ordinateur = model.born()
ordinateur2 = model.born()


# Variables de jeu
vitesse_joueur = 1

# Murs [X, Y, largeur, longeur]
murs = [ pygame.Rect(100, 70, 60, 300), # mur de gauche
         pygame.Rect(100, 60, 1190, 60), # mur du haut
         pygame.Rect(1230, 100, 60, 500), # mur de droite
         pygame.Rect(100, 600, 1190, 60)] # Mur du bas

obstacles = [# pygame.Rect(500, 200,20, 10),
         pygame.Rect(400, 250, 5, 200),
         pygame.Rect(600, 250, 10, 200),
         pygame.Rect(800, 250, 10, 200),
         pygame.Rect(1000, 250, 10, 200)
         ]

walls =np.array([
    # xmin xmax   ymin ymax
    [[560, 610], [215, 440]],
    [[760, 810], [215, 440]],
    [[960, 1010],[215, 440]],
    [[360, 405], [215, 440 ]]
])

# Boucle principale
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Déplacement du joueur
    touches = pygame.key.get_pressed()
    dx, dy = 0, 0

    paramettres = joueur.x, joueur.y
    agent = AgentPathfinder(joueur.x, joueur.y, [(ordinateur.x, ordinateur.y)],
                     5, walls)
    
    position = agent.init_agent()
    print("X,Y ordinateur", ordinateur.x, ordinateur.y)
    
    #joueur.x = position[0][0]
    #joueur.y = position[0][1]
    
    if paramettres[0] > position[0]:
        dx = -vitesse_joueur
    else:
        dx = vitesse_joueur
    if paramettres[1] > position[1]:
        dy = -vitesse_joueur
    else:
        dy = vitesse_joueur
        
    import time
    #time.sleep(0.00005)

    # Vérifier les collisions avec les murs pour le joueur
    future_position_joueur = joueur.move(dx, dy)
    collision = False

    for mur in murs:
        if future_position_joueur.colliderect(mur):
            collision = True
            break
    for obj in obstacles:
        if future_position_joueur.colliderect(obj):
            collision = True
            pygame.draw.rect(ecran, bleu, joueur)
            pygame.display.flip()
            break

    if not collision:
        joueur.x = future_position_joueur.x
        joueur.y = future_position_joueur.y

    #model.move(ordinateur, vitesse_joueur)
    #model.move(ordinateur2, vitesse_joueur)

    dx2 , dy2 = 0,0
    if touches[pygame.K_LEFT]:
        dx2 = -5
    if touches[pygame.K_RIGHT]:
        dx2 = 5
    if touches[pygame.K_UP]:
        dy2 = -5
    if touches[pygame.K_DOWN]:
        dy2 = 5
    # Déplacement aléatoire de l'ordinateur
    deplacement_x = dx2
    deplacement_y = dy2

    # Vérifier les collisions avec les murs pour l'ordinateur
    #future_position_ordinateur = ordinateur.move(deplacement_x, deplacement_y)
    #collision = False

    #ordinateur.x += deplacement_x
    #ordinateur.y += deplacement_y
    
    future_hider = ordinateur.move(dx2, dy2)
    
    collision = False

    for mur in murs:
        if future_hider.colliderect(mur):
            collision = True
            break
    for obj in obstacles:
        if future_hider.colliderect(obj):
            collision = True
            #pygame.draw.rect(ecran, bleu, joueur)
            #pygame.display.flip()
            break

    if not collision:
        ordinateur.x = future_hider.x
        ordinateur.y = future_hider.y


    # Limites de l'écran
    joueur.x = max(0, min(largeur - joueur.width, joueur.x))
    joueur.y = max(0, min(hauteur - joueur.height, joueur.y))
    print(joueur.x, joueur.y)

    ordinateur.x = max(0, min(largeur - ordinateur.width, ordinateur.x))
    ordinateur.y = max(0, min(hauteur - ordinateur.height, ordinateur.y))
    model.shit(joueur, ordinateur2)
    model.shit(joueur, ordinateur)

    # Effacer l'écran
    ecran.fill(blanc)

    # Dessiner les murs
    for mur in murs:
        pygame.draw.rect(ecran, color_of_wall, mur)
    
    for obj in obstacles:
        pygame.draw.rect(ecran, gray_balck, obj)

    # Dessiner les avatars
    pygame.draw.rect(ecran, color_of_seeker, joueur)
    pygame.draw.rect(ecran, color_of_hider, ordinateur)
    #pygame.draw.rect(ecran, color_of_hider, ordinateur2)
    #model.display(ecran, bleu, ordinateur2)

    # Mettre à jour l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
