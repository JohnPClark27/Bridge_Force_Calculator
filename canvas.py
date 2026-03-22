from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint, QEvent, QTimer, QPointF
import math
import numpy as np
from node import Node
from member import Member
from applied_force import AppliedForce
from reaction_force import ReactionForce


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

        temp_objects = [self.temp_node, self.temp_member, self.temp_applied_force, self.temp_reaction_force]

        for obj in temp_objects:
            if obj is not None:
                obj.paint(painter)

        # Draw members
        for member in self.members:
            member.paint(painter)

        # Draw nodes
        for node in self.nodes:
            node.paint(painter)

        # Draw applied forces
        for force in self.applied_forces:
            force.paint(painter)

        # Draw reaction forces
        for reaction in self.reaction_forces:
            reaction.paint(painter)

        
    def set_mode(self, mode):
        self.mode = mode
        self.temp_node = None
        self.temp_member = None
        self.temp_applied_force = None
        self.temp_reaction_force = None

        self.update()
    def mousePressEvent(self, event):
        x, y = self.map_to_grid(event.position())
        if hasattr(self, "activePopup") and self.activePopup is not None:
            return
        elif event.button() == Qt.MiddleButton:
            self.panning = True
            self.last_mouse_pos = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.LeftButton:
            if self.mode == "placeNode":
                for node in self.nodes:
                    if node.position == QPointF(x, y):
                        return # Node already exists at this position
                self.nodes.append(Node(x, y, self.id_counter))
                self.id_counter += 1
            elif self.mode == "deleteNode":
                for node in self.nodes:
                    if node.is_touching(QPointF(x, y)):
                        self.nodes.remove(node)
                        for member in self.members[:]:
                            if member.node1 == node or member.node2 == node:
                                self.members.remove(member)
                        for force in self.applied_forces[:]:
                            if force.node == node:
                                self.applied_forces.remove(force)
                        for reaction in self.reaction_forces[:]:
                            if reaction.node == node:
                                self.reaction_forces.remove(reaction)
                        print(f"Deleted node at ({node.position.x()}, {node.position.y()})")
                        break
            elif self.mode == "placeMember":
                for node in self.nodes:
                    if node.is_touching(QPointF(x, y)):
                        if self.temp_member is None:
                            self.temp_member = Member(node, node, self.id_counter)
                            self.id_counter += 1
                        else:
                            if node != self.temp_member.node1:
                                self.temp_member.node2 = node
                                for member in self.members:
                                    if (member.node1 == self.temp_member.node1 and member.node2 == self.temp_member.node2) or (member.node1 == self.temp_member.node2 and member.node2 == self.temp_member.node1):
                                        return # Member already exists between these nodes
                                self.members.append(self.temp_member)
                            self.temp_member = None
                        break
            elif self.mode == "reactionForce":
                # We can either draw a force from point to node or from node to point.
                # "node1" is always the node. Magnitude determines direction.

                node = self.node_at_pos(QPointF(x, y))
                if node is not None and self.temp_reaction_force is None:
                    self.temp_reaction_force = ReactionForce(node, node, 1, self.id_counter)
                    self.id_counter += 1
                    
                elif node is None and self.temp_reaction_force is None:
                    self.temp_reaction_force = ReactionForce(Node(x,y), Node(x,y), -1, self.id_counter)
                    self.id_counter += 1

                elif node is not None and self.temp_reaction_force is not None:
                    if self.temp_reaction_force.magnitude == -1: 
                        self.temp_reaction_force.node1 = node
                        if self.temp_reaction_force in self.reaction_forces:
                            return # Reaction force already exists between these nodes
                        self.reaction_forces.append(self.temp_reaction_force)
                        self.temp_reaction_force = None
                else: # node is None and temp_reaction_force is not None
                    if self.temp_reaction_force.magnitude == 1:
                        self.temp_reaction_force.node2 = Node(x,y)
                        if self.temp_reaction_force in self.reaction_forces:
                            return # Reaction force already exists between these nodes
                        self.reaction_forces.append(self.temp_reaction_force)
                        self.temp_reaction_force = None               

            elif self.mode == "appliedForce":
                node = self.node_at_pos(QPointF(x, y))
                if node is not None and self.temp_applied_force is None:
                    self.temp_applied_force = AppliedForce(node, node, 1, self.id_counter)
                    self.id_counter += 1
                    
                elif node is None and self.temp_applied_force is None:
                    self.temp_applied_force = AppliedForce(Node(x,y), Node(x,y), -1, self.id_counter)
                    self.id_counter += 1

                elif node is not None and self.temp_applied_force is not None:
                    if self.temp_applied_force.magnitude == -1: 
                        self.temp_applied_force.node1 = node
                        if self.temp_applied_force in self.applied_forces:
                            return # Applied force already exists between these nodes
                        self.applied_forces.append(self.temp_applied_force)
                        self.temp_applied_force = None
                else: # node is None and temp_applied_force is not None
                    if self.temp_applied_force.magnitude == 1:
                        self.temp_applied_force.node2 = Node(x,y)
                        if self.temp_applied_force in self.applied_forces:
                            return # Applied force already exists between these nodes
                        self.applied_forces.append(self.temp_applied_force)
                        self.temp_applied_force = None    



        self.update()
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