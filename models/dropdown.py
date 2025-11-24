import pygame

class Dropdown:
    def __init__ (self, x,y, width, height, options, font):
        self.rect = pygame.Rect(x,y,width,height)
        self.options = options
        self.font = font
        self.expanded = False
        self.selected_option = None
        self.option_rects = [pygame.Rect(x,y+(height*(i+1)), width, height) for i in range(len(options))]

        def draw(self, screen):
            pygame.draw.rect(screen, (200,200,200), self.rect)
            
            