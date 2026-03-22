from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen
import math

class arrow:
    def __init__(self, x1, y1, x2, y2, direction):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.direction = direction

    def paint(self, painter):
        # Draws arrow
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)
        # Draws arrowhead
        angle = 30
        length = 10
        if self.direction == 1: # From p1 to p2
            angle_rad = math.radians(angle)
            dx = self.x2 - self.x1
            dy = self.y2 - self.y1
            line_angle = math.atan2(dy, dx)
            left_angle = line_angle + math.pi - angle_rad
            right_angle = line_angle + math.pi + angle_rad
            left_x = self.x2 + length * math.cos(left_angle)
            left_y = self.y2 + length * math.sin(left_angle)
            right_x = self.x2 + length * math.cos(right_angle)
            right_y = self.y2 + length * math.sin(right_angle)
            painter.drawLine(self.x2, self.y2, left_x, left_y)
            painter.drawLine(self.x2, self.y2, right_x, right_y)

        else: # From p2 to p1
            angle_rad = math.radians(angle)
            dx = self.x1 - self.x2
            dy = self.y1 - self.y2
            line_angle = math.atan2(dy, dx)
            left_angle = line_angle + math.pi - angle_rad
            right_angle = line_angle + math.pi + angle_rad
            left_x = self.x1 + length * math.cos(left_angle)
            left_y = self.y1 + length * math.sin(left_angle)
            right_x = self.x1 + length * math.cos(right_angle)
            right_y = self.y1 + length * math.sin(right_angle)
            painter.drawLine(self.x1, self.y1, left_x, left_y)
            painter.drawLine(self.x1, self.y1, right_x, right_y)

    


