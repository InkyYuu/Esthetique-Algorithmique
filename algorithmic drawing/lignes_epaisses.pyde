SIZE_X = 640
SIZE_Y = 400

def setup():
    size(SIZE_X, SIZE_Y)
    noFill()
    # Mode couleur HSB :
    # Choisis pour faire les couleurs de l'arc en ciel plus facilement
    colorMode(HSB, 360, 100, 100, 100)
    
    N = 0
    D = 0

    X = SIZE_X - 1
    Y = SIZE_Y - 1
    
    while N <= Y:
        D += 1
        strokeWeight(D)
        N += D + 1

        X -= D + 10
        Y -= D + 10
        
        hue = (120 + Y) % 360
        stroke(hue, 100, 100, 100)
        
        rect(N, N, X - N, Y - N)
        
def draw():    
    pass
