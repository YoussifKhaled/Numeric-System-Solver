import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QGroupBox, QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea, QDesktopWidget, QTextEdit
from PyQt5 import QtGui
from PyQt5.QtGui import QFont  # Add this line
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import re
from sympy import Symbol, sympify, diff, plot
from PyQt5.QtWidgets import QMessageBox
from Newton import chef

class NonLinearTab(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Matrix Input')

        # Get screen geometry
        screen_rect = QDesktopWidget().screenGeometry()

        # Set maximum size to the full screen
        self.setMaximumSize(screen_rect.width(), screen_rect.height())

        # Set dark theme stylesheet
        self.setStyleSheet('''
            QWidget {
                background-color: #8B0000; /* Dark Red */
                color: #eee;
            }
            QGroupBox {
                border: 3px solid #B22222; /* Fire Brick */
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
        self.setWindowOpacity(0.92)
        self.last_runtime_label = QLabel('Last Runtime: N/A')
        self.last_runtime_label.setStyleSheet('color: #ffbb00')  # Set text color to yellow

        # Input settings group box
        input_settings_groupbox = QGroupBox('Input Settings')

        input_mode_layout = QHBoxLayout()

        # Options for the selection box
        self.method_options = ['Bisection', 'False-Position', 'Fixed Point', 'Original Newton-Raphson',
                               'Modified Newton-Raphson1','Modified Newton-Raphson2', 'Secant']
        self.method_label = QLabel('Select method:')
        self.method_combobox = QComboBox()
        self.method_combobox.addItems(self.method_options)

        input_mode_layout.addWidget(self.method_label)
        input_mode_layout.addWidget(self.method_combobox)

        # Maximum iterations for Gauss-Seidel or Jacobi
        self.max_iterations_label = QLabel('Max Iterations:')
        self.max_iterations_spinbox = QSpinBox()
        self.max_iterations_spinbox.setMinimum(1)
        self.max_iterations_spinbox.setMaximum(1000)
        self.max_iterations_spinbox.setMaximumWidth(50)
        default_value = 100
        self.max_iterations_spinbox.setValue(default_value)

        max_iterations_layout = QHBoxLayout()
        max_iterations_layout.addWidget(self.max_iterations_label)
        max_iterations_layout.addWidget(self.max_iterations_spinbox)

        # Second Guess input
        self.second_guess_label = QLabel('Second Guess:')
        self.second_guess_edit = QLineEdit()
        second_guess_layout = QHBoxLayout()
        second_guess_layout.addWidget(self.second_guess_label)
        second_guess_layout.addWidget(self.second_guess_edit)

        # Absolute Relative Error for Gauss-Seidel or Jacobi
        self.abs_relative_error_label = QLabel('Absolute Relative Error: 1e-')
        self.abs_relative_error_spinbox = QSpinBox()
        self.abs_relative_error_spinbox.setMinimum(0)  # corresponds to 10e-15
        self.abs_relative_error_spinbox.setMaximum(15)
        self.abs_relative_error_spinbox.setValue(6)  # corresponds to 10e-6
        self.abs_relative_error_spinbox.setSingleStep(1)
        self.abs_relative_error_spinbox.setToolTip('Enter a value in the range of 15 to 0.\nFor example, 6 corresponds to 10e-6.')

        abs_relative_error_layout = QHBoxLayout()
        abs_relative_error_layout.addWidget(self.abs_relative_error_label)
        abs_relative_error_layout.addWidget(self.abs_relative_error_spinbox)

        # Significant digits input
        self.significant_digits_label = QLabel('Significant Digits:')
        self.significant_digits_spinbox = QSpinBox()
        self.significant_digits_spinbox.setMinimum(1)
        self.significant_digits_spinbox.setMaximum(15)
        self.significant_digits_spinbox.setMaximumWidth(50)
        default_value = 7
        self.significant_digits_spinbox.setValue(default_value)

        significant_digits_layout = QHBoxLayout()
        significant_digits_layout.addWidget(self.significant_digits_label)
        significant_digits_layout.addWidget(self.significant_digits_spinbox)
        # Multiplicity input
        self.multiplicity_label = QLabel('Multiplicity:')
        self.multiplicity_spinbox = QSpinBox()
        self.multiplicity_spinbox.setMinimum(1)
        self.multiplicity_spinbox.setMaximum(10)
        self.multiplicity_spinbox.setMaximumWidth(50)
        default_multiplicity = 1
        self.multiplicity_spinbox.setValue(default_multiplicity)

        multiplicity_layout = QHBoxLayout()
        multiplicity_layout.addWidget(self.multiplicity_label)
        multiplicity_layout.addWidget(self.multiplicity_spinbox)

        # Minimum x-value input
        self.min_x_label = QLabel('Min x-value for the plot:')
        self.min_x_edit = QLineEdit()
        min_x_layout = QHBoxLayout()
        min_x_layout.addWidget(self.min_x_label)
        min_x_layout.addWidget(self.min_x_edit)

        # Maximum x-value input
        self.max_x_label = QLabel('Max x-value for the plot:')
        self.max_x_edit = QLineEdit()
        max_x_layout = QHBoxLayout()
        max_x_layout.addWidget(self.max_x_label)
        max_x_layout.addWidget(self.max_x_edit)

        range_layout = QVBoxLayout()
        range_layout.addLayout(min_x_layout)
        range_layout.addLayout(max_x_layout)


        input_settings_layout = QVBoxLayout()
        input_settings_layout.addLayout(input_mode_layout)
        input_settings_layout.addLayout(max_iterations_layout)
        input_settings_layout.addLayout(abs_relative_error_layout)
        input_settings_layout.addLayout(significant_digits_layout)
        input_settings_layout.addLayout(multiplicity_layout)
        input_settings_groupbox.setLayout(input_settings_layout)

        # Equation layout within a group box named "Input"
        input_groupbox = QGroupBox('Input')
        self.equation_layout = QVBoxLayout()

        # Steps group box
        steps_groupbox = QGroupBox('Steps')
        self.steps_layout = QVBoxLayout()

        # Add a stretch to push the steps group to the top
        self.steps_layout.addStretch(1)
        self.steps_label = QLabel('HI')
        self.steps_layout.addWidget(self.steps_label)
        steps_groupbox.setLayout(self.steps_layout)

        # Answers group box
        answers_groupbox = QGroupBox('Answer')
        self.answers_layout = QVBoxLayout()

        # Add a stretch to push the answers group to the top
        self.answers_layout.addStretch(1)
        self.answers_label = QLabel('HI')
        self.answers_layout.addWidget(self.answers_label)
        answers_groupbox.setLayout(self.answers_layout)

        # Solve button
        self.solve_button = QPushButton('Solve')
        self.solve_button.setFixedSize(80, 30)
        self.solve_button.clicked.connect(lambda: self.solve_clicked())


        input_scroll_area = QScrollArea()
        input_scroll_area.setWidgetResizable(True)
        input_scroll_area.setWidget(input_groupbox)
        steps_scroll_area = QScrollArea()
        steps_scroll_area.setWidgetResizable(True)
        steps_scroll_area.setWidget(steps_groupbox)
        answer_scroll_area = QScrollArea()
        answer_scroll_area.setWidgetResizable(True)
        answer_scroll_area.setWidget(answers_groupbox)

        # Textbox for equations
        self.equation_textbox = QTextEdit()
        self.equation_textbox.setPlaceholderText("Enter equations here...")
        self.equation_textbox.setMaximumHeight(100)
        self.equation_textbox.setStyleSheet(
            "background-color: #800000; color: #eee; border: 1px solid #B22222; border-radius: 3px; padding: 5px;")

        # Initial Guess input
        self.initial_guess_label = QLabel('Initial Guess:')
        self.initial_guess_edit = QLineEdit()
        initial_guess_layout = QHBoxLayout()
        initial_guess_layout.addWidget(self.initial_guess_label)
        initial_guess_layout.addWidget(self.initial_guess_edit)

        input_settings_layout.addLayout(initial_guess_layout)
        input_settings_layout.addLayout(second_guess_layout)  # Add second guess layout
        input_settings_layout.addLayout(range_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(input_settings_groupbox)
        main_layout.addWidget(self.equation_textbox)
        self.plot_button = QPushButton('Show Plot')
        self.plot_button.setFixedSize(80, 30)
        self.plot_button.clicked.connect(self.show_plot)

        # Add the plot button to the main layout
        main_layout.addWidget(self.plot_button)
        main_layout.addWidget(self.solve_button)
        main_layout.addWidget(steps_scroll_area)
        main_layout.addWidget(answer_scroll_area)
        main_layout.addWidget(self.last_runtime_label)  # Add the Last Runtime label

        # Additional layouts
        self.setLayout(main_layout)

        self.method_combobox.currentIndexChanged.connect(self.toggle_method_options)
        self.multiplicity_label.hide()
        self.multiplicity_spinbox.hide()
        self.show()

    def toggle_method_options(self):
        if self.method_combobox.currentText() in ('Bisection', 'False-Position', 'Secant'):
            # Show the second guess input for specific methods
            self.second_guess_label.show()
            self.second_guess_edit.show()
            
            # Hide the multiplicity field if visible
            self.multiplicity_label.hide()
            self.multiplicity_spinbox.hide()
        elif self.method_combobox.currentText() == 'Modified Newton-Raphson1':
            # Show the second guess and multiplicity inputs for Modified Newton-Raphson
            self.second_guess_label.hide()
            self.second_guess_edit.hide()
            self.multiplicity_label.show()
            self.multiplicity_spinbox.show()
        else:
            # Hide the second guess and multiplicity inputs for other methods
            self.second_guess_label.hide()
            self.second_guess_edit.hide()
            self.multiplicity_label.hide()
            self.multiplicity_spinbox.hide()


    def get_actual_abs_relative_error(self):
        # Calculate the actual value from the spin box value
        return 10 ** -self.current_abs_relative_error

    def solve_clicked(self):
        print('Solve clicked')

        try:
            self.current_method = self.method_combobox.currentText()
            self.current_max_iterations = self.max_iterations_spinbox.value()
            self.current_abs_relative_error = self.abs_relative_error_spinbox.value()
            self.current_significant_digits = self.significant_digits_spinbox.value()
            self.current_multiplicity = self.multiplicity_spinbox.value()
            self.current_initial_guess = float(self.initial_guess_edit.text())  # Get the initial guess value

            if self.second_guess_label.isVisible():
                self.current_second_guess = float(self.second_guess_edit.text())
            else:
                self.current_second_guess = None

            print("Method: " + self.current_method)
            print("Max Iterations: " + str(self.current_max_iterations))
            print("Abs Relative Error: " + str(self.current_abs_relative_error))
            print("Significant Digits: " + str(self.current_significant_digits))
            print("Multiplicity: " + str(self.current_multiplicity))
            print("Initial Guess: " + str(self.current_initial_guess))
            print("Second Guess: " + str(self.current_second_guess))

            answer_text = ''
            steps_text = ''

            if self.current_method == 'Bisection':
                pass
            elif self.current_method == 'False-Position':
                pass
            elif self.current_method == 'Fixed Point':
                pass
            elif self.current_method == 'Original Newton-Raphson':
                try:
                    answer, steps = chef('Newton', self.equation_textbox.toPlainText(), self.current_initial_guess,
                                        self.get_actual_abs_relative_error(), self.current_max_iterations,
                                        self.current_significant_digits)
                    answer_text = str(answer)
                    steps_text = '\n'.join(steps)
                except Exception as e:
                    raise ValueError(f'Newton Method Error: {str(e)}')

            elif self.current_method == 'Modified Newton-Raphson1':
                try:
                    answer, steps = chef('Modified Newton1', self.equation_textbox.toPlainText(), self.current_initial_guess,
                                        self.get_actual_abs_relative_error(), self.current_max_iterations,
                                        self.current_significant_digits, self.current_multiplicity)
                    answer_text = str(answer)
                    steps_text = '\n'.join(steps)
                except Exception as e:
                    raise ValueError(f'Modified Newton1 Method Error: {str(e)}')

            elif self.current_method == 'Modified Newton-Raphson2':
                try:
                    answer, steps = chef('Modified Newton2', self.equation_textbox.toPlainText(), self.current_initial_guess,
                                        self.get_actual_abs_relative_error(), self.current_max_iterations,
                                        self.current_significant_digits)
                    answer_text = str(answer)
                    steps_text = '\n'.join(steps)
                except Exception as e:
                    raise ValueError(f'Modified Newton2 Method Error: {str(e)}')

            elif self.current_method == 'Secant':
                pass

            self.steps_label.setText(steps_text)
            self.answers_label.setText(answer_text)
            equations_text = self.equation_textbox.toPlainText()

        except ValueError as ve:
            self.showErrorMessage(f'Value Error: {str(ve)}')
        except Exception as ex:
            self.showErrorMessage(f'An unexpected error occurred: {str(ex)}')

    def stringify_steps(steps):
        return '\n'.join(steps)

    def show_plot(self):
        Expression = self.equation_textbox.toPlainText()
        Expression = Expression.replace('^', '**').lower().replace('e', 'E').replace(' ', '')
        Expression = re.sub(r'(\d+)x', r'\1*x', Expression)

        try:
            x = Symbol('x')
            fx = sympify(Expression)
            f1x = diff(fx)
            f2x = diff(f1x)
            # Close previous plots
            plt.close('all')

            # Get the min and max x-values from the user input
            min_x = float(self.min_x_edit.text())
            max_x = float(self.max_x_edit.text())

            # Plot the new expression with the specified range
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
    matrix_input_app = NonLinearTab()
    sys.exit(app.exec_())
