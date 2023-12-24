from logicclass import MinskCounterMachine

import unittest
import time

class TestMinskCounterMachine(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр MinskCounterMachine перед каждым тестом
        self.machine = MinskCounterMachine(num_counters=3)

    def log_test_info(self, function_name, input_data, result, output_data, execution_time):
        print(f"Function: {function_name}")
        print(f"Input: {input_data}")
        print(f"Result: {result}")
        print(f"Expected Output: {output_data}")
        print(f"Execution Time: {execution_time:.6f} seconds")
        print()

    def test_add_transition(self):
        # Проверяем, что метод add_transition корректно добавляет переход
        function_name = "add_transition"
        start_time = time.time()
        self.machine.add_transition(1, 1, None, 2)
        execution_time = time.time() - start_time
        self.assertEqual(len(self.machine.transitions), 1)
        self.log_test_info(function_name, "N/A", "N/A", "N/A", execution_time)

    def test_execute_single_transition(self):
        # Проверяем выполнение машины с единственным переходом
        function_name = "execute_single_transition"
        self.machine.add_transition(1, 1, None, 2)
        initial_config = (1, [0, 0, 0])
        start_time = time.time()
        result = self.machine.execute(initial_config)
        execution_time = time.time() - start_time
        self.assertEqual(len(result), 2)  # Два шага: начальное состояние и конечное
        self.assertEqual(result[-1], (2, [1, 0, 0]))
        self.log_test_info(function_name, initial_config, result, (2, [1, 0, 0]), execution_time)



if __name__ == '__main__':
    unittest.main()
