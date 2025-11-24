import pygame

class force_input_popup:
    def __init__(self,message, x,y, width, height, color = (200,200,200)):
        self.message = message
        self.input_text = ""
        self.active = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = pygame.font.SysFont(None, 24)

    def open(self):
        self.active = True
        self.input_text = ""
        print("Popup opened with message:", self.message)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return self.input_text
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            # If input is a number
            elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in self.input_text):
                self.input_text += event.unicode

    def draw(self, screen):
        if self.active:
            print("Drawing popup with message:", self.message)
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            message_surf = self.font.render(self.message, True, (0, 0, 0))
            input_surf = self.font.render(self.input_text, True, (0, 0, 0))
            screen.blit(message_surf, (self.x + 10, self.y + 10))
            screen.blit(input_surf, (self.x + 10, self.y + 40))