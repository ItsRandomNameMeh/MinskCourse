import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFileDialog, QPushButton, QVBoxLayout, QTextEdit, QScrollArea, \
    QGroupBox, QFormLayout


from logicclass import MinskCounterMachine


class MinskMachineApp(QWidget):

    __counters = 16
    def __init__(self):
        super().__init__()

        self.minsk_machine = MinskCounterMachine(num_counters=15)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Minsk Counter Machine Simulator')

        # Создаем TextBox для ввода начального состояния
        self.state_label = QLabel('Initial State:')
        self.state_input = QLineEdit(self)

        # Создаем TextBox для ввода начальных значений счетчиков
        self.counters_inputs = []

        # Создаем QScrollArea для счетчиков
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Создаем виджет, который будет содержать все TextBox для счетчиков
        self.scroll_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        # Создаем компоновку для размещения TextBox для счетчиков внутри виджета
        self.scroll_layout = QFormLayout(self.scroll_widget)

        # Инициализируем счетчики значениями по умолчанию
        for i in range(self.__counters):
            input_box = QLineEdit(self)
            input_box.setText('0')  # Задаем значение по умолчанию
            self.counters_inputs.append(input_box)
            self.scroll_layout.addRow(f'Counter {i + 1}:', input_box)

        # TextBox для ввода правил переходов
        self.transitions_label = QLabel('Transitions:')
        self.transitions_input = QTextEdit(self)

        # Кнопка запуска симуляции
        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_simulation)

        # TextBox для вывода результата
        self.result_label = QLabel('Result:')
        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)

        # Создаем основную композицию
        self.load_file_button = QPushButton('Load Transitions from File', self)
        self.load_file_button.clicked.connect(self.load_transitions_from_file)

        # Основная композиция
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.state_label)
        main_layout.addWidget(self.state_input)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.transitions_label)
        main_layout.addWidget(self.transitions_input)
        main_layout.addWidget(self.load_file_button)  # Добавляем кнопку
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.result_output)

    def load_transitions_from_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a file", "", "Text Files (.txt);;All Files ()",
                                                  options=options)
        if file_name:
            with open(file_name, 'r') as file:
                transitions_data = file.read()
                self.transitions_input.setPlainText(transitions_data)

    def run_simulation(self):
        # Очищаем поле вывода перед каждой генерацией
        self.result_output.clear()

        initial_state = self.state_input.text()
        initial_counters = [int(input_box.text()) for input_box in self.counters_inputs]

        self.minsk_machine.transitions = eval(
            self.transitions_input.toPlainText())  # Правильно обработать строку с переходами

        initial_config = (initial_state, initial_counters)
        all_configs = self.minsk_machine.execute(initial_config)

        # Форматируем вывод
        for i, config in enumerate(all_configs):
            state, counters = config
            output_text = f"Step {i + 1}: State={state}, Counters={counters}\n"
            self.result_output.insertPlainText(output_text)

        result_text = f"\nFinal Configuration: {all_configs[-1]}"
        self.result_output.insertPlainText(result_text)

        logs_folder = "Logs"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(logs_folder, f"{timestamp}.txt")
        with open(file_path, 'w') as file:
            file.write(result_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinskMachineApp()
    ex.show()
    sys.exit(app.exec_())
