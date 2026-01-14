from math import sin, cos, pi

SIZE_X = 900
SIZE_Y = 520
UI_H = 44

FLOCON, SOLEIL, NUAGE, HERBE = 0, 1, 2, 3
NOMS = ["Flocon", "Soleil", "Nuage", "Herbe"]

selected = FLOCON
items = []

DETAIL = 3  # Profondeur fractale globale

def setup():
    size(SIZE_X, SIZE_Y)
    smooth()
    colorMode(HSB, 360, 100, 100, 100)

def draw_ui():
    noStroke()
    fill(210, 20, 20, 100)
    rect(0, 0, width, UI_H)

    w = width / 4.0
    textAlign(CENTER, CENTER)
    textSize(14)

    for i in range(4):
        x = i * w
        fill(45, 80, 100, 85 if i == selected else 20)
        rect(x + 6, 6, w - 12, UI_H - 12, 10)
        fill(0, 0, 15 if i == selected else 95)
        text(NOMS[i], x + w/2, UI_H/2)

    textAlign(LEFT, CENTER)
    fill(0, 0, 100, 70)
    text("Clic: placer | +/- detail", 12, UI_H + 14)

def pick_ui(mx, my):
    if my > UI_H:
        return None
    return int(mx / (width / 4.0))

def add_item(t, x, y):
    items.append({
        "type": t,
        "x": float(x),
        "y": float(y),
        "phase": random(TWO_PI),
        "vx": random(0.3, 1.1),
        "vy": random(0.6, 1.4),
        "s": random(0.8, 1.4),
        "seed": int(random(100000))
    })

# FRACTALES

def koch(x1, y1, x2, y2, n):
    if n == 0:
        line(x1, y1, x2, y2)
        return
    dx = (x2 - x1) / 3.0
    dy = (y2 - y1) / 3.0
    xa, ya = x1 + dx, y1 + dy
    xb, yb = x1 + 2*dx, y1 + 2*dy
    a = pi / 3
    px = xa + cos(a)*dx - sin(a)*dy
    py = ya + sin(a)*dx + cos(a)*dy
    koch(x1, y1, xa, ya, n-1)
    koch(xa, ya, px, py, n-1)
    koch(px, py, xb, yb, n-1)
    koch(xb, yb, x2, y2, n-1)

def draw_flocon(r, n):
    for i in range(6):
        a1 = i * TWO_PI / 6
        a2 = (i+1) * TWO_PI / 6
        koch(cos(a1)*r, sin(a1)*r, cos(a2)*r, sin(a2)*r, n)

def rayon_fractal(length, n):
    if n <= 0 or length < 2:
        return
    line(0, 0, length, 0)
    pushMatrix()
    translate(length, 0)
    rotate(0.45)
    rayon_fractal(length*0.6, n-1)
    rotate(-0.9)
    rayon_fractal(length*0.6, n-1)
    popMatrix()

def nuage_fractal(r, depth, seed):
    if depth <= 0 or r < 4:
        return
    ellipse(0, 0, r*2, r*1.3)
    randomSeed(seed + depth*999)
    for i in range(3):
        a = random(TWO_PI)
        rr = r * random(0.35, 0.6)
        ox = cos(a) * r * random(0.2, 0.6)
        oy = sin(a) * r * random(0.1, 0.3)
        pushMatrix()
        translate(ox, oy)
        nuage_fractal(rr, depth-1, seed+i*1337)
        popMatrix()

def brin_herbe(length, n, wind):
    if n <= 0 or length < 3:
        return
    line(0, 0, 0, -length)
    pushMatrix()
    translate(0, -length)
    rotate(wind)
    brin_herbe(length*0.72, n-1, wind*0.9)
    pushMatrix()
    rotate(0.4)
    brin_herbe(length*0.5, n-1, wind*0.7)
    popMatrix()
    pushMatrix()
    rotate(-0.4)
    brin_herbe(length*0.5, n-1, wind*0.7)
    popMatrix()
    popMatrix()

def draw_background():
    noStroke()
    fill(200, 30, 95)
    rect(0, UI_H, width, height-UI_H)
    fill(110, 35, 45)
    rect(0, height*0.75, width, height)

def draw():
    draw_background()

    if mousePressed and mouseY > UI_H and frameCount % 6 == 0:
        add_item(selected, mouseX, mouseY)

    for it in items:
        t = it["type"]

        # Update
        if t == FLOCON:
            it["y"] += it["vy"]
            it["phase"] += 0.02
            if it["y"] > height + 40:
                it["y"] = UI_H
                it["x"] = random(width)

        elif t == SOLEIL:
            it["phase"] += 0.01

        elif t == NUAGE:
            it["x"] += it["vx"]
            if it["x"] > width + 80:
                it["x"] = -80

        elif t == HERBE:
            it["phase"] += 0.04

        # On dessine
        pushMatrix()
        translate(it["x"], it["y"])

        if t == FLOCON:
            rotate(it["phase"])
            stroke(190, 10, 100)
            draw_flocon(18*it["s"], DETAIL)

        elif t == SOLEIL:
            rotate(it["phase"])
            noStroke()
            fill(45, 90, 100)
            ellipse(0, 0, 32, 32)
            stroke(45, 80, 100)
            for i in range(12):
                pushMatrix()
                rotate(i * TWO_PI / 12)
                translate(16, 0)
                rayon_fractal(18*it["s"], DETAIL)
                popMatrix()

        elif t == NUAGE:
            stroke(0, 0, 100, 35)
            fill(0, 0, 100, 30)
            nuage_fractal(32*it["s"], DETAIL, it["seed"])

        elif t == HERBE:
            stroke(110, 70, 55)
            wind = sin(it["phase"]) * 0.25
            rotate(-0.2)
            brin_herbe(32*it["s"], DETAIL+1, wind)

        popMatrix()

    draw_ui()

def mouseClicked():
    global selected
    p = pick_ui(mouseX, mouseY)
    if p is not None:
        selected = constrain(p, 0, 3)
    elif mouseY > UI_H:
        add_item(selected, mouseX, mouseY)

def keyPressed():
    global selected, DETAIL, items
    if key == '+' or key == '=':
        DETAIL = min(6, DETAIL + 1)
    if key == '-':
        DETAIL = max(1, DETAIL - 1)
    if key == 'c' or key == 'C':
        items = []
