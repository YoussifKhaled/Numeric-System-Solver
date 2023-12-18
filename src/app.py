import sys
import time
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QGroupBox, QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea, QDesktopWidget
from PyQt5 import QtGui
import qtpy

from LinearSolver import LinearSolverEngine

class MatrixInputApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Matrix Input')

        # Get screen geometry
        screen_rect = QDesktopWidget().screenGeometry()

        # Set maximum size to the full screen
        self.setMaximumSize(screen_rect.width(), screen_rect.height())

        self.mode = 'equations'
        self.coefficient_inputs = []

        # Set dark theme stylesheet
        self.setStyleSheet('''
            QWidget {
                background-color: #333;
                color: #eee;
            }
            QGroupBox {
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 10px;
            }
            QLineEdit, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #444;
                color: #eee;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QRadioButton {
                spacing: 5px;
            }
        ''')

        # Set window opacity
        self.setWindowOpacity(0.92)
        self.last_runtime_label = QLabel('Last Runtime: N/A')
        self.last_runtime_label.setStyleSheet('color: #ffbb00')  # Set text color to yellow

        # Input settings group box
        input_settings_groupbox = QGroupBox('Input Settings')

        # Input mode widgets
        self.input_mode_label = QLabel('Select input mode:')
        self.equation_radio_button = QRadioButton('Equations')
        self.matrix_radio_button = QRadioButton('Matrix')

        input_mode_layout = QHBoxLayout()
        input_mode_layout.addWidget(self.input_mode_label)
        input_mode_layout.addWidget(self.equation_radio_button)
        input_mode_layout.addWidget(self.matrix_radio_button)

        # Options for the selection box
        self.method_options = ['Gauss Elimination', 'Gauss-Jordan', 'LU Decomposition', 'Gauss-Seidel', 'Jacobi-Iteration']
        self.method_label = QLabel('Select method:')
        self.method_combobox = QComboBox()
        self.method_combobox.addItems(self.method_options)

        input_mode_layout.addWidget(self.method_label)
        input_mode_layout.addWidget(self.method_combobox)

        # LU Decomposition options
        self.lu_options_label = QLabel('LU Decomposition Options:')
        self.lu_options_combobox = QComboBox()
        self.lu_options_combobox.addItems(['Doolittle Form', 'Crout Form', 'Cholesky Form'])
        self.lu_options_label.setVisible(False)
        self.lu_options_combobox.setVisible(False)

        lu_options_layout = QHBoxLayout()
        lu_options_layout.addWidget(self.lu_options_label)
        lu_options_layout.addWidget(self.lu_options_combobox)

        # Maximum iterations for Gauss-Seidel or Jacobi
        self.max_iterations_label = QLabel('Max Iterations:')
        self.max_iterations_spinbox = QSpinBox()
        self.max_iterations_spinbox.setMinimum(1)
        self.max_iterations_spinbox.setMaximum(1000)
        self.max_iterations_spinbox.setMaximumWidth(50)
        self.max_iterations_label.setVisible(False)
        self.max_iterations_spinbox.setVisible(False)

        max_iterations_layout = QHBoxLayout()
        max_iterations_layout.addWidget(self.max_iterations_label)
        max_iterations_layout.addWidget(self.max_iterations_spinbox)


        # Absolute Relative Error for Gauss-Seidel or Jacobi
        self.abs_relative_error_label = QLabel('Absolute Relative Error: 10e-')
        self.abs_relative_error_spinbox = QSpinBox()
        self.abs_relative_error_spinbox.setMinimum(0)  # corresponds to 10e-15
        self.abs_relative_error_spinbox.setMaximum(15)
        self.abs_relative_error_spinbox.setValue(6)  # corresponds to 10e-6
        self.abs_relative_error_spinbox.setSingleStep(1)
        self.abs_relative_error_spinbox.setToolTip('Enter a value in the range of 15 to 0.\nFor example, 6 corresponds to 10e-6.')

        abs_relative_error_layout = QHBoxLayout()
        abs_relative_error_layout.addWidget(self.abs_relative_error_label)
        abs_relative_error_layout.addWidget(self.abs_relative_error_spinbox)
        self.abs_relative_error_label.setVisible(False)
        self.abs_relative_error_spinbox.setVisible(False)


        # Significant digits input
        self.significant_digits_label = QLabel('Significant Digits:')
        self.significant_digits_spinbox = QSpinBox()
        self.significant_digits_spinbox.setMinimum(1)
        self.significant_digits_spinbox.setMaximum(15)
        self.significant_digits_spinbox.setMaximumWidth(50)

        significant_digits_layout = QHBoxLayout()
        significant_digits_layout.addWidget(self.significant_digits_label)
        significant_digits_layout.addWidget(self.significant_digits_spinbox)

        input_settings_layout = QVBoxLayout()
        input_settings_layout.addLayout(input_mode_layout)
        input_settings_layout.addLayout(lu_options_layout)
        input_settings_layout.addLayout(max_iterations_layout)
        input_settings_layout.addLayout(abs_relative_error_layout)
        input_settings_layout.addLayout(significant_digits_layout)

        # Dimensions input widgets
        self.equation_count_label = QLabel('Enter the number of equations (and variables):')
        self.equation_count_input = QLineEdit()
        self.submit_button = QPushButton('Submit')

        dimensions_submit_layout = QHBoxLayout()
        dimensions_submit_layout.addWidget(self.equation_count_label)
        dimensions_submit_layout.addWidget(self.equation_count_input)
        dimensions_submit_layout.addWidget(self.submit_button)

        input_settings_layout.addLayout(dimensions_submit_layout)

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
        self.solve_button.clicked.connect(self.solve_clicked)
        input_scroll_area = QScrollArea()
        input_scroll_area.setWidgetResizable(True)
        input_scroll_area.setWidget(input_groupbox)
        steps_scroll_area = QScrollArea()
        steps_scroll_area.setWidgetResizable(True)
        steps_scroll_area.setWidget(steps_groupbox)
        answer_scroll_area = QScrollArea()
        answer_scroll_area.setWidgetResizable(True)
        answer_scroll_area.setWidget(answers_groupbox)
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(input_settings_groupbox)
        main_layout.addWidget(input_scroll_area)
        input_groupbox.setLayout(self.equation_layout)
        main_layout.addWidget(self.solve_button)
        main_layout.addWidget(steps_scroll_area)
        main_layout.addWidget(answer_scroll_area)
        main_layout.addWidget(self.last_runtime_label)  # Add the Last Runtime label

        # Additional layouts
        self.setLayout(main_layout)

        self.submit_button.clicked.connect(self.submit_clicked)
        self.equation_radio_button.toggled.connect(self.toggle_input_mode)
        self.matrix_radio_button.toggled.connect(self.toggle_input_mode)
        self.method_combobox.currentIndexChanged.connect(self.toggle_method_options)
        self.table = None
        self.table2 = None
        self.equations = None
        self.initial_guess_label = None
        self.initial_guess_layout = None
        
        self.show()
    def toggle_input_mode(self):
        if self.equation_radio_button.isChecked():
            self.mode = 'equations'
        elif self.matrix_radio_button.isChecked():
            self.mode = 'matrix'
        self.toggle_method_options()

    def toggle_method_options(self):
        selected_method = self.method_combobox.currentText()
        if selected_method == 'LU Decomposition':
            self.lu_options_label.setVisible(True)
            self.lu_options_combobox.setVisible(True)
            self.max_iterations_label.setVisible(False)
            self.max_iterations_spinbox.setVisible(False)
            self.abs_relative_error_label.setVisible(False)
            self.abs_relative_error_spinbox.setVisible(False)
        elif selected_method in ('Gauss-Seidel', 'Jacobi-Iteration'):
            self.lu_options_label.setVisible(False)
            self.lu_options_combobox.setVisible(False)
            self.max_iterations_label.setVisible(True)
            self.max_iterations_spinbox.setVisible(True)
            self.abs_relative_error_label.setVisible(True)
            self.abs_relative_error_spinbox.setVisible(True)
        else:
            self.lu_options_label.setVisible(False)
            self.lu_options_combobox.setVisible(False)
            self.max_iterations_label.setVisible(False)
            self.max_iterations_spinbox.setVisible(False)
            self.abs_relative_error_label.setVisible(False)
            self.abs_relative_error_spinbox.setVisible(False)

    def create_matrix_table(self, matrix_size):
        # Create a horizontal layout to hold both tables
        matrix_layout = QHBoxLayout()

        # First table (table)
        self.table = QTableWidget(self)
        self.table.setRowCount(matrix_size)
        self.table.setColumnCount(matrix_size)

        for i in range(matrix_size):
            for j in range(matrix_size):
                item = QTableWidgetItem()
                item.setText('0')  # Set default value to zero
                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        matrix_layout.addWidget(self.table)

        self.table2 = QTableWidget(self)
        self.table2.setRowCount(matrix_size)
        self.table2.setColumnCount(1)

        for i in range(matrix_size):
            item = QTableWidgetItem('0')
            self.table2.setItem(i, 0, item)

        self.table2.resizeColumnsToContents()
        self.table2.resizeRowsToContents()

        matrix_layout.addWidget(self.table2)

        self.equation_layout.addLayout(matrix_layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.clear_layout(item.layout())

    def create_equation_input_boxes(self):
        self.coefficient_inputs.clear()  # Clear the list before adding new inputs

        self.equations = QVBoxLayout()

        for i in range(self.equation_count):
            answer_input = QLineEdit()
            answer_input.setText('0')

            equation_layout = QHBoxLayout()
            equation_layout.addWidget(QLabel(f'Equation {i + 1}: '))

            for j in range(self.equation_count):
                coefficient_input = QLineEdit()
                coefficient_input.setText('0')
                self.coefficient_inputs.append(coefficient_input)
                equation_layout.addWidget(coefficient_input)
                equation_layout.addWidget(QLabel(f'x{j + 1}'))

            equation_layout.addWidget(QLabel(' = '))
            equation_layout.addWidget(answer_input)

            self.equations.addLayout(equation_layout)
        self.equation_layout.addLayout(self.equations)

    def get_actual_abs_relative_error(self):
        # Calculate the actual value from the spin box value
        return 10 ** -self.current_abs_relative_error
    def submit_clicked(self):
        self.equation_count = int(self.equation_count_input.text())
        if self.equations is not None:
            # Clear the existing layout and its children
            self.clear_layout(self.equations)
            self.equations.setParent(None)
        if self.table is not None:
            self.table.setParent(None)
        if self.table2 is not None:
            self.table2.setParent(None)
        if self.initial_guess_label is not None:
            self.initial_guess_label.setParent(None)
        if self.initial_guess_layout is not None:
            self.clear_layout(self.initial_guess_layout)
            self.initial_guess_layout.setParent(None)

        if self.mode == 'equations':
            self.create_equation_input_boxes()
        elif self.mode == 'matrix':
            matrix_size = int(self.equation_count)
            self.create_matrix_table(matrix_size)

        self.equation_count_input.clear()
        self.current_method = self.method_combobox.currentText()
        self.current_lu_option = self.lu_options_combobox.currentText()
        self.current_max_iterations = self.max_iterations_spinbox.value()
        self.current_abs_relative_error = self.abs_relative_error_spinbox.value()
        self.current_significant_digits = self.significant_digits_spinbox.value()
        self.current_mode = self.mode

        for input_field in self.coefficient_inputs:
            input_field.setText('0')  # Set the value to zero

        if self.current_method in ('Jacobi-Iteration', 'Gauss-Seidel'):
            # Initial Guess Section
            self.initial_guess_label = QLabel('Initial Guess:')
            self.initial_guess_layout = QHBoxLayout()

            for i in range(self.equation_count):
                initial_guess_input = QLineEdit()
                initial_guess_input.setText('0')
                self.initial_guess_layout.addWidget(initial_guess_input)

            self.initial_guess_layout.addStretch(1)

            self.equation_layout.addWidget(self.initial_guess_label)
            self.equation_layout.addLayout(self.initial_guess_layout)
        
        self.steps_label.setText("Hi")
        self.answers_label.setText("Hi")


    def solve_clicked(self):
        # Print all input data
        print("Input Data:")
        print(f"Mode: {self.mode}")
        print(f"Equation Count: {self.equation_count}")
        print(f"Method: {self.method_combobox.currentText()}")
        print(f"LU Options: {self.lu_options_combobox.currentText()}")
        print(f"Max Iterations: {self.max_iterations_spinbox.value()}")
        print(f"Absolute Relative Error: {self.abs_relative_error_spinbox.value()}")
        print(f"Significant Digits: {self.significant_digits_spinbox.value()}")
        print("Initial Guess:")
        initial_guess_values = []
        if self.initial_guess_layout is not None:
            for i in range(self.initial_guess_layout.count()):
                initial_guess_widget = self.initial_guess_layout.itemAt(i).widget()
                if isinstance(initial_guess_widget, QLineEdit):
                    if initial_guess_widget.text() == '':
                        initial_guess_widget.setText('0')
                    initial_guess_values.append(float(initial_guess_widget.text()))
            print(f"Values: {initial_guess_values}")

        if self.current_mode == 'matrix':
            # Print matrix table data
            print("Matrix Table Data:")
            for i in range(self.table.rowCount()):
                row_data = []
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    if item.text() == '':
                        item.setText('0')
                    row_data.append(float(item.text()))
                print(f"Row {i + 1}: {row_data}")

        elif self.current_mode == 'equations':
            # Print equation input data
            print("Equation Input Data:")
            for i in range(self.equation_count):
                equation_data = []
                for j in range(self.equation_count):
                    
                    coefficient_input = self.coefficient_inputs[i * self.equation_count + j]
                    if coefficient_input.text() == '':
                        coefficient_input.setText('0')
                    equation_data.append(float(coefficient_input.text()))
                answer_input = self.equations.itemAt(i).itemAt(self.equation_count * 2 + 2).widget()
                print(f"Equation {i + 1}: Coefficients={equation_data}, Answer={float(answer_input.text())}")
        print("matrix data", self.get_matrix_data())
        print("method", self.method_combobox.currentText())
        print("initial guess", initial_guess_values)
        print("iterations", self.max_iterations_spinbox.value())
        print("tol", self.get_actual_abs_relative_error())
        print("precision", self.significant_digits_spinbox.value())


        engine = LinearSolverEngine(
            method=self.current_method,
            matrix=self.get_matrix_data(),
            initial_guess=initial_guess_values,
            iterations=self.current_max_iterations,
            tol=self.get_actual_abs_relative_error(),
            precision=self.current_significant_digits
        )

        # Solve the linear system and get results
        try:
            start_time = time.time() 
            ans, steps = engine.solve()
            end_time = time.time()  # Measure the end time
            runtime = end_time - start_time

            # Update the Last Runtime label
            self.last_runtime_label.setText(f'Last Runtime: {runtime:.4f} seconds')

        except ValueError as e:
            print(f"Error: {e}")
            self.steps_label.setText(f"Error: {e}")
            self.answers_label.setText(f"Error: {e}")
            return
        print(f"Answer: {ans}")
        print("Steps:")
        print(engine.format_steps(steps))

        self.steps_label.setText(engine.format_steps(steps))
        self.answers_label.setText(engine.format_answer(ans))




    def get_matrix_data(self):
        matrix_size = self.equation_count
        matrix_data = []

        if self.current_mode == 'matrix':
            for i in range(matrix_size):
                row_data = []
                for j in range(matrix_size):
                    item = self.table.item(i, j)
                    row_data.append(float(item.text()))
                answer_item = float(self.table2.item(i, 0).text())
                row_data.append(answer_item)
                matrix_data.append(row_data)

        elif self.current_mode == 'equations':
            for i in range(matrix_size):
                equation_data = []
                for j in range(matrix_size):
                    coefficient_input = self.coefficient_inputs[i * matrix_size + j]
                    equation_data.append(float(coefficient_input.text()))
                answer_input = self.equations.itemAt(i).itemAt(matrix_size * 2 + 2).widget()
                equation_data.append(float(answer_input.text()))
                matrix_data.append(equation_data)

        print(matrix_data)
        return matrix_data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    matrix_input_app = MatrixInputApp()
    sys.exit(app.exec_())