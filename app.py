from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from PySide6.QtGui import QAction
import sys

from canvas import Canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statics Software")
      

        WIDTH = 800
        HEIGHT = 600
        self.setMinimumSize(WIDTH, HEIGHT)

        self.currentMode = "placeNode"

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.canvas.set_mode(self.currentMode)

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        placeNode = QAction("Place Node", self)
        deleteNode = QAction("Delete Node", self)
        connectNode = QAction("Connect Node", self)
        reactionForce = QAction("Reaction Force", self)
        applyForce = QAction("Apply Force", self)
        visualizeForces = QAction("Visualize Forces", self)


        toolbar.addAction(placeNode)
        toolbar.addAction(deleteNode)   
        toolbar.addAction(connectNode)
        toolbar.addAction(reactionForce)
        toolbar.addAction(applyForce)
        toolbar.addAction(visualizeForces)


        placeNode.triggered.connect(self.place_node)
        deleteNode.triggered.connect(self.delete_node)
        connectNode.triggered.connect(self.connect_node)
        reactionForce.triggered.connect(self.reaction_force)
        applyForce.triggered.connect(self.apply_force)
        visualizeForces.triggered.connect(self.visualize_forces)

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

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()