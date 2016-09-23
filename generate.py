from PIL import Image
import random, math

def scaled_sine(t):
    return (math.sin(t * math.pi * 2) + 1) / 2

def get_color(t, z):
    r = t * scaled_sine(z)
    b = t * scaled_sine(z + 1/3)
    g = t * scaled_sine(z + 2/3)
    return tuple(map(lambda c: math.floor(c * 255), (r, g, b)))

def interp(w, a, b):
    return (1 - w) * a + w * b

def fade(t):
    return t ** 3 * (t * (t * 6 - 15) + 10);

def create_gradient(size):
    g = {}
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            for z in range(0, size[2]):
                g[x, y, z] = (random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1))
    return g

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def pv(point, x, y, z, grad, gsize):
    dx = point[0] * gsize[0] - x
    dy = point[1] * gsize[1] - y
    dz = point[2] * gsize[2] - z
    return dot_product((dx, dy, dz), grad[x % gsize[0], y % gsize[1], z % gsize[2]])

def get_noise(point, grad, gsize):
    x = math.floor(point[0] * gsize[0])
    y = math.floor(point[1] * gsize[1])
    z = math.floor(point[2] * gsize[2])
    u = fade(point[0] * gsize[0] - x)
    v = fade(point[1] * gsize[1] - y)
    w = fade(point[2] * gsize[2] - z)
    t = interp(w, 
        interp(v,
            interp(u, pv(point, x, y, z, grad, gsize), pv(point, x + 1, y, z, grad, gsize)),
            interp(u, pv(point, x, y + 1, z, grad, gsize), pv(point, x + 1, y + 1, z, grad, gsize))),
        interp(v,
            interp(u, pv(point, x, y, z + 1, grad, gsize), pv(point, x + 1, y, z + 1, grad, gsize)),
            interp(u, pv(point, x, y + 1, z + 1, grad, gsize), pv(point, x + 1, y + 1, z + 1, grad, gsize))))
    return (t + 1) / 2

def draw_noise(img, z, grad, grad_size):
    pixels = img.load()
    for x in range(0, width):
        for y in range(0, height):
            t = get_noise((x / width, y / height, z), grad, grad_size)
            pixels[x, y] = get_color(t, z)
    
width, height = 320, 180
img = Image.new("RGB", (width, height))
gsize = (5, 5, 50)
grad = create_gradient(gsize)
imax = 500
for i in range(0, imax + 1):
    z = i / imax
    draw_noise(img, z, grad, gsize)
    print(str(i) + " / " + str(imax))
    img.save("images/" + str(i) + ".bmp")
