import pygame
from models.node import Node

# Joint that connects between two nodes.
class Joint:
    def __init__(self, node_a: Node, node_b: Node, Color=(255,255,255), Thickness = 2, tension = 0):
        self.node_a = node_a
        self.node_b = node_b
        self.color = Color
        self.thickness = Thickness
        self.tension = tension

    def draw(self, surface):
        pygame.draw.line(surface, self.color, (self.node_a.x, self.node_a.y), (self.node_b.x, self.node_b.y), self.thickness)

    def get_length(self):
        dx = self.node_b.x - self.node_a.x
        dy = self.node_b.y - self.node_a.y
        return (dx**2 + dy**2) ** 0.5
    
    def get_tension(self):
        return self.tension
    
    def set_tension(self, tension):
        self.tension = tension

    def get_unit_vector(self):
        length = self.get_length()
        if length == 0:
            return (0, 0)
        dx = abs(self.node_b.x - self.node_a.x)
        dy = abs(self.node_b.y - self.node_a.y)
        return (dx / length, dy / length)

    

    