import pygame
import sys

pygame.init()

# Set up button class
class Button:
    def __init__(self,x,y,width, height, text, text_color, button_color):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
class Toolbar:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.surface = pygame.Surface((width, height))
        self.surface.fill((50, 50, 50))
        self.buttons = []
    
    def add_button(self, button_text):
        button = Button(10 + len(self.buttons) * 100, 10, 80, 30, button_text, (255, 255, 255), (100, 100, 100))
        self.buttons.append(button)

    def set_width(self, width):
        self.width = width
        self.surface = pygame.Surface((width, self.height))
        self.surface.fill((50, 50, 50))

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))
        for button in self.buttons:
            button.draw(self.surface)

class Node:
    def __init__(self, x, y, type, color):
        grid_size = 25

        # Snap to nearest grid intersection
        self.x = round(x / grid_size) * grid_size
        self.y = round(y / grid_size) * grid_size
        
        self.type = type
        self.color = color
        self.radius = 10

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

class Grid:
    def __init__(self, width, height, spacing):
        self.width = width
        self.height = height
        self.spacing = spacing

    def draw(self, surface):
        for x in range(0, self.width, self.spacing):
            pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, self.height))
        for y in range(0, self.height, self.spacing):
            pygame.draw.line(surface, (40, 40, 40), (0, y), (self.width, y))

    

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create grid
grid_size = 25
grid = Grid(WIDTH, HEIGHT, grid_size)

# Create toolbar
toolbar = Toolbar(WIDTH, 50)
toolbar.add_button("Button 1")
toolbar.add_button("Button 2")
toolbar.add_button("Button 3")

screen.fill((0, 0, 0))
toolbar.draw(screen)
pygame.display.flip()

screen_items = []


screen_items.append(grid)
screen_items.append(toolbar)


nodes = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    width, height = screen.get_size()

    # Display mouse coordinates beside mouse cursor
    if event.type == pygame.MOUSEMOTION:
        mouse_x, mouse_y = event.pos
        screen.fill((0, 0, 0))
        for item in screen_items:
            item.draw(screen)
        font = pygame.font.SysFont(None, 24)
        coord_text = font.render(f'X: {mouse_x} Y: {mouse_y}', True, (255, 255, 255))
        screen.blit(coord_text, (mouse_x + 10, mouse_y + 10))
        pygame.display.flip()
        continue

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        # Create a new node at the mouse position
        node = Node(mouse_x, mouse_y, "default", (255, 0, 0))
        nodes.append(node)
        screen_items.append(node)
        screen.fill((0, 0, 0))
        for item in screen_items:
            item.draw(screen)
        pygame.display.flip()

pygame.quit()
sys.exit()