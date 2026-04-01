from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
from PySide6.QtGui import QPen
from node import Node
from arrow import arrow

class AppliedForce:
    def __init__(self,id = None):
        self.endnode = None

        self.tempnode = Node(id = 0)

        self.endpoint = Node(id = 0)
        
        self.magnitude = 1 # 1 node 1 to node 2, -1 node 2 to node 1
        self.force = 0
        self.id = id
        self.color = Qt.blue
        self.temp_line = False

        self.endnodeSet = False
        self.endpointSet = False

    def __eq__(self, other):
        if not isinstance(other, AppliedForce):
            return NotImplemented
        return self.endnode == other.endnode and self.endpoint == other.endpoint

    def set_endpoint(self, node, pos):
        if node is not None:
            if self.endnodeSet == False:
                self.endnode = node
                if self.endpointSet == False:
                    self.magnitude = 1
                self.endnodeSet = True
        else:
            if self.endpointSet == False:
                self.endpoint.move_endpoint(node, pos)
                if self.endnodeSet == False:
                    self.magnitude = -1
                self.endpointSet = True
            

    def move_endpoint(self, node, pos):
        if self.endnodeSet == False:
            self.tempnode.move_endpoint(node, pos)
            self.endnode = self.tempnode
        if self.endpointSet == False:
            self.endpoint.move_endpoint(node, pos)

    def is_complete(self):
        return self.endnodeSet and self.endpointSet


    def paint(self, painter):
        if (self.is_complete() == False):
            painter.setPen(QPen(Qt.yellow, 3, Qt.DashLine))
        else:
            painter.setPen(QPen(self.color, 3))

        if self.endnode is not None and self.endpoint is not None:
            x1 = self.endnode.position[0]
            y1 = self.endnode.position[1]
            x2 = self.endpoint.position[0]
            y2 = self.endpoint.position[1]

            if self.magnitude == 1:
                arrow(x1, y1, x2, y2, 1).paint(painter)
                painter.setPen(QPen(Qt.white, 1))
                painter.drawText((x1 + x2) / 2, (y1 + y2) / 2, f"{self.force} N")
            else:  
                arrow(x1, y1, x2, y2, -1).paint(painter)
                painter.setPen(QPen(Qt.white, 1))
                painter.drawText((x1 + x2) / 2, (y1 + y2) / 2, f"{self.force} N")

        elif self.endpoint is None and self.endnode is not None:
            painter.drawLine(self.endnode.QPoint, self.endnode.QPoint)
        elif self.endpoint is not None and self.endnode is None:
            painter.drawLine(self.endpoint.QPoint, self.endpoint.QPoint)

    def is_touching(self, pos):
        x1 = self.endnode.position[0]
        y1 = self.endnode.position[1]
        x2 = self.endpoint.position[0]
        y2 = self.endpoint.position[1]

        px, py = pos.x(), pos.y()

        ab = (x2 - x1, y2 - y1)
        ap = (px - x1, py - y1)

        t = (ap[0] * ab[0] + ap[1] * ab[1]) / (ab[0] ** 2 + ab[1] ** 2)

        t = max(0, min(1, t))

        closest = (x1 + ab[0] * t, y1 + ab[1] * t)

        distance = ((closest[0] - px) ** 2 + (closest[1] - py) ** 2) ** 0.5
        return distance < 3
