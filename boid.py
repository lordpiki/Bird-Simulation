import pygame
import random

SEPERATION_RADIUS = 300
ALIGNMENT_RADIUS = 200 
COHESION_RADIUS = 200
WIDTH, HEIGHT = 1600, 1000



class Boid:
    def __init__(self, x, y, scout_group_num=0):
        self.x = x
        self.y = y
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.scout_group_num = scout_group_num

    def separation(self, boids):
        separation_radius = SEPERATION_RADIUS  # Adjust this value based on the desired separation distance
        steer = pygame.Vector2(0, 0)

        for other_boid in boids:
            if other_boid != self:
                distance = pygame.Vector2(self.x - other_boid.x, self.y - other_boid.y).length()
                if distance < separation_radius:
                    diff = pygame.Vector2(self.x - other_boid.x, self.y - other_boid.y)
                    diff.normalize_ip()
                    diff /= distance  # Weight by distance
                    steer += diff

        return steer

    def alignment(self, boids):
        alignment_radius = ALIGNMENT_RADIUS  # Adjust this value based on the desired alignment distance
        average_velocity = pygame.Vector2(0, 0)
        total_boids = 0

        for other_boid in boids:
            if other_boid != self:
                distance = pygame.Vector2(self.x - other_boid.x, self.y - other_boid.y).length()
                if distance < alignment_radius:
                    average_velocity += other_boid.velocity
                    total_boids += 1

        if total_boids > 0:
            average_velocity /= total_boids

        return average_velocity

    def cohesion(self, boids):
        cohesion_radius = COHESION_RADIUS  # Adjust this value based on the desired cohesion distance
        center_of_mass = pygame.Vector2(0, 0)
        total_boids = 0

        for other_boid in boids:
            if other_boid != self:
                distance = pygame.Vector2(self.x - other_boid.x, self.y - other_boid.y).length()
                if distance < cohesion_radius:
                    center_of_mass += pygame.Vector2(other_boid.x, other_boid.y)
                    total_boids += 1

        if total_boids > 0:
            center_of_mass /= total_boids
            desired_direction = pygame.Vector2(center_of_mass.x - self.x, center_of_mass.y - self.y)
            desired_direction.normalize_ip()

            return desired_direction
        else:
            return pygame.Vector2(0, 0)

    def update(self, boids):
        separation_force = self.separation(boids)
        alignment_force = self.alignment(boids)
        cohesion_force = self.cohesion(boids)

        # Adjust weights for each rule based on desired behavior
        separation_weight = 4.5
        alignment_weight = 1.0
        cohesion_weight = 1.0

        # Apply the rules to adjust the Boid's velocity
        self.acceleration = (separation_force * separation_weight +
                             alignment_force * alignment_weight +
                             cohesion_force * cohesion_weight)

        # Update velocity and position
        self.velocity += self.acceleration

        # Set minimum and maximum speed
        min_speed = 0.5
        max_speed = 5.0

        self.x += self.velocity.x
        self.y += self.velocity.y

        speed = self.velocity.length()

        if speed > max_speed:
            self.velocity.x = (self.velocity.x / speed) * max_speed
            self.velocity.y = (self.velocity.y / speed) * max_speed

        if speed < min_speed:
            self.velocity.x = (self.velocity.x / speed) * min_speed
            self.velocity.y = (self.velocity.y / speed) * min_speed
        
        
        # Apply bias behavior
        bias_val = 0.01  # Adjust the bias strength as needed
        if self.scout_group_num == 1:
            self.apply_bias(bias_val, 1)
        elif self.scout_group_num == 2:
            self.apply_bias(bias_val, -1)
        
# Apply turn-around behavior based on screen edges
        left_margin = 300
        right_margin = WIDTH - 300
        top_margin = 300
        bottom_margin = HEIGHT - 300
        turn_factor = 0.9  # Adjust as needed

        if self.x < left_margin:
            self.velocity.x += turn_factor
        if self.x > right_margin:
            self.velocity.x -= turn_factor
        if self.y > bottom_margin:
            self.velocity.y -= turn_factor
        if self.y < top_margin:
            self.velocity.y += turn_factor

    

    def apply_bias(self, bias_val, direction):
        # Apply bias to the Boid's velocity
        self.velocity.x = (1 - bias_val) * self.velocity.x + (bias_val * direction)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)
    # Draw the direction of the boid
        direction_length = 10
        direction = self.velocity.normalize() * direction_length
        end_point = (int(self.x + direction.x), int(self.y + direction.y))
        pygame.draw.line(screen, (255, 0, 0), (int(self.x), int(self.y)), end_point, 2)
        
