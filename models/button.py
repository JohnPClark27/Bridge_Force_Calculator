import pygame

# Set up button class
class Button:
    def __init__(self,x,y,width, height, text, text_color, button_color):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def set_width(self, width):
        self.rect.width = width
    
    def set_x(self, x):
        self.rect.x = x

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)