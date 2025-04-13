import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Camera settings
camera = {'x': 0, 'y': 0, 'z': -5, 'fov': 90}

# Projection function
def project_point(x, y, z):
    """Project a 3D point onto a 2D plane."""
    fov_factor = camera['fov'] / (z - camera['z']) if z - camera['z'] != 0 else 1
    proj_x = int(WIDTH / 2 + x * fov_factor)
    proj_y = int(HEIGHT / 2 - y * fov_factor)
    return proj_x, proj_y

# 3D objects
class Target:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.size = 0.5
        self.hit = False

    def render(self):
        if not self.hit:
            px, py = project_point(self.x, self.y, self.z)
            pygame.draw.circle(screen, GREEN, (px, py), 10)

    def check_collision(self, bullet):
        if (bullet.x - self.x)**2 + (bullet.y - self.y)**2 + (bullet.z - self.z)**2 < self.size**2:
            self.hit = True

class Bullet:
    def __init__(self, x, y, z, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dz = dz

    def update(self):
        self.z += self.dz

    def render(self):
        px, py = project_point(self.x, self.y, self.z)
        pygame.draw.circle(screen, RED, (px, py), 5)

# Game objects
player = {'x': 0, 'y': 0, 'z': 0}
bullets = []
targets = [Target(random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(5, 15)) for _ in range(5)]

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player['x'], player['y'], player['z'], 0.5))

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player['y'] += 0.1
    if keys[pygame.K_s]:
        player['y'] -= 0.1
    if keys[pygame.K_a]:
        player['x'] -= 0.1
    if keys[pygame.K_d]:
        player['x'] += 0.1

    # Update bullets
    for bullet in bullets[:]:
        bullet.update()
        if bullet.z > 20:
            bullets.remove(bullet)

    # Check collisions
    for target in targets:
        for bullet in bullets:
            target.check_collision(bullet)

    # Render objects
    for bullet in bullets:
        bullet.render()
    for target in targets:
        target.render()

    # Render player (crosshair)
    pygame.draw.line(screen, WHITE, (WIDTH // 2 - 10, HEIGHT // 2), (WIDTH // 2 + 10, HEIGHT // 2))
    pygame.draw.line(screen, WHITE, (WIDTH // 2, HEIGHT // 2 - 10), (WIDTH // 2, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
