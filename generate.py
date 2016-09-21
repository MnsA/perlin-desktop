from PIL import Image
import random, math

sine_wave = lambda k: math.floor(150 * math.sin(k * math.pi * 2))
def get_color(t):
    return (sine_wave(t), sine_wave(t + 1/3), sine_wave(t + 2/3))

def interp(w, a, b):
    return (1 - w) * a + w * b

def fade(t):
    return t ** 3 * (t * (t * 6 - 15) + 10);

def create_gradient(size):
    g = {}
    for x in range(0, size):
        for y in range(0, size):
            for z in range(0, size):
                g[x, y, z] = (random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1))
    return g

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def pv(point, x, y, z, grad, grad_size):
    dx = point[0] * grad_size - x
    dy = point[1] * grad_size - y
    dz = point[2] * grad_size - z
    return dot_product((dx, dy, dz), grad[x % grad_size, y % grad_size, z % grad_size])

def get_noise(point, grad, grad_size):
    x, y, z = tuple(map(lambda c: math.floor(c * grad_size), point))
    u = fade(point[0] * grad_size - x)
    v = fade(point[1] * grad_size - y)
    w = fade(point[2] * grad_size - z)
    return interp(w, 
        interp(v,
            interp(u, pv(point, x, y, z, grad, grad_size), pv(point, x + 1, y, z, grad, grad_size)),
            interp(u, pv(point, x, y + 1, z, grad, grad_size), pv(point, x + 1, y + 1, z, grad, grad_size))),
        interp(v,
            interp(u, pv(point, x, y, z + 1, grad, grad_size), pv(point, x + 1, y, z + 1, grad, grad_size)),
            interp(u, pv(point, x, y + 1, z + 1, grad, grad_size), pv(point, x + 1, y + 1, z + 1, grad, grad_size))))

def draw_noise(img, z, grad, grad_size):
    pixels = img.load()
    for x in range(0, width):
        for y in range(0, height):
            t = get_noise((x / width, y / height, z), grad, grad_size)
            pixels[x, y] = get_color(interp(0.7, z, t))
    
width, height = 320, 180
img = Image.new("RGB", (width, height))
grad_size = 5
grad = create_gradient(grad_size)
imax = 100
for i in range(0, imax):
    z = i / imax
    draw_noise(img, z, grad, grad_size)
    print(str(i) + " / " + str(imax))
    img.save("images/" + str(i) + ".bmp")
