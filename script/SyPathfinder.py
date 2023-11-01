# importation des modules
import random
import math

# definitions des constantes
DEVIATION_RATE    = 50 # pas de deviation definissant de combien des pas devrait etre la deviation
ANTICIPATION_RATE = 20 # Anticipation des obstacles

# Variable globale de memoire, stockant les coordonnees -t
last_details_x = 0
last_details_y = 0
walls          = []
cordo_X        = []  # Liste vide pour stocker les coordonnées X
cordo_Y        = []  # Liste vide pour stocker les coordonnées 
state_capture  = []
object_matrix  = []
stop_update    = False

class AgentPathfinder:
    # Constructeur
    def __init__(self, x:int or float, y:int or float, destination_details:tuple[int or float], step:int, obstacles:list[list]) -> None:
        self.x                   = x
        self.y                   = y
        self.destination_details = destination_details
        self.obstacles           = obstacles
        self.movement_step       = step
        self.actions             = ['north', 'south', 'east', 'west', 'northeast', 
                                    'southeast', 'southwest', 'northwest']
        self.high_parameter      = 0
        self.ismoving            = True
        self.memory              = x 
        
    # Méthode renvoyant le résultat final
    def init_agent(self) -> tuple:
        return self.gradual_approach()
    
    # Méthode pour générer des coordonnées circulaires 
    def generate_circle_coordinates(self, rayon : int = 5, nombre_points : int = 50):
        coordonnees = []
        angle = 0
        increment_angle = (2 * math.pi) / nombre_points

        for _ in range(nombre_points):
            x = self.x + (rayon * math.cos(angle))
            y = self.y + (rayon * math.sin(angle))
            coordonnees.append((x, y))
            angle += increment_angle

        return coordonnees
    
    # Méthode pour modéliser les obstacles
    def obstacles_modeling(self, substactor : int = 10, adder:int = 10):  
        modeling_vector = []
        for wall in self.obstacles:
            modeling_vector.append(wall[0][0] - substactor)
            modeling_vector.append(wall[0][1] + adder)
        
        return modeling_vector
        
     # Méthode pour ajuster la vitesse   
    def adjust_speed(self, speed = 1000):
        self.movement_step += speed #random.randint(2, 10)
    
     # Calcul de la distance entre deux points   
    def distance_calculation(self, a, b):
        # Théorème de PYTHAGORE : OM = sqrt(x^2 + y^2)
        OM = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
        return math.sqrt(OM)
           
    # Définition des actions        
    def north(self):
        self.y += self.movement_step * DEVIATION_RATE
    def south(self):
        self.y -= self.movement_step * DEVIATION_RATE
    def east(self):
        self.x += self.movement_step * DEVIATION_RATE
    def west(self):
        self.x -= self.movement_step * DEVIATION_RATE
    def northeast(self):
        self.y += self.movement_step * DEVIATION_RATE
        self.x += self.movement_step * DEVIATION_RATE
    def southeast(self):
        self.y -= self.movement_step * DEVIATION_RATE
        self.x += self.movement_step * DEVIATION_RATE
    def southwest(self):
        self.y -= self.movement_step * DEVIATION_RATE
        self.x -= self.movement_step * DEVIATION_RATE
    def northwest(self):
        self.y += self.movement_step * DEVIATION_RATE
        self.x -= self.movement_step * DEVIATION_RATE
    
    # Fonction pour mettre à jour les coordonnées selon le mouvement
    def Update_contact_details(self, a, b):  
        return a - self.movement_step if a > b else a + self.movement_step if a < b else a
    
    # Decode si a est plus grand, plus petit ou égal à b 
    def Decode_contact_details(slef,a, b):
        return False if a > b else True if a < b else None
    
    # declencheur des actions
    def trigger_action(self, act):
        if   act == 'north'      : self.north()
        elif act == 'south'      : self.south()
        elif act == 'east'       : self.east()
        elif act == 'west'       : self.west()
        elif act == 'northeast'  : self.northeast()
        elif act == 'southeast'  : self.southeast()
        elif act == 'southwest'  : self.southwest()
        else                     : self.northwest()
    
    
    def trigger_opposite_action(self, act):
        if act == 'north'      : self.south()
        if act == 'south'      : self.north()
        if act == 'east'       : self.west()
        if act == 'west'       : self.east()
        #if act == 'northeast'  : self.southwest()
        #if act == 'southeast'  : self.northwest()
        #if act == 'southwest'  : self.northeast()
        #if act == 'northhwest' : self.southeast()
        
     # Sauvegarder l'état   
    def save_state(self, state):
        if len(state_capture) < 10:
            state_capture.append(state)
        else:
            del state_capture[0]
            state_capture.append(state)
            
        
    # Définir une fonction Assessment qui simule le déplacement anticipé de l'agent et vérifie s'il rencontre l'obstacle ou atteint la destination
    def Assessment(self, coord:tuple[int or float]):
        global walls
        global stop_update
        x_dest , y_dest = coord[0], coord[1]
        
        
        for _ in range(ANTICIPATION_RATE):
            X = self.Update_contact_details(self.x, x_dest)
            Y = self.Update_contact_details(self.y, y_dest)
            
            if (self.x, self.y) == (x_dest, y_dest): # si l'agent bouge l'etat 'move' est enregistre
                self.save_state('move')
                break
            
            use_experience = False
            if (self.x, self.y) in walls and use_experience:
                    use_experience = True
                    stop_update = False
                    self.ismoving = False
                    self.save_state('move-1')
                    stop_update  = True
                    #self.high_parameter = wall[1]
                    self.adjust_speed()
                    virtual_x = self.Decode_contact_details(self.x, x_dest)
                    virtual_y = self.Decode_contact_details(self.y, y_dest)
                    x_act, y_act = None, None
                    
                    if virtual_x : x_act = 'east'
                    else         : x_act = 'west'
                    
                    if virtual_y : y_act = 'south'
                    else         : y_act = 'north'
                    
                    self.trigger_opposite_action(x_act)
                    self.trigger_opposite_action(y_act)
                    
            for wall in self.obstacles:
                
                if (X >= wall[0][0] and X <= wall[0][1]) and (Y > wall[1][0] and Y <= wall[1][1]) :
                    self.ismoving = False
                    self.save_state('move-1')
                    stop_update  = True
                    self.high_parameter = wall[1]
                    self.adjust_speed()
                    virtual_x = self.Decode_contact_details(self.x, x_dest)
                    virtual_y = self.Decode_contact_details(self.y, y_dest)
                    x_act, y_act = None, None
                    
                    if virtual_x : x_act = 'east'
                    else         : x_act = 'west'
                    
                    if virtual_y : y_act = 'south'
                    else         : y_act = 'north'
                    
                    self.trigger_opposite_action(x_act)
                    self.trigger_opposite_action(y_act)
                    break

                
            if last_details_x == (self.x, self.y):
                #stop_update  = True
                #self.ismoving = False
                self.save_state('trying')
                self.adjust_speed()
                if last_details_x not in walls and use_experience:
                    walls.append(last_details_x)
                index = random.randint(0, len(self.actions) - 1)
                action = self.actions[index]
                self.trigger_action(action)
            else:
                self.save_state('move')
            #if (X, Y) not in walls:
             #   self.adjust_speed()
     
    # Trouve la destination la plus proche        
    def find_the_nearest_destination(self) -> int:
        if len(self.destination_details) == 1:
            return 0
        small_value = 100**10
        index_and_value = ()
        for index, coord in enumerate(self.destination_details):
            if self.distance_calculation((self.x, self.y), coord) < small_value:
                small_value = self.distance_calculation((self.x, self.y), coord)
                index_and_value = (index, small_value)
     
        return index_and_value[0]
    
    
    # Trouve la valeur la plus proche dans une liste
    def near_value(self, b:int, a:list[int] = [550, 620, 750, 820, 950, 1020 ]) -> int: 
            return  min(a, key=lambda x:abs(x-b))
            
    # Trouve des coordonnées proches des obstacles
    def Get_around(self, coord:tuple[int or float]) -> tuple:
        refy = self.near_value(self.y, [145, 510])  
        refx = self.near_value(self.memory, self.obstacles_modeling())   
        return (refx, refy)

    
    # Methode reduisant graduellement la distance separant A et B
    def gradual_approach(self) -> tuple:
        global last_details_x, last_details_y, stop_update

        index = self.find_the_nearest_destination()
        coord = self.destination_details[index]
        
        self.Assessment(coord)
        current_contact_details_of_A = (self.x, self.y)
        current_contact_details_of_B = coord
        
        if state_capture[-1] == 'move':
            self.adjust_speed() 
        if self.y == 150 or self.y == 510:
            stop_update = False
            
            
        coord_of_get_around = self.Get_around(coord)
        refx = coord_of_get_around[0]
        refy = coord_of_get_around[1]
        
        # Mise-a-jour des coordonnees des x et y en les incrementant ou decrementant pour qu'il s'approche de la destination
        if stop_update and self.ismoving:
            Y = self.Update_contact_details(current_contact_details_of_A[1],
                                            refy)
            X = refx
        else:  
            Y = self.Update_contact_details(current_contact_details_of_A[1],
                                        current_contact_details_of_B[1])
            X = self.Update_contact_details(current_contact_details_of_A[0],
                                            current_contact_details_of_B[0])
        
        updated_contact_details_of_A = (X, Y)
        last_details_x = (self.x, self.y)
        last_details_y = coord
        print("learning : ", walls)
        return updated_contact_details_of_A # Retourne les coordonnées mises à jour
    