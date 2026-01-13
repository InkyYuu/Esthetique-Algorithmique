import random
from math import atan2, pi

SIZE_X, SIZE_Y = 150, 150
cellule = 4

tAct  = [[0.0 for x in range(SIZE_X)] for y in range(SIZE_Y)]
tPrec = [[0.0 for x in range(SIZE_X)] for y in range(SIZE_Y)]

WHITE = 0.0

GROW_STEPS   = 45   # Taille de la tâche
RADIUS       = 7    # Rayon
SPREAD_TRIES = 2    # Tentatives de propagation par cellule colorée / frame

def setup():
    size(cellule * SIZE_X, cellule * SIZE_Y)
    noStroke()
    colorMode(HSB, 360, 100, 100, 100)

def draw():
    step()
    show()

def hue_from_click(x, y):
    # Répartir les couleurs en fonction des coordonnées
    cx = (SIZE_X - 1) * 0.5
    cy = (SIZE_Y - 1) * 0.5
    a = atan2(y - cy, x - cx)          # [-pi, pi]
    h = (a + pi) * (360.0 / (2.0 * pi))  # [0, 360)
    return 360.0 if h == 0 else h

def mix_hue(h1, h2):
    if h1 == WHITE: return h2
    if h2 == WHITE: return h1
    d = abs(h1 - h2)
    if d > 180:
        if h1 < h2: h1 += 360
        else:       h2 += 360
    m = (h1 + h2) * 0.5
    m = m % 360.0
    return 360.0 if m == 0 else m

def deposit_blob(cx, cy, h):
    r2 = RADIUS * RADIUS
    for _ in range(GROW_STEPS):
        dx = random.randint(-RADIUS, RADIUS)
        dy = random.randint(-RADIUS, RADIUS)
        if dx*dx + dy*dy > r2:
            continue
        x = cx + dx
        y = cy + dy
        if 1 <= x < SIZE_X-1 and 1 <= y < SIZE_Y-1:
            if tAct[y][x] == WHITE:
                tAct[y][x] = h
            else:
                tAct[y][x] = mix_hue(tAct[y][x], h)

def step():
    global tAct, tPrec

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            tPrec[y][x] = tAct[y][x]

    for y in range(1, SIZE_Y - 1):
        for x in range(1, SIZE_X - 1):
            h = tAct[y][x]
            if h <= 0:
                continue

            for _ in range(SPREAD_TRIES):
                nx = x + random.randint(-1, 1)
                ny = y + random.randint(-1, 1)
                if nx == x and ny == y:
                    continue

                v = tAct[ny][nx]
                if v == WHITE:
                    tPrec[ny][nx] = h
                else:
                    tPrec[ny][nx] = mix_hue(v, h)

    tAct, tPrec = tPrec, tAct

def show():
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            v = tAct[y][x]
            if v == WHITE:
                fill(0, 0, 100, 100)
            else:
                fill(v, 90, 95, 100)
            rect(x * cellule, y * cellule, cellule, cellule)

def mousePressed():
    x = int(mouseX / cellule)
    y = int(mouseY / cellule)
    if 1 <= x < SIZE_X - 1 and 1 <= y < SIZE_Y - 1:
        h = hue_from_click(x, y)
        deposit_blob(x, y, h)

def keyPressed():
    if key == 'r':
        for y in range(SIZE_Y):
            for x in range(SIZE_X):
                tAct[y][x] = WHITE
