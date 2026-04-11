from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF, QRectF
from PySide6.QtGui import QPen
from node import Node
from arrow import arrow
from PySide6.QtGui import QPainter, QPen, QColor

class Member:
    def __init__(self, id = None):
        self.node1 = None
        self.node2 = None
        self.node1_id = None
        self.node2_id = None
        self.temp_node = Node(id = 0)
        self.id = id
        self.color = Qt.black
        self.node1Complete = False
        self.node2Complete = False
        
        self.visualize_force = False
        self.visualize_method = "line"
        self.max_force = 0
        self.force = 0

    def __eq__(self, other): # Compare members by nodes
        if not isinstance(other, Member):
            return NotImplemented
        return (self.node1 == other.node1 and self.node2 == other.node2) or (self.node1 == other.node2 and self.node2 == other.node1)

    def paint(self, painter):
        if not self.is_complete():
            painter.setPen(QPen(Qt.black, 3, Qt.DashLine))
        else:
            painter.setPen(QPen(self.color, 3))

        if self.node1 is not None and self.node2 is not None:
            painter.drawLine(self.node1.QPoint, self.node2.QPoint)
        elif self.node1 is not None:
            painter.drawLine(self.node1.QPoint, self.node1.QPoint)

        # Visualize Force
        if self.visualize_force:
            x1, y1 = self.node1.position
            x2, y2 = self.node2.position

            mid_x = (x1 + x2)/2
            mid_y = (y1 + y2)/2

            if self.visualize_method == "line":
                if self.max_force != 0:
                    scaler = float((abs(self.force[0])/self.max_force[0]) * 6)
                else:
                    scaler = 0

                if self.force < 0:
                    painter.setPen(QPen(QColor(200,50,50), 3 + scaler))
                else:
                    painter.setPen(QPen(QColor(50,100,210), 3 + scaler))
                painter.drawLine(self.node1.QPoint, self.node2.QPoint)
            elif self.visualize_method == "arrow":
                

                painter.setPen(QPen(Qt.magenta, 4))
                if self.force < 0:
                    arrow(x1,y1,mid_x,mid_y,1).paint(painter)
                    arrow(x2,y2, mid_x, mid_y,1).paint(painter)
                else:
                    arrow(mid_x,mid_y,x1,y1,1).paint(painter)
                    arrow(mid_x, mid_y,x2,y2,1).paint(painter)

            painter.setPen(QPen(Qt.black, 2))
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)

            rect = QRectF(mid_x - 50, mid_y - 10, 100, 20)
            painter.drawText(rect, Qt.AlignCenter, f"{self.force[0]:.2f} N")



    def set_endpoint(self, node, pos):
        if node is not None:
            if not self.node1Complete:
                self.node1 = node
                self.node1_id = node.id
                self.node1Complete = True
            elif self.node2Complete == False and node != self.node1:
                self.node2 = node
                self.node2_id = node.id
                self.node2Complete = True

    def move_endpoint(self, node, pos):
        if node is not None:
            if not self.node1Complete:
                self.node1 = node
                self.node1_id = node.id
            elif not self.node2Complete:
                self.node2 = node
                self.node2_id = node.id
        else:
            if not self.node1Complete:
                self.temp_node.move_endpoint(node, pos)
                self.node1 = self.temp_node
            elif not self.node2Complete:
                self.temp_node.move_endpoint(node, pos)
                self.node2 = self.temp_node

    def is_complete(self):
        return self.node2Complete

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