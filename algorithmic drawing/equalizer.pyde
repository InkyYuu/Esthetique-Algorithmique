SIZE_X = 640
SIZE_Y = 400

VITESSE = 0.02

def setup():
    size(SIZE_X, SIZE_Y)
    noStroke()
    
    # Mode couleur HSB :
    # Choisis pour faire les couleurs de l'arc en ciel plus facilement
    colorMode(HSB, 360, 100, 100, 100)
    
    noiseSeed(42) #IA utilisé pour remplacer un random trop violent

def draw():
    background(0, 0, 100)

    t = frameCount * VITESSE

    for x in range(0, width, 10):
        n = noise(x * 0.02, t)
        h = map(n, 0, 1, 40, 200)

        d = dist(mouseX, mouseY, x + 10 / 2, height - 10) #Calcule la distance entre le curseur et le bas du rectangle

        if d < 200: #Si on est à moins de 200px du bas
            facteur = 1 - d / 200 #On calcule un ratio pour que plus on soit vers le bas plus l'effet sera fort
            h += facteur * 200 #On applique une puissance supplémentaire

        hue = (x * 0.7 + frameCount) % 360
        fill(hue, 100, 100, 100)

        rect(x, height - h, 10 * 0.8, h)
