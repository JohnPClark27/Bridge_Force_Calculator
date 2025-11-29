from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
import math

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.grid_size = 25
        self.nodes = []
        self.connections = [] # List of tuples: ((x1, y1), (x2, y2))
        self.reaction_forces = [] # List of tuples: ((x_start, y_start), (x_end, y_end))
        self.forces = [] # Two touples and force value: ((x_start, y_start), (x_end, y_end), force_value)
        self.temp_connection_start = None
        self.temp_connection_end = None
        self.force_endpoint = None
        self.currentMode = "placeNode"
        self.setMouseTracking(True)
        self.preview_node = None
        self.activePopup = None
        
        self.offset = QPoint(0, 0)       # Current pan offset
        self.zoom = 1.0                   # Zoom factor
        self.min_zoom = 0.2
        self.max_zoom = 5.0
        self.last_mouse_pos = None        # For dragging
        self.panning = False


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

        # Draw connections
        painter.setPen(QPen(Qt.white, 5))
        for ((x1, y1), (x2, y2)) in self.connections:
            painter.drawLine(x1, y1, x2, y2)

        # Draw nodes
        painter.setPen(QPen(Qt.red, 15))
        for (x,y) in self.nodes:
            painter.drawPoint(QPoint(x, y))

        # Draw reaction arrows
        painter.setPen(QPen(Qt.green, 3))
        for ((x_start, y_start), (x_end, y_end)) in self.reaction_forces:
            self.draw_arrow(painter, QPoint(x_start, y_start), QPoint(x_end, y_end))

        # Draw applied forces with magnitude
        painter.setPen(QPen(Qt.blue, 3))
        for ((x_start, y_start), (x_end, y_end), value) in self.forces:
            self.draw_arrow(painter, QPoint(x_start, y_start), QPoint(x_end, y_end))
            # Draw force magnitude text
            mid_x = (x_start + x_end) / 2
            mid_y = (y_start + y_end) / 2
            painter.drawText(mid_x + 5, mid_y - 5, f"{value} N")

        # Draw temporary connection line
        if self.temp_connection_start and self.temp_connection_end and self.currentMode == "connectNode":
            painter.setPen(QPen(Qt.yellow, 3, Qt.DashLine))
            painter.drawLine(self.temp_connection_start[0], self.temp_connection_start[1],
                             self.temp_connection_end[0], self.temp_connection_end[1])

        # Draw temporary reaction or force arrow
        if self.temp_connection_start and self.temp_connection_end and (self.currentMode == "reactionForce"):
            painter.setPen(QPen(Qt.yellow, 3, Qt.DashLine))
            self.draw_arrow(painter, QPoint(self.temp_connection_start[0], self.temp_connection_start[1]),
                            QPoint(self.temp_connection_end[0], self.temp_connection_end[1]))

        if self.temp_connection_start and self.temp_connection_end and (self.currentMode == "applyForce"):
            if self.force_endpoint is None:
                painter.setPen(QPen(Qt.yellow, 3, Qt.DashLine))
                self.draw_arrow(painter, QPoint(self.temp_connection_start[0], self.temp_connection_start[1]),
                                QPoint(self.temp_connection_end[0], self.temp_connection_end[1]))
            else:
                painter.setPen(QPen(Qt.yellow, 3))
                self.draw_arrow(painter, QPoint(self.temp_connection_start[0], self.temp_connection_start[1]),
                                QPoint(self.force_endpoint[0], self.force_endpoint[1]))
            
        # Draw preview node
        if self.preview_node and self.currentMode == "placeNode":
            painter.setPen(QPen(Qt.blue, 15))
            painter.drawPoint(QPoint(self.preview_node[0], self.preview_node[1]))

        if self.preview_node and self.currentMode == "deleteNode":
            painter.setPen(QPen(Qt.cyan, 15))
            painter.drawPoint(QPoint(self.preview_node[0], self.preview_node[1]))

    def draw_arrow(self, painter, start, end):
        painter.drawLine(start, end)
        # Draw arrowhead
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 10
        p1 = QPoint(end.x() - arrow_size * math.cos(angle - math.pi / 6), end.y() - arrow_size * math.sin(angle - math.pi / 6))
        p2 = QPoint(end.x() - arrow_size * math.cos(angle + math.pi / 6), end.y() - arrow_size * math.sin(angle + math.pi / 6))
        painter.drawLine(end, p1)
        painter.drawLine(end, p2)

    def mousePressEvent(self, event):
        if hasattr(self, "activePopup") and self.activePopup is not None:
            return
        elif event.button() == Qt.MiddleButton:
            self.panning = True
            self.last_mouse_pos = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.LeftButton:
            if self.currentMode == "placeNode":
                x,y = self.map_to_canvas(event.position())
                if (x, y) not in self.nodes:
                    self.nodes.append((x, y))
                    self.update()
            elif self.currentMode == "deleteNode":
                x,y = self.map_to_canvas(event.position())
                if (x, y) in self.nodes:
                    self.nodes.remove((x, y))
                    for conn in self.connections[:]:
                        if (x, y) in conn:
                            self.connections.remove(conn)
                    for rf in self.reaction_forces[:]:
                        if (x, y) in rf:
                            self.reaction_forces.remove(rf)
                    for f in self.forces[:]:
                        if (x, y) in f[:2]:
                            self.forces.remove(f)
                    self.preview_node = None
                    self.update()
            elif self.currentMode == "connectNode":
                if  self.temp_connection_start is None:
                    x,y = self.map_to_canvas(event.position())
                    if (x, y) in self.nodes:
                        self.temp_connection_start = (x, y)
                else:
                    x,y = self.map_to_canvas(event.position())
                    if (x, y) in self.nodes and (x, y) != self.temp_connection_start:
                        self.connections.append((self.temp_connection_start, (x, y)))
                        self.temp_connection_start = None
                        self.update()
            elif self.currentMode == "reactionForce": # Arrow to or from point
                x,y = self.map_to_canvas(event.position())
                if self.temp_connection_start is None:
                    self.temp_connection_start = (x,y)
                    self.temp_connection_end = self.temp_connection_start
                else:
                    if self.temp_connection_start in self.nodes: # We previously clicked on a node (Must click empty point next)
                        if (x,y) not in self.nodes:
                            self.temp_connection_end = (x,y)
                            self.reaction_forces.append((self.temp_connection_start, self.temp_connection_end))
                            self.temp_connection_start = None
                            self.temp_connection_end = None
                            self.update()
                    elif self.temp_connection_start not in self.nodes: # We previously clicked on empty point (Must click node next)
                        if (x,y) in self.nodes:
                            self.temp_connection_end = (x,y)
                            self.reaction_forces.append((self.temp_connection_start, self.temp_connection_end))
                            self.temp_connection_start = None
                            self.temp_connection_end = None
                            self.update()

            elif self.currentMode == "applyForce":
                x,y = self.map_to_canvas(event.position())
                if self.temp_connection_start is None:
                    self.temp_connection_start = (x,y)
                    self.temp_connection_end = self.temp_connection_start
                else:
                    if self.temp_connection_start in self.nodes: # We previously clicked on a node (Must click empty point next)
                        if (x,y) not in self.nodes:
                            self.temp_connection_end = (x,y)
                            self.force_endpoint = (x,y)
                            def apply_force(value):
                                self.activePopup = None
                                if value is None:
                                    self.temp_connection_start = None
                                    self.temp_connection_end = None
                                    self.force_endpoint = None
                                    self.update()
                                    return
                                self.forces.append((self.temp_connection_start, self.force_endpoint, value))
                                self.temp_connection_start = None
                                self.temp_connection_end = None
                                self.force_endpoint = None
                                self.update()
                            self.showForceInput(event.position().x(), event.position().y(), apply_force)
                            
                    elif self.temp_connection_start not in self.nodes: # We previously clicked on empty point (Must click node next)
                        if (x,y) in self.nodes:
                            self.temp_connection_end = (x,y)
                            self.force_endpoint = (x,y)
                            def apply_force(value):
                                self.activePopup = None
                                if value is None:
                                    self.temp_connection_start = None
                                    self.temp_connection_end = None
                                    self.force_endpoint = None
                                    self.update()
                                    return
                                self.forces.append((self.temp_connection_start, self.force_endpoint, value))
                                self.temp_connection_start = None
                                self.temp_connection_end = None
                                self.force_endpoint = None
                                self.update()
                            self.showForceInput(event.position().x(), event.position().y(), apply_force)
                            
            elif self.currentMode == "visualizeForces":
                pass  # Placeholder for visualize forces logic
        

    def mouseMoveEvent(self, event):
        if self.panning and self.last_mouse_pos is not None:
            delta = event.position() - self.last_mouse_pos  # QPointF
            self.offset = QPointF(self.offset.x() + delta.x(), self.offset.y() + delta.y())
            self.last_mouse_pos = event.position()
            self.update()
            return
        if self.currentMode == "placeNode":
            x,y = self.map_to_canvas(event.position())
            if (x, y) not in self.nodes:
                self.preview_node = (x, y)
                self.update()
            else:
                self.preview_node = None
                self.update()
        elif self.currentMode == "deleteNode":
            x,y = self.map_to_canvas(event.position())
            if (x, y) in self.nodes:
                self.preview_node = (x, y)
                self.update()
            else:
                self.preview_node = None
                self.update()
        elif self.currentMode == "connectNode":
            if self.temp_connection_start is not None:
                x,y = self.map_to_canvas(event.position())
                self.temp_connection_end = (x, y)
                self.update()
        elif self.currentMode == "reactionForce":
            if self.temp_connection_start is not None:
                x,y = self.map_to_canvas(event.position())
                self.temp_connection_end = (x, y)
                self.update()
        elif self.currentMode == "applyForce":
            if self.temp_connection_start is not None:
                x,y = self.map_to_canvas(event.position())
                self.temp_connection_end = (x, y)
                self.update()

    def eventFilter(self, obj, event):
        if hasattr(self, "activePopup") and obj == self.activePopup:
            if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
                obj._cancel_function()
                self.activePopup = None
                return True
        return super().eventFilter(obj, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        factor = 1.2 if angle > 0 else 1 / 1.2

        mouse_pos = event.position()
        before_scale = (mouse_pos - self.offset) / self.zoom

        self.zoom *= factor
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom))

        self.offset = mouse_pos - before_scale * self.zoom
        self.update()

    def set_mode(self, mode):
        self.currentMode = mode
        self.temp_connection_start = None
        self.temp_connection_end = None
        self.preview_node = None
        self.update()

    def map_to_canvas(self, pos):
        x = (pos.x() - self.offset.x()) / self.zoom
        y = (pos.y() - self.offset.y()) / self.zoom
        x = round(x / self.grid_size) * self.grid_size
        y = round(y / self.grid_size) * self.grid_size
        return x, y



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