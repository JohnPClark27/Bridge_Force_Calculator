from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen

class Node:
    def __init__(self,id=None):
        self.position = None
        self.id = id
        self.complete = False

    def __eq__(self, other): # Compare nodes by position
        if not isinstance(other, Node):
            return NotImplemented
        return self.position == other.position
    
    def set_endpoint(self, node, pos):
        if node is None:
            self.position = QPoint(pos[0], pos[1])
            self.complete = True

    def is_complete(self):
        return self.complete

    def paint(self, painter):
        painter.setPen(QPen(Qt.red, 15))
        painter.drawPoint(self.position)

    

    def is_touching(self, pos):
        if (self.position == pos):
            return True