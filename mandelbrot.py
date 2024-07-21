import pygame, sys, math, colorsys
from math import log, log2

MAX_ITER = 128


#MAX_ITER = 100
def scale_number(OldMin, OldMax, OldValue, NewMin, NewMax):

    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER
    
    return n + 1 - log(log2(abs(z)))



# Image size (pixels)
WIDTH = 4800
HEIGHT = 3200

# Plot window
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1

palette = []

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hello Mandelbrot!')

#im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
#draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = mandelbrot(c)
        # The color depends on the number of iterations
        hue = int(255 * m / MAX_ITER)
        saturation =255
        value = 255 if m < MAX_ITER else 128
        # Plot the point

        hue = scale_number(0,255, hue, 0,1)
        saturation = scale_number(0,255,saturation,0,1)
        value = scale_number(0,255,value,0,1)
        color = colorsys.hsv_to_rgb(hue, saturation, value)
        #print (color)
        r=int(color[0]*255)
        g=int(color[1]*255)
        b=int(color[2]*255)
        screen.set_at([x, y], [r,g,b] )
print("DONE!!!")
pygame.image.save(screen, "mandelbrot1a.png")
while True: # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
#im.save('output.png', 'PNG')
