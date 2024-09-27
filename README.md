# Agent Pathfinder

Ce programme Python implémente un agent pathfinder capable de se déplacer dans un environnement 2D entre un point de départ et une destination finale en évitant des obstacles.

## Fonctionnalités

- L'agent peut se déplacer dans 8 directions: nord, sud, est, ouest, nord-est, sud-est, sud-ouest, nord-ouest
- L'agent utilise une approche graduelle pour atteindre sa destination finale
- L'agent anticipe et évite les obstacles sur son chemin
- L'agent ajuste sa vitesse en fonction des obstacles rencontrés
- L'agent apprend de ses expériences passées pour éviter de se retrouver bloqué


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
