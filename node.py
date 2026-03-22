from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen

class Node:
    def __init__(self, x, y, id=None):
        self.position = QPointF(x,y)
        self.id = id
        self.connections = [] # Connected member objects
        self.reactions = [] # Connected reaction force objects
        self.forces = [] # Connected applied force objects

    def __repr__(self):
        return f"Node(id={self.id}, pos=({self.position.x()}, {self.position.y()}))"

    def __eq__(self, other): # Compare nodes by position
        if not isinstance(other, Node):
            return NotImplemented
        return self.position == other.position

    def paint(self, painter):
        painter.setPen(QPen(Qt.red, 15))
        painter.drawPoint(self.position)

    

    def is_touching(self, pos):
        if (self.position == pos):
            return True