import pygame, sys, math, colorsys
from math import log, log2, floor, ceil
from collections import defaultdict

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t 


def scale_number(OldMin, OldMax, OldValue, NewMin, NewMax):

    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def julia(c, z0):
    z = z0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER
    
    return n + 1 - log(log2(abs(z)))


MAX_ITER = 130
# Image size (pixels)
#WIDTH = 3200
#HEIGHT = 4800
WIDTH = 800
HEIGHT = 600

# Plot window
RE_START = -1
RE_END = 1
IM_START = -1.2
IM_END = 1.2

# c constant used to compute the julia set
c = complex(0.285, 0.01)
# Other interesting values:
# c = complex(-0.7269, 0.1889)
# c = complex(-0.8, 0.156)
# c = complex(-0.4, 0.6)


histogram = defaultdict(lambda: 0)
values = {}

palette = []

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hello Mandelbrot!')

#im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
#draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # Convert pixel coordinate to complex number
        z0 = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                    IM_START + (y / HEIGHT) * (IM_END - IM_START))
        # Compute the number of iterations
        m = julia(c, z0)
        
        values[(x, y)] = m
        if m < MAX_ITER:
            histogram[floor(m)] += 1

total = sum(histogram.values())
hues = []
h = 0
for i in range(MAX_ITER):
    h += histogram[i] / total
    hues.append(h)
hues.append(h)


for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        m = values[(x, y)]
        # The color depends on the number of iterations    
        hue = 1+(255 - int(255 * linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1)))
        saturation =255
        value = 255 if m < MAX_ITER else 0
        color = colorsys.hsv_to_rgb(hue, saturation, value)
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
pygame.image.save(screen, "julia.png")
while True: # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

