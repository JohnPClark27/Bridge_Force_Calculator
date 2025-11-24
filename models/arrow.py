import pygame
import math

class Arrow:
    def __init__(self, start_pos, end_pos,node = None,  color=(0,0,0), thickness = 2, head_length=10, head_width=5):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.thickness = thickness
        self.head_length = head_length
        self.head_width = head_width
        self.node = node
        self.force_magnitude = 0

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.thickness)
        
        # Calculate the angle of the arrow
        angle = math.atan2(self.end_pos[1] - self.start_pos[1], self.end_pos[0] - self.start_pos[0])
        
        # Calculate the points for the arrowhead
        left_point = (self.end_pos[0] - self.head_length * math.cos(angle) + self.head_width * math.sin(angle),
                      self.end_pos[1] - self.head_length * math.sin(angle) - self.head_width * math.cos(angle))
        
        right_point = (self.end_pos[0] - self.head_length * math.cos(angle) - self.head_width * math.sin(angle),
                       self.end_pos[1] - self.head_length * math.sin(angle) + self.head_width * math.cos(angle))
        
        # Draw the arrowhead
        pygame.draw.polygon(surface, self.color, [self.end_pos, left_point, right_point])

    def set_end_pos(self, x,y):
        self.end_pos = (x, y)

    def set_node(self, node):
        self.node = node

    def get_node(self):
        return self.node

    def get_unit_vector(self):
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:
            return (0, 0)
        return (dx / length, dy / length)
    
    def get_end_pos(self):
        return self.end_pos

    def set_force_magnitude(self, magnitude):
        self.force_magnitude = magnitude



    def get_force_vector(self):
        unit_vector = self.get_unit_vector()
        return (unit_vector[0] * self.force_magnitude, unit_vector[1] * self.force_magnitude)
