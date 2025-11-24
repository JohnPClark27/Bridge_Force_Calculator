import pygame

class Node:
    def __init__(self, x, y, type, color):
        grid_size = 25

        # Snap to nearest grid intersection
        self.x = round(x / grid_size) * grid_size
        self.y = round(y / grid_size) * grid_size
        
        self.type = type
        self.color = color
        self.radius = 5
        self.x_force = 0
        self.y_force = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def is_hovered(self, mouse_pos):
        mx, my = mouse_pos

        distance = ((mx - self.x) ** 2 + (my - self.y) ** 2) ** 0.5
        is_touching = distance <= self.radius
        
        return is_touching

    def set_location(self, x, y):
        grid_size = 25
        self.x = round(x / grid_size) * grid_size
        self.y = round(y / grid_size) * grid_size

    