# App.py
# Description: Main application file for truss analysis software using PySide6.
# Author: John Clark
# Date: 3/20/2026

from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QHBoxLayout, QWidget
from PySide6.QtGui import QAction
from debugpanel import DebugPanel
import sys
from canvas import Canvas


# Class for main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Static Software")

        #initial values
        WIDTH = 800
        HEIGHT = 800
        self.setMinimumSize(WIDTH, HEIGHT)

        self.canvas = Canvas()
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.debug_panel = DebugPanel()
        layout.addWidget(self.canvas, stretch = 4)
        layout.addWidget(self.debug_panel, stretch = 1)
        self.setCentralWidget(container)
        self.canvas.set_mode("placeNode")

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
        toolbar.setMinimumHeight(50)
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

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background-color: #ffffff;
                border-bottom: 1px solid #cccccc;
                padding: 4px;
                spacing: 6px;
            }
            QToolBar QToolButton {
                color: #222222;
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #e8e8e8;
            }
            QToolBar QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        self.canvas.setStyleSheet("background-color: #ffffff;")

    def place_node(self):
        self.canvas.set_mode("placeNode")

    def delete_node(self):
        self.canvas.set_mode("deleteNode")

    def connect_node(self):
        self.canvas.set_mode("placeMember")

    def reaction_force(self):
        self.canvas.set_mode("reactionForce")

    def apply_force(self):
        self.canvas.set_mode("applyForce")

    def visualize_forces(self):
        self.canvas.set_mode("visualizeForces")

    def toggle_debug_panel(self):
        if self.debug_panel.isVisible():
            self.debug_panel.hide()
        else:
            self.debug_panel.show()

    # Actions for debug panel
    def show_matrix(self):
        A = self.canvas.model.generate_matrix()
        self.debug_panel.display(str(A))
    def show_force_vector(self):
        F = self.canvas.model.generate_force_array()
        self.debug_panel.display(str(F))

    def show_solution_vector(self):
        
            X = self.canvas.model.calculate_supports()
            self.debug_panel.display(str(X))
        
            #self.debug_panel.display("No solution vector available.")

    def show_connections(self):
        self.debug_panel.display(str(self.canvas.model.members))

    def show_reaction_forces(self):
        self.debug_panel.display(str(self.canvas.model.reaction_forces))

    def show_applied_forces(self):
        self.debug_panel.display(str(self.canvas.model.applied_forces))

    
# Start
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()