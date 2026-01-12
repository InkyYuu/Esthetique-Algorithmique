from math import sin

SIZE_X = 640
SIZE_Y = 400

VITESSE = 0.10

def setup():
    size(SIZE_X, SIZE_Y)
    noStroke()
    
    # Mode couleur HSB :
    # Choisis pour faire les couleurs de l'arc en ciel plus facilement
    colorMode(HSB, 360, 100, 100, 100)

def draw():
    background(0, 0, 100)

    t = frameCount * VITESSE
    y = height / 2.0

    for x in range(0, width, 10):
        amplitude = map(mouseX, 0, width, 0, 250) #Map utilisé pour reborné la valeur entre 2 nouvelles valeurs (proportionnalité)
        frequence = map(mouseY, 0, height, 0.01, 0.20)
        signal = sin(x * frequence + t) #Courbe sinusoïdale
        h = 20 + (signal + 1) / 2.0 * amplitude #Hauteur du rectangle

        hue = (x * 0.7 + frameCount) % 360
        fill(hue, 90, 90, 70)

        rect(x, y - h/2.0, 10 * 0.8, h)
