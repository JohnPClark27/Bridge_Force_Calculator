# App.py
# Description: Main application file for truss analysis software using PySide6.
# Author: John Clark
# Date: 12/1/2025

from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QHBoxLayout, QWidget
from PySide6.QtGui import QAction
from debugpanel import DebugPanel
import sys
from canvas import Canvas

# Class for main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statics Software")
      
        # Initial values
        WIDTH = 800
        HEIGHT = 600
        self.setMinimumSize(WIDTH, HEIGHT)
        self.currentMode = "placeNode"

        # Initialize canvas and widget items
        self.canvas = Canvas()
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.debug_panel = DebugPanel()
        layout.addWidget(self.canvas, stretch = 4)
        layout.addWidget(self.debug_panel, stretch = 1)
        self.setCentralWidget(container)
        self.canvas.set_mode(self.currentMode)

        # Connect debug buttons
        self.debug_panel.btn_matrix.clicked.connect(self.show_matrix)
        self.debug_panel.btn_forces.clicked.connect(self.show_force_vector)
        self.debug_panel.btn_solution.clicked.connect(self.show_solution_vector)
        self.debug_panel.btn_connections.clicked.connect(self.show_connections)
        self.debug_panel.btn_reactions.clicked.connect(self.show_reaction_forces)
        self.debug_panel.btn_applied.clicked.connect(self.show_applied_forces)

        self.debug_panel.hide()

        # Create toolbar and actions
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        placeNode = QAction("Place Node", self)
        deleteNode = QAction("Delete Node", self)
        connectNode = QAction("Connect Node", self)
        reactionForce = QAction("Reaction Force", self)
        applyForce = QAction("Apply Force", self)
        visualizeForces = QAction("Visualize Forces", self)
        debugPanel = QAction("Debug Panel", self)


        toolbar.addAction(placeNode)
        toolbar.addAction(deleteNode)   
        toolbar.addAction(connectNode)
        toolbar.addAction(reactionForce)
        toolbar.addAction(applyForce)
        toolbar.addAction(visualizeForces)
        toolbar.addAction(debugPanel)


        placeNode.triggered.connect(self.place_node)
        deleteNode.triggered.connect(self.delete_node)
        connectNode.triggered.connect(self.connect_node)
        reactionForce.triggered.connect(self.reaction_force)
        applyForce.triggered.connect(self.apply_force)
        visualizeForces.triggered.connect(self.visualize_forces)
        debugPanel.triggered.connect(self.toggle_debug_panel)

    # Actions for toolbar buttons
    def place_node(self):
        print("Place Node action triggered")
        self.currentMode = "placeNode"
        self.canvas.set_mode(self.currentMode)

    def delete_node(self):
        print("Delete Node action triggered")
        self.currentMode = "deleteNode"
        self.canvas.set_mode(self.currentMode)

    def connect_node(self):
        print("Connect Node action triggered")
        self.currentMode = "connectNode"
        self.canvas.set_mode(self.currentMode)

    def reaction_force(self):
        print("Reaction Force action triggered")
        self.currentMode = "reactionForce"
        self.canvas.set_mode(self.currentMode)

    def apply_force(self):
        print("Apply Force action triggered")
        self.currentMode = "applyForce"
        self.canvas.set_mode(self.currentMode)

    def visualize_forces(self):
        print("Visualize Forces action triggered")
        self.currentMode = "visualizeForces"
        self.canvas.set_mode(self.currentMode)

    def toggle_debug_panel(self):
        if self.debug_panel.isVisible():
            self.debug_panel.hide()
        else:
            self.debug_panel.show()

    # Actions for debug panel
    def show_matrix(self):
        A = self.canvas.generate_matrix()
        self.debug_panel.display(str(A))
    def show_force_vector(self):
        F = self.canvas.generate_force_array()
        self.debug_panel.display(str(F))

    def show_solution_vector(self):
        if hasattr(self.canvas, 'member_forces_array'):
            X = self.canvas.member_forces_array
            self.debug_panel.display(str(X))
        else:
            self.debug_panel.display("No solution vector available.")

    def show_connections(self):
        self.debug_panel.display(str(self.canvas.connections))

    def show_reaction_forces(self):
        self.debug_panel.display(str(self.canvas.reaction_forces))

    def show_applied_forces(self):
        self.debug_panel.display(str(self.canvas.forces))

    
# Start
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()