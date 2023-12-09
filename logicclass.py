
class MinskCounterMachine:
    def __init__(self, num_counters):
        self.num_counters = num_counters
        self.transitions = []

    def add_transition(self, state, increment, goto, next_state):
        self.transitions.append({
            'state': state,
            'increment': increment,
            'goto': goto,
            'next_state': next_state
        })

    def execute(self, initial_config):
        configs_history = []  # Список для хранения промежуточных конфигураций
        current_config = list(initial_config)

        while True:
            current_state, counters = current_config
            halted = True

            # Вывод информации о текущей конфигурации
            configs_history.append(current_config)

            for transition in self.transitions:
                if transition['state'] == current_state:
                    halted = False
                    counter_index = transition['increment'] - 1
                    counters[counter_index] += 1
                    current_state = transition['next_state']
                    goto_state = transition['goto']

                    current_config = (current_state, counters[:])

                    if goto_state is not None:
                        current_config = (goto_state, counters[:])

                    break

            if halted:
                break

        return configs_history