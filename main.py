import pygame
from boid import Boid
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create Boids
num_boids = 50
boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_boids)]

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Boids
    for boid in boids:
        boid.update()

    # Draw Boids
    screen.fill((0, 0, 0))
    for boid in boids:
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
