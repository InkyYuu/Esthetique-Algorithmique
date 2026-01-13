SIZE_X, SIZE_Y = 250, 250
cellule = 4  # Taille d'une "cellule" en pixels

tAct = [[0.0 for x in range(SIZE_X)] for y in range(SIZE_Y)]
tPrec = [[0.0 for x in range(SIZE_X)] for y in range(SIZE_Y)]

def setup():
    size(cellule * SIZE_X, cellule * SIZE_Y)
    noStroke()
    colorMode(HSB, 360, 100, 100, 100)

def draw():
    step()
    show()

def step():
    global tAct, tPrec # Car on les swap plus tard
    for y in range(1, SIZE_Y - 1):
        for x in range(1, SIZE_X - 1):
            # Moyenne des 8 voisins
            moy_v = (tAct[y-1][x] + tAct[y-1][x-1] + tAct[y-1][x+1] + tAct[y][x-1] + tAct[y][x+1] + tAct[y+1][x] + tAct[y+1][x-1] + tAct[y+1][x+1]) / 8.0

            tPrec[y][x] = moy_v * 2.0 - tPrec[y][x] # Equation de l'onde (simplifié)

    tAct, tPrec = tPrec, tAct

def show():
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            c = tAct[y][x]

            hue = (200 + c * 200) % 360 # Bleu
            fill(hue, 100, 100, 100)

            rect(x * cellule, y * cellule, cellule, cellule)

def mousePressed():
    x = int(mouseX / cellule)
    y = int(mouseY / cellule)
    if 1 <= x < SIZE_X - 1 and 1 <= y < SIZE_Y - 1:
        # Impulsion
        tAct[y][x] = 2.0
