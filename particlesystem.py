import pygame
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random
import math
from OpenGL.GL import glClearColor

#INFO AT THE BOTTOM OF THE CODE

# Klasa cząsteczki
class Particle:
    def __init__(self, position, velocity, color, lifespan):
        self.position = position  # [x, y, z]
        self.velocity = velocity  # [vx, vy, vz]
        self.color = color  # [r, g, b]
        self.lifespan = lifespan  # czas życia w klatkach

    def apply_force(self, force):
        # Aktualizacja prędkości pod wpływem siły
        self.velocity = [v + f for v, f in zip(self.velocity, force)]

    def update(self):
        # Aktualizacja pozycji
        self.position = [p + v for p, v in zip(self.position, self.velocity)]
        self.lifespan -= 1

    def is_dead(self):
        return self.lifespan <= 0


# Klasa Emitera
class Emitter:
    def __init__(self, position, rate, lifespan, speed_range):
        self.position = position
        self.rate = rate   # ile cząsteczek na klatkę
        self.lifespan = lifespan
        self.speed_range = speed_range
        self.particles = []

    def emit(self):
        for _ in range(self.rate):
            velocity = [
                random.uniform(-self.speed_range, self.speed_range),
                random.uniform(-self.speed_range, self.speed_range),
                random.uniform(-self.speed_range, self.speed_range),
            ]
            color = [random.random(), random.random(), random.random()]
            particle = Particle(self.position[:], velocity, color, self.lifespan)
            self.particles.append(particle)

    def update(self, external_force):
        self.emit()
        for particle in self.particles:
            particle.apply_force(external_force)
            particle.update()
        # Usuwanie martwych cząsteczek
        self.particles = [p for p in self.particles if not p.is_dead()]


# Funkcja do rysowania cząsteczek
def draw_particles(particles):
    for particle in particles:
        glPushMatrix()  # Zachowujemy bieżący stan macierzy
        glColor3f(*particle.color)  # Ustawiamy kolor cząsteczki
        glTranslatef(*particle.position)  # Przesuwamy do pozycji cząsteczki
        quadric = gluNewQuadric()  # Tworzymy nowy obiekt quadric
        gluSphere(quadric, 0.05, 16, 16)  # Rysujemy kulę (rozmiar i szczegółowość można dostosować)
        glPopMatrix()  # Przywracamy poprzedni stan macierzy

# Kolizje z sferą
def handle_collisions(particles, sphere_center, sphere_radius):
    for particle in particles:
        distance = math.sqrt(sum([(p - c) ** 2 for p, c in zip(particle.position, sphere_center)]))
        if distance < sphere_radius:
            # Odbicie (proste) - zmiana kierunku prędkości
            particle.velocity = [-v for v in particle.velocity]


# Główna pętla programu
def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.1, 0.1, 0.1, 1)  # Ustawiamy ciemnoszare tło
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    """
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
    """

    
    camera_pos = [0.0, 0.0, -20.0]  # Startowa pozycja kamery
    glTranslatef(*camera_pos)
    camera_pos = [0.0, 0.0, 0.0]  # Pozycja kamery
    camera_angle = [0.0, 0.0]  # Kąty obrotu kamery
            
    emitter = Emitter([0, 0, 0], 10, 100, 0.2)  # Emiter w środku sceny
    emitter2 = Emitter([10, 3, 1], 1, 100, 0.1)  # Emiter w środku sceny
    emitter3 = Emitter([-10, 3, 1], 1, 100, 0.1)  # Emiter w środku sceny

    sphere_center = [0, -5, 0]  # Sfera pod emiterem
    sphere_radius = 3

    clock = pygame.time.Clock()

    #mouse_held = False
    #last_mouse_x, last_mouse_y = pygame.mouse.get_pos()

    wind = 0
    attraction = -0.01
    resistance = 0


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
                """
            if event.type == MOUSEMOTION:
                if mouse_held:
                    dx, dy = event.rel
                    camera_angle[0] += dx * 0.1  # Obrot w poziomie
                    camera_angle[1] += dy * 0.1  # Obrot w pionie
                    """
                    

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            camera_pos[2] += 0.2  # Przesunięcie do przodu
        if keys[K_s]:
            camera_pos[2] -= 0.2
        if keys[K_a]:
            camera_pos[0] += 0.2  # Przesunięcie w lewo
        if keys[K_d]:
            camera_pos[0] -= 0.2  # Przesunięcie w prawo
        if keys[K_SPACE]:
            camera_pos[1] -= 0.2  # Przesunięcie w górę
        if keys[K_LSHIFT]:
            camera_pos[1] += 0.2 # Przesunięcie w dół
        #if keys[K_q]:
            #camera_angle[0] += 0.2  # Obrot w lewo
        if keys[K_ESCAPE]:
            run = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Aktualizacja cząsteczek
        
        if keys[K_o]:
            wind -= 0.001
        if keys[K_p]:
            wind += 0.001
        if keys[K_k]:
            attraction -= 0.001
        if keys[K_l]:
            attraction += 0.001
        if keys[K_n]:
            resistance -= 0.001
        if keys[K_m]:
            resistance += 0.001
        if keys[K_r]:
            attraction = 0.0
            wind = 0.0
            resistance = 0.0

        
        
        
        gravity = -0.01
        y_force = attraction + gravity
        external_force = [wind, y_force, resistance]  # Grawitacja
        emitter.update(external_force)
        emitter2.update([0, 0.1, 0])
        emitter3.update([0, 0.1, 0])
        handle_collisions(emitter.particles, sphere_center, sphere_radius)
        handle_collisions(emitter2.particles, sphere_center, sphere_radius)
        handle_collisions(emitter3.particles, sphere_center, sphere_radius)

        #Ustawianie kamery
        glTranslatef(*camera_pos)
        camera_pos = [0.0, 0.0, 0.0]
        glRotatef(camera_angle[1], 1, 0, 0)
        glRotatef(camera_angle[0], 0, 1, 0)

        # Rysowanie sfery (kolizja)
        glPushMatrix()
        glColor3f(1, 1, 1)
        glTranslatef(*sphere_center)
        quadric = gluNewQuadric()
        gluSphere(quadric, sphere_radius, 50, 50)
        glPopMatrix()

        # Rysowanie cząsteczek
        draw_particles(emitter.particles)
        draw_particles(emitter2.particles)
        draw_particles(emitter3.particles)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()




"""
USEFUL INFORMATIONS:
- W, S, A, D, SPACE, LSHIFT - poruszanie się kamerą (move forward, backward, left, right, up, down)
- ESC - wyjście z programu (exit)
FOR EMITTER 1 (center):
- O, P - zmiana wiatru (set wind force)  
- K, L - zmiana przyciągania (set attraction force)
- N, M - zmiana oporu (set resistance force)
- R - resetowanie wartości (reset all forces)

requirements:
- PyOpenGL
- Pygame

"""