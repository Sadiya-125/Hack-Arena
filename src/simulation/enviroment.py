import numpy as np
import random

class Environment:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles()
        self.exit_point = (width - 50, height // 2)
    
    def generate_obstacles(self):
        obstacles = []
        # Generate random rectangular obstacles
        for _ in range(5):
            x = random.randint(100, self.width - 200)
            y = random.randint(100, self.height - 200)
            w = random.randint(50, 100)
            h = random.randint(50, 100)
            obstacles.append((x, y, w, h))
        return obstacles
    
    def check_collision(self, pos, radius):
        # Check wall collisions
        if (pos[0] - radius < 0 or pos[0] + radius > self.width or
            pos[1] - radius < 0 or pos[1] + radius > self.height):
            return True
        
        # Check obstacle collisions
        for obstacle in self.obstacles:
            x, y, w, h = obstacle
            if (pos[0] > x and pos[0] < x + w and
                pos[1] < y and pos[1] > y - h):
                return True
        
        return False
    
    def draw_obstacles(self, screen):
        import pygame
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (100, 100, 100), obstacle)