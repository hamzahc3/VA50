# VA50 - Interactive table

Mise en place d'un jeu interractif à partir d'un vidéo-projecteur.

# Concept

Défense de tours : l'utilisateur place des objets sur la table pour vaincre des ennemis vidéo-projetés.

# Matériel 

- Vidéo projecteur : dimensions 720x1280
- Trépied
- Caméra RGB + profondeur (RealSense)

# Langage

Langage utilisé : Python 3.10

Packages utilisés :

- **opencv-python**
- **pyrealsense2**
- numpy
- matplotlib
- time

# Fonctionnement

### Environnement

L'idéal est de se placer dans une salle peu éclairée pour que l'image vidéo-projetée soit la plus visuellement riche possible.

Ensemble vidéo projecteur - caméra sur le trépied sur la table.


### Calibration de la caméra

Une image d'abord entièrement noire est ouverte. Il faut la placer dans le champs de vidéo projecteur. Elle deviendra par la suite entièrement blanche pour que la caméra la détecte.
Le changement noir-blanc se fait automatiquement. La variable `TIME_LIMIT` permet de définir, en seconde, le temps avant le changement.

On utilise d'abord une image noire pour que la caméra puisse s'habituer à la luminosité de la pièce, puis le passage à l'image blanche permet à la caméra de se concentrer sur la forme de l'image vidéo-projetée.

Une détection des contours est faite. Lorsque l'image est blanche et que les contours sont stables, l'utilisateur **__appuie sur une touche clavier__** pour confirmer les contours, calculant ainsi la matrice perspective entre l'image projetée et l'image caméra.


### Détection d'objets

*Cette partie n'est pas encore implémentée.
Objectif : détecter via la profonder lorsqu'un objet est inséré dans le champ de la caméra, via une différence de profondeur entre une image de référence et l'image actuelle.*
