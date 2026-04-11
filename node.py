from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen

class Node:
    def __init__(self,id=None):
        self.position = None
        self.QPoint = None
        self.id = id
        self.complete = False
        self.label = ""

    def __eq__(self, other): # Compare nodes by position
        if not isinstance(other, Node):
            return NotImplemented
        return self.position == other.position
    
    def set_endpoint(self, node, pos):
        if node is None:
            self.position = pos
            self.QPoint = QPointF(pos[0], pos[1])
            self.complete = True

    def move_endpoint(self, node, pos):
        if self.complete == False:
            self.position = pos
            self.QPoint = QPointF(pos[0], pos[1])

    def is_complete(self):
        return self.complete

    def paint(self, painter):
        if self.position is not None:
            if self.complete == False:
                painter.setPen(QPen(Qt.blue, 15))
            else:
                painter.setPen(QPen(Qt.red, 15))
            painter.drawPoint(self.QPoint)
        painter.setPen(QPen(Qt.black, 2))
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.position[0]+10, self.position[1] - 5, self.label)

    

    def is_touching(self, pos):
        if (self.position == pos):
            return True
        return False