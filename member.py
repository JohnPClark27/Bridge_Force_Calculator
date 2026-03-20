from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen
from node import Node

class Member:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.id = None
        self.color = Qt.white
        self.temp_line = False

    def __repr__(self):
        return f"Member(id={self.id}, node1={self.node1.id}, node2={self.node2.id})"
    
    def paint(self, painter):
        if (self.temp_line):
            painter.setPen(QPen(Qt.yellow, 3, Qt.DashLine))
        else:
            painter.setPen(QPen(self.color, 3))
        painter.drawLine(self.node1.position, self.node2.position)

    def is_touching(self, pos):
        x1, y1 = self.node1.position.x(), self.node1.position.y()
        x2, y2 = self.node2.position.x(), self.node2.position.y()
        px, py = pos.x(), pos.y()

        ab = (x2 - x1, y2 - y1)
        ap = (px - x1, py - y1)

        t = (ap[0] * ab[0] + ap[1] * ab[1]) / (ab[0] ** 2 + ab[1] ** 2)

        t = max(0, min(1, t))

        closest = (x1 + ab[0] * t, y1 + ab[1] * t)

        distance = ((closest[0] - px) ** 2 + (closest[1] - py) ** 2) ** 0.5
        return distance < 3
    

line = Member(Node(0,0), Node(100,100))
print(line.is_touching(QPointF(50,50))) # Should be True
print(line.is_touching(QPointF(10,15))) # Should be False
