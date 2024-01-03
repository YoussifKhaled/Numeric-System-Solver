import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import re
from sympy import Symbol, sympify, diff, plot
from PyQt5.QtWidgets import QMessageBox

class PlotterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Expression Plotter')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.expression_label = QLabel('Enter Expression:')
        self.expression_input = QLineEdit()

        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plotExpression)

        self.layout.addWidget(self.expression_label)
        self.layout.addWidget(self.expression_input)
        self.layout.addWidget(self.plot_button)

        self.setLayout(self.layout)

    def plotExpression(self):
        Expression = self.expression_input.text()
        Expression = Expression.replace('^', '**').lower().replace('e', 'E').replace(' ', '')
        Expression = re.sub(r'(\d+)x', r'\1*x', Expression)

        try:
            x = Symbol('x')
            fx = sympify(Expression)
            f1x = diff(fx)
            f2x = diff(f1x)
            # Close previous plots
            plt.close('all')
            # Plot the new expression
            min_x = -10   # you can take it as input
            max_x = 10
            p = plot(fx, (x, min_x, max_x), show=False)
            p.title = fx
            p.ylabel = ''
            p.xlabel = ''
            p.show()
        except Exception as e:
            self.showErrorMessage(f'Invalid Expression: {str(e)}')

    def showErrorMessage(self, message):
        QMessageBox.critical(self, 'Error', message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotterApp()
    ex.show()
    sys.exit(app.exec_())
