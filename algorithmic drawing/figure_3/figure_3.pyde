from math import sin

SIZE_X = 640
SIZE_Y = 400

V = [(0,0), (0,2), (2,-1)]
DIM_X = [0.0, 0.0, 0.0]
DIM_Y = [0.0, 0.0, 0.0]

def setup():
    size(SIZE_X, SIZE_Y)
    background(255)
    noFill()

    # Mode couleur HSB :
    # Choisis pour faire les couleurs de l'arc en ciel plus facilement
    colorMode(HSB, 360, 100, 100, 100)

    for i in range(3):
        DIM_X[i] = V[i][0] * SIZE_X / 15.0
        DIM_Y[i] = V[i][1] * SIZE_Y / 15.0

    strokeWeight(1)

def draw():
    t = frameCount * 2

    for x in range(1, 1100, 4):
        for i in range(3):
            xi = x + DIM_X[i]

            x1 = xi / 2.0
            y1 = xi / 10.0 * sin(xi / 20.0) + xi / 20.0 + SIZE_Y / 5.0
            x2 = 50.0 * sin((SIZE_X / xi) / 70.0) + SIZE_Y / 2.0
            y2 = xi / 4.0 * sin(xi / 120.0) + SIZE_X / 5.0

            hue = (t + x * 0.6 + i * 120) % 360
            stroke(hue, 100, 100, 20)

            line(x1, y1, x2, y2)
