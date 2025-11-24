import pygame

class Grid:
    def __init__(self, width, height, grid_size):
        self.surface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.grid_size = grid_size

    def draw(self, grid_surface):
        grid_surface.fill((0,0,0))
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(grid_surface, (40, 40, 40), (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(grid_surface, (40, 40, 40), (0, y), (self.width, y))
