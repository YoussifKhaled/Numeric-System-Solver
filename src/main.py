import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from PyQt5.QtCore import Qt
from LinearTab import LinearTab
import time
from PyQt5.QtWidgets import  QApplication, QTableWidget, QTableWidgetItem, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QGroupBox, QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea, QDesktopWidget
from PyQt5 import QtGui
import qtpy
from NonLinearTab import NonLinearTab
from PyQt5.QtGui import QFont

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        FONT_SIZER = 10
        self.setStyleSheet('''
            QWidget {
                background-color: #8B0000; /* Dark Red */
                color: #eee;
            }
            QGroupBox {
                border: 2px solid #B22222; /* Fire Brick */
                border-radius: 5px;
                margin-top: 10px;
            }
            QLineEdit, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #800000; /* Maroon */
                color: #eee;
                border: 1px solid #B22222; /* Fire Brick */
                border-radius: 3px;
                padding: 5px;
            }
            QRadioButton {
                spacing: 5px;
                color: #eee;
            }
            QTabBar::tab {
                color: #000; /* Black */
            }
        ''')

        # Set window opacity
        self.setWindowOpacity(1)
        self.setWindowTitle('Linear Solver App')
        self.setGeometry(100, 100, 800, 600)

        # Create a tab widget
        tab_widget = QTabWidget(self)
        self.setCentralWidget(tab_widget)

        # Create a tab for Linear Solver
        linear_solver_tab = QWidget()
        matrix_input_app = LinearTab()
        linear_solver_tab_layout = QVBoxLayout()
        linear_solver_tab_layout.addWidget(matrix_input_app)
        linear_solver_tab.setLayout(linear_solver_tab_layout)
        

        # Add the Linear Solver tab to the tab widget
        tab_widget.addTab(linear_solver_tab, 'Linear Solver')

        # Create a tab for Nonlinear Solver
        nonlinear_solver_tab = NonLinearTab()

        # Add the Nonlinear Solver tab to the tab widget
        tab_widget.addTab(nonlinear_solver_tab, 'Nonlinear Solver')
        self.set_font_size_recursive(self, FONT_SIZER)



        self.show()
    def set_font_size_recursive(self, widget, font_size):
        if hasattr(widget, 'setFont'):
            font = QFont()
            font.setPointSize(font_size)
            widget.setFont(font)

        for child_widget in widget.findChildren(QWidget):
            self.set_font_size_recursive(child_widget, font_size)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec_())
