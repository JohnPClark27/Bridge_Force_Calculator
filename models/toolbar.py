import pygame

from models.button import Button

class Toolbar:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.surface = pygame.Surface((width, height))
        self.surface.fill((50, 50, 50))
        self.buttons = []
    
    def add_button(self, button_text):
        button = Button(len(self.buttons) * 120, 0, 120, self.height, button_text, (255, 255, 255), (100, 100, 100))
        self.buttons.append(button)
        for i, button in enumerate(self.buttons):
            button.set_x(i * (self.width/len(self.buttons)))
            button.set_width(self.width/len(self.buttons))
        

    def set_width(self, width):
        self.width = width
        self.surface = pygame.Surface((width, self.height))
        self.surface.fill((50, 50, 50))
        

    def draw(self, toolbar_surface):
        toolbar_surface.fill((50, 50, 50))
        for button in self.buttons:
            button.draw(toolbar_surface)

    