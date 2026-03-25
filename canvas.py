from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
import math
import numpy as np
from node import Node
from member import Member
from applied_force import AppliedForce
from reaction_force import ReactionForce
from state import State


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.grid_size = 25
        self.nodes = []
        self.members = []
        self.applied_forces = []
        self.reaction_forces = []
        self.temp_node = None
        self.temp_member = None
        self.temp_applied_force = None
        self.temp_reaction_force = None
        self.placeholder = None # Temp node to hold position data on force input
        self.mode = "placeNode"
        self.id_counter = 1
        self.model = State()
        self.pending = None

        self.setMouseTracking(True)
        self.offset = QPoint(0, 0) # Current pan offset
        self.zoom = 1.0 # Zoom factor
        self.min_zoom = 0.2
        self.max_zoom = 5.0
        self.last_mouse_pos = None # For dragging
        self.panning = False # When the user is panning

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.offset)
        painter.scale(self.zoom, self.zoom)

        pen = QPen(QColor(50, 50, 50))
        painter.setPen(pen)

        w = self.width()
        h = self.height()

        # Draw grid
        for x in range(-1000, w+1000, self.grid_size):
            painter.drawLine(x, -1000, x, h+1000)
        for y in range(-1000, h+1000, self.grid_size):
            painter.drawLine(-1000, y, w+1000, y)

        self.model.paint_objects(painter)
        

        
    def set_mode(self, mode):
        self.mode = mode
        self.temp_node = None
        self.temp_member = None
        self.temp_applied_force = None
        self.temp_reaction_force = None

        self.update()
    def mousePressEvent(self, event):
        x,y = self.map_to_grid(event.position())
        if hasattr(self, "activePopup") and self.activePopup is not None:
            return
        elif event.button() == Qt.MiddleButton:
            self.panning = True
            self.last_mouse_pos = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.LeftButton:
            self.handle_click((x,y))

        self.update()

    def handle_click(self, pos):
        node = self.model.get_node_at(pos)

        if self.pending is None:
            self.pending = self.mode_to_object()
            
        self.pending.set_endpoint(node,pos)

        if self.pending.is_complete():
            self.model.add_object(self.pending)
            self.pending = None

    def mode_to_object(self):
        self.id_counter += 1
        if self.mode == "placeNode":
            return Node(id = self.id_counter)
        elif self.mode == "placeMember":
            return Member(id = self.id_counter)
        elif self.mode == "reactionForce":
            return ReactionForce(id = self.id_counter)
        elif self.mode == "applyForce":
            return AppliedForce(id = self.id_counter)
        return None

        
    def mouseMoveEvent(self, event):
        pass
    def mouseReleaseEvent(self, event):
        pass
    def eventFilter(self, source, event):
        pass
    def wheelEvent(self, event):
        pass
    def showForceInput(self, pos):
        pass
    def generate_matrix(self):
        pass
    def generate_force_array(self):
        pass
    def calculate_supports(self):
        pass

    def node_at_pos(self, pos):
        for node in self.nodes:
            if node.is_touching(pos):
                return node
        return None

    def map_to_grid(self, pos):
        x = (pos.x() - self.offset.x()) / self.zoom
        y = (pos.y() - self.offset.y()) / self.zoom
        x = round(x / self.grid_size) * self.grid_size
        y = round(y / self.grid_size) * self.grid_size
        return x, y