# Esthetique-Algorithmique

Workshop "Esthétique &amp; Algorithmique" - S1 - IMAC1

Ce projet est réalisé avec **Processing** en utilisant le **mode Python**.

## Prérequis

- Processing installé
- Mode Python pour Processing
- **Python 3.10 recommandé**

<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; border-radius: 5px; font-family: Arial, sans-serif; color: #856404;">
    ⚠️&nbsp; Le mode Python de Processing est compatible avec <strong>Python 3.10</strong>. Si vous utilisez une version <strong>supérieure à 3.10</strong>, une configuration supplémentaire est nécessaire.
</div>

## Python > 3.10 – Correctif nécessaire

Avec les versions récentes de Python (3.11, 3.12, etc.), le **formatter automatique** du mode Python peut provoquer des erreurs.

### Solution

1. Ouvrir le dossier d’installation de Processing
2. Aller dans : `Processing/PythonMode/`
3. Repérer le dossier ou fichier nommé `formatter`
4. Supprimer le dossier ou renommer le `formatter_off`

Cela désactive le formatter et permet au mode Python de fonctionner correctement.

## Lancer les projets processing

1. Ouvrir Processing
2. Sélectionner **Python Mode**
3. Ouvrir le sketch
4. Cliquer sur **Run**

## Lancer le mini jeu Ace Attorney

1. Se placer dans le dossier `ace_attorney`
2. Installer les dépendances `pygame` et `pillow` si ce n'est pas déjà fait :
   ```bash
   pip install pygame pillow
   ```
3. Lancer le script `main.py` avec Python 3.12 de préférence (ou 3.10 si le correctif n'a pas été fait)
4. Profiter du jeu !

## Descriptions jour par jour

### Jour 1 - Dessin algorithmique

Etant un grand mélomane, j'ai choisi de faire une ligne audio où la fréquence de l'onde et l'amplitude varient en fonction de l'emplacement de la souris et un equalizer qui réagit également au placement de la souris.

### Jour 2 - Automates cellulaires

J'ai d'abord tenté de reproduire une onde sonore avec un automate cellulaire (moyenne de 8 voisins + formule de l'onde) puis j'ai ensuite fais une sorte de guerre de peinture entre plusieurs couleurs où la règle est que chaque cellule qui rencontre une autre couleur fait apparaître la couleur moyenne entre les deux.

### Jour 3 - Fractales

N'ayant pas trop d'idées, j'ai décidé de faire un mandelbrot classique avec quelques variations de couleurs en fonction du nombre d'itérations. Après cela j'ai fais un créateur de paysage fractal (avec plusieurs fractales et plusieurs animations)

### Jour 4 - Littérature numérique

J'ai d'abord décidé de faire l'algorithme love letter qui génère une lettre d'amour aléatoire en combinant des phrases pré-écrites. Ensuite je me suis lancé dans un projet plus ambitieux : un mini jeu de type Ace Attorney où l'on incarne un avocat de la défense qui doit prouver l'innocence de sa cliente accusée de meurtre. Le jeu est composé de dialogues, de scènes d'investigation et d'un procès où il faut présenter des preuves pour défendre sa cliente (pas entiérement terminé).

### Jour 5 - Projet libre

J'ai continué le mini jeu Ace Attorney en ajoutant plus de dialogues, des ajouts de fonctionnalités et j'ai créer un petit script spécial IMAC avec un scénario simple.

<div align="center" style="margin-top: 30px; font-size: 0.9em;"><p>Réalisé par <strong>Kellian Bredeau</strong>.</p> </div>
