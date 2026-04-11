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
        self.setFocusPolicy(Qt.StrongFocus)
        self.grid_size = 25
        self.objectTypes = ["placeNode", "placeMember", "reactionForce", "applyForce"]
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

        self.activePopup = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.offset)
        painter.scale(self.zoom, self.zoom)

        pen = QPen(QColor(210, 210, 210))
        painter.setPen(pen)

        w = self.width()
        h = self.height()

        # Draw grid
        for x in range(-1000, w+1000, self.grid_size):
            painter.drawLine(x, -1000, x, h+1000)
        for y in range(-1000, h+1000, self.grid_size):
            painter.drawLine(-1000, y, w+1000, y)

        self.pending.paint(painter) if self.pending is not None else None

        self.model.paint_objects(painter)

        painter.end()

    def set_mode(self, mode):
        self.mode = mode

        self.pending = None

        if self.mode == "visualizeForces":
            self.model.show_forces()
        else:
            self.model.stop_showing_forces()

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
        if self.mode in self.objectTypes:
            node = self.model.get_node_at(pos)

            if self.pending is None:
                self.pending = self.mode_to_object()
                
            self.pending.set_endpoint(node,pos)

            if self.pending.is_complete():
                if isinstance(self.pending, AppliedForce):
                    def callback(value):
                        if value is not None:
                            self.pending.force = value
                            self.model.add_object(self.pending)
                            self.update()
                        self.pending = None

                    self.showForceInput(pos[0], pos[1], callback)
                else:
                    self.model.add_object(self.pending)
                    self.pending = None
                self.update()

        else:
            if self.mode == "deleteNode":
                node = self.model.get_node_at(pos)

                if node != None:
                    self.model.delete(node)

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
        x, y = self.map_to_grid(event.position())
        if self.panning:
            delta = event.position() - self.last_mouse_pos  # QPointF
            self.offset = QPointF(self.offset.x() + delta.x(), self.offset.y() + delta.y())
            self.last_mouse_pos = event.position()
            self.update()
            return
        if self.pending is not None:
            self.pending.move_endpoint(self.node_at_pos((x,y)), (x,y))
            self.update()
        else:
            if self.mode in self.objectTypes:
                self.pending = self.mode_to_object()
                self.pending.move_endpoint(self.node_at_pos((x,y)), (x,y))
                self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if hasattr(self, "activePopup") and self.activePopup is not None:
                self.activePopup._cancel_function()
                self.activePopup = None
                return True
            else:
                self.set_mode("none")
                return True

        return super().keyPressEvent(event)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        factor = 1.2 if angle > 0 else 1 / 1.2

        mouse_pos = event.position()
        before_scale = (mouse_pos - self.offset) / self.zoom

        self.zoom *= factor
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom))

        self.offset = mouse_pos - before_scale * self.zoom
        self.update()

    # Popup activates for user to enter force value.
    def showForceInput(self, x, y, callback):
        popup = QLineEdit(self)
        popup.setPlaceholderText("Force (N)")
        popup.setFixedWidth(100)


        popup.move(int(x+10), int(y+10))
        popup.show()

        popup.setAttribute(Qt.WA_InputMethodEnabled, True)
        popup.setFocusPolicy(Qt.StrongFocus)

        QTimer.singleShot(0, lambda: popup.setFocus())

        self.activePopup = popup

        def submit():
            text = popup.text().strip()
            if text == "":
                return
            
            try:
                value = float(text)
            except  ValueError:
                popup.setText("")
                return

            popup.deleteLater()
            self.activePopup = None
            callback(value)
        
        def cancel():
            popup.deleteLater()
            self.activePopup = None
            callback(None)

        popup.returnPressed.connect(submit)
        popup.editingFinished.connect(cancel)
        popup.installEventFilter(self)

        popup._cancel_function = cancel
        self.activePopup = popup

    def generate_matrix(self):
        pass
    def generate_force_array(self):
        pass
    def calculate_supports(self):
        pass

    def node_at_pos(self, pos):
        for node in self.model.nodes:
            if node.is_touching(pos):
                return node
        return None

    def map_to_grid(self, pos):
        x = (pos.x() - self.offset.x()) / self.zoom
        y = (pos.y() - self.offset.y()) / self.zoom
        x = round(x / self.grid_size) * self.grid_size
        y = round(y / self.grid_size) * self.grid_size
        return x, y