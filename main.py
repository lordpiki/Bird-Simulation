import pygame
import pygame_gui
from boid import Boid
import random

# Constants
WIDTH, HEIGHT = 1500, 900
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create Boids
num_boids = 100
boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT), int(random.randrange(0, 2))) for _ in range(num_boids)]

# Create a UIManager
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Define your weights
alignment_weight = 1.0
cohesion_weight = 1.0
separation_weight = 1.0


alignment_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10), (200, 30)),
    start_value=alignment_weight,
    value_range=(0.01, 5.0),
    manager=ui_manager
)

cohesion_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 50), (200, 30)),
    start_value=cohesion_weight,
    value_range=(0.01, 5.0),
    manager=ui_manager
)

separation_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 90), (200, 30)),
    start_value=separation_weight,
    value_range=(0.01, 5.0),
    manager=ui_manager
)

clock = pygame.time.Clock()


# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle slider events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == alignment_slider:
                    alignment_weight = alignment_slider.get_current_value()
                    print(alignment_weight)
                elif event.ui_element == cohesion_slider:
                    cohesion_weight = cohesion_slider.get_current_value()
                    print(cohesion_weight)
                elif event.ui_element == separation_slider:
                    separation_weight = separation_slider.get_current_value()
                    print(separation_weight)


        ui_manager.process_events(event)

    # Update Boids
    for boid in boids:
        boid.update(boids, alignment_weight, cohesion_weight, separation_weight)

    # Draw Boids
    screen.fill((0, 0, 0))
    for boid in boids:
        boid.draw(screen)
        
    ui_manager.update(clock.tick(60) / 1000.0)
    ui_manager.draw_ui(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
