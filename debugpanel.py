from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

# Debug Panel for testing
class DebugPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(350)
        self.setWindowTitle("Debug Panel")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.textBox = QTextEdit()
        self.textBox.setReadOnly(True)
        layout.addWidget(self.textBox)

        self.btn_matrix = QPushButton("Show A Matrix")
        self.btn_forces = QPushButton("Show Force Vector F")
        self.btn_solution = QPushButton("Show Solution Vector X")
        self.btn_connections = QPushButton("Show Connections")
        self.btn_reactions = QPushButton("Show Reaction Forces")
        self.btn_applied = QPushButton("Show Applied Forces")

        layout.addWidget(self.btn_matrix)
        layout.addWidget(self.btn_forces)
        layout.addWidget(self.btn_solution)
        layout.addWidget(self.btn_connections)
        layout.addWidget(self.btn_reactions)
        layout.addWidget(self.btn_applied)

    def display(self, text):
        self.textBox.setText(text)