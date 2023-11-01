# Agent Pathfinder

Ce programme Python implémente un agent pathfinder capable de se déplacer dans un environnement 2D entre un point de départ et une destination finale en évitant des obstacles.

## Fonctionnalités

- L'agent peut se déplacer dans 8 directions: nord, sud, est, ouest, nord-est, sud-est, sud-ouest, nord-ouest
- L'agent utilise une approche graduelle pour atteindre sa destination finale
- L'agent anticipe et évite les obstacles sur son chemin
- L'agent ajuste sa vitesse en fonction des obstacles rencontrés
- L'agent apprend de ses expériences passées pour éviter de se retrouver bloqué

## Modules 

Le programme utilise les modules Python suivants:

- `random`: pour générer des mouvements aléatoires
- `math`: pour les calculs géométriques

## Classes

La classe `AgentPathfinder` contient toute la logique de l'agent:

- `__init__`: Constructeur, initialise les attributs de l'agent
- `init_agent()`: Méthode principale, calcule et retourne le chemin final
- `gradual_approach()`: Approche graduelle de la destination
- `Assessment()`: Simule le déplacement et vérifie obstacles/destination
- `find_the_nearest_destination()`: Trouve destination la plus proche
- `adjust_speed()`: Ajuste la vitesse de l'agent
- `trigger_action()`: Déclenche le mouvement dans une direction
- `save_state()`: Sauvegarde l'état courant dans l'historique
- `Get_around()`: Trouve des coordonnées proches des obstacles
- `obstacles_modeling()`: Modélise les obstacles sous forme de vecteur

## Algorithm

L'algorithme principal est le suivant:

1. Initialiser la position de départ de l'agent
2. Tant que la destination n'est pas atteinte:
   1. Trouver la destination la plus proche
   2. Faire une simulation de déplacement vers la destination (Assessment)
   3. Ajuster la vitesse si nécessaire
   4. Mettre à jour la position courante 
   5. Sauvegarder l'état courant
3. Retourner le chemin final

L'agent apprend au fur et à mesure en sauvegardant les états et les obstacles rencontrés.

## Exécution

Pour exécuter le programme:

```
python environnement_of_agent..py
```
