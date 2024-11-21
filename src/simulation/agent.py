import numpy as np
import pygame

class Agent:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = np.array([0.0, 0.0])
        self.evacuated = False
        self.color = (0, 100, 255)
    
    def update_position(self, movement, environment):
        # Apply movement with collision detection
        new_pos = np.array([self.x, self.y])
        
        # Movement logic
        if movement == 'up':
            new_pos[1] -= 2
        elif movement == 'down':
            new_pos[1] += 2
        elif movement == 'left':
            new_pos[0] -= 2
        elif movement == 'right':
            new_pos[0] += 2
        
        # Check for collisions
        if not environment.check_collision(new_pos, self.radius):
            self.x, self.y = new_pos
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                           (int(self.x), int(self.y)), self.radius)