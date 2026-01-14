SIZE_X = 640
SIZE_Y = 400
MAX_ITER = 25

def setup():
    size(SIZE_X, SIZE_Y)
    colorMode(HSB, 360, 100, 100)
    noStroke()
    
    for y in range(height):
        for x in range(width):

            # Conversion pixel -> plan complexe
            cx = map(x, 0, width, -2.5, 1)
            cy = map(y, 0, height, -1, 1)

            zx = 0
            zy = 0
            i = 0

            # Algorithme de Mandelbrot
            while zx*zx + zy*zy <= 4 and i < MAX_ITER:
                xt = zx*zx - zy*zy + cx
                zy = 2*zx*zy + cy
                zx = xt
                i += 1

            # Couleur
            if i == MAX_ITER:
                fill(0, 0, 0) # Noir si ça appartient à l'ensemble
            else:
                fill(i * 4 % 360, 80, 90)

            rect(x, y, 1, 1)


def draw():
    pass
