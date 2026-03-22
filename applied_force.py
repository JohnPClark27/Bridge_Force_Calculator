from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen
from node import Node
from arrow import arrow

class AppliedForce:
    def __init__(self, node1, node2, magnitude, id = None):
        self.node1 = node1
        self.node2 = node2
        
        self.magnitude = magnitude # 1 node 1 to node 2, -1 node 2 to node 1
        self.id = id
        self.color = Qt.green
        self.temp_line = False

    def __eq__(self, other):
        if not isinstance(other, ReactionForce):
            return NotImplemented
        return (self.node1 == other.node1 and self.node2 == other.node2) or (self.node1 == other.node2 and self.node2 == other.node1)

    def paint(self, painter):
        x1 = self.node1.position.x()
        y1 = self.node1.position.y()
        x2 = self.node2.position.x()
        y2 = self.node2.position.y()
        
        if (self.temp_line):
            painter.setPen(QPen(Qt.yellow, 3, Qt.DashLine))
        else:
            painter.setPen(QPen(self.color, 3))
        if self.magnitude == 1:
            arrow(x1, y1, x2, y2, 1).paint(painter)
        else:  
            arrow(x1, y1, x2, y2, -1).paint(painter)

    def is_touching(self, pos):
        x1 = self.node1.position.x()
        y1 = self.node1.position.y()
        x2 = self.node2.position.x()
        y2 = self.node2.position.y()

        px, py = pos.x(), pos.y()

        ab = (x2 - x1, y2 - y1)
        ap = (px - x1, py - y1)

        t = (ap[0] * ab[0] + ap[1] * ab[1]) / (ab[0] ** 2 + ab[1] ** 2)

        t = max(0, min(1, t))

        closest = (x1 + ab[0] * t, y1 + ab[1] * t)

        distance = ((closest[0] - px) ** 2 + (closest[1] - py) ** 2) ** 0.5
        return distance < 3
