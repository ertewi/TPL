import sys
import re

class DPDA:
    def __init__(self, transitions, start_state, start_stack_symbol, accepting_states):
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.accepting_states = accepting_states

    def print_transitions(self):
        print("\nМП-преобразователь:")
        for (state, input_symbol, stack_top), (new_state, stack_operation, output_symbols) in self.transitions.items():
            print(f"  δ({state}, '{input_symbol}', '{stack_top}') = ({new_state}, '{stack_operation}', '{output_symbols}')")

    def simulate(self, input_string, output_array, mode):
        state = self.start_state
        stack = [self.start_stack_symbol]
        input_index = 0

        step = 0
        while True:
            step += 1
            current_input = input_string[input_index] if input_index < len(input_string) else None
            output_display = current_input
            if mode == '1' and current_input is not None and re.match(r'[a-zA-Z0-9_]+$', current_input):
                current_input = 'a'
            stack_top = stack[-1] if stack else None

            input_display = current_input if current_input is not None else 'EOF'
            print(f"Шаг {step}")

            if (input_index == len(input_string) and state in self.accepting_states):
                return True, None

            transition_found = False
            new_state = '?'
            stack_op = '?'
            output_symbols = '?'

            if current_input is not None and (state, current_input, stack_top) in self.transitions:
                new_state, stack_op, output_symbols = self.transitions[(state, current_input, stack_top)]
                input_display = current_input
                transition_found = True
                input_index += 1
                if mode == '1' and current_input == 'a' and output_symbols == 'a':
                    output_array.append(output_display)
                else:
                    output_array.append(output_symbols)


            elif (state, 'λ', stack_top) in self.transitions:
                new_state, stack_op, output_symbols = self.transitions[(state, 'λ', stack_top)]
                input_display = 'λ'
                transition_found = True
                if mode == '1' and current_input == 'a' and output_symbols == 'a':
                    output_array.append(output_display)
                else:
                    output_array.append(output_symbols)

            if not transition_found:
                reason = f"Нет перехода из состояния '{state}' "
                reason += f"при входном символе '{current_input if current_input else 'EOF'}' "
                reason += f"и символе стека '{stack_top}'"
                return False, reason

            print(f"  δ({state}, '{input_display}', '{stack_top}') = ({new_state}, '{stack_op}', '{output_symbols}')")

            if stack_op == 'ε':
                if stack:
                    stack.pop()
            elif stack_op == 'λ':
                pass
            else:
                if stack:
                    stack.pop()
                for symbol in reversed(stack_op):
                    stack.append(symbol)

            state = new_state

            if step > 1000:
                reason = "Превышено максимальное количество шагов"
                return False, reason


def read_dpda_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        transitions = {}
        start_state = None
        start_stack_symbol = None
        accepting_states = set()

        for line in lines:
            if line.startswith('δ(') or line.startswith('d('):
                parts = line.split('=')
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()

                    left_clean = left.replace('δ(', '').replace('d(', '').replace('\)', 'custom').replace(')', '').replace('custom', ')')
                    left_parts = [part.strip().strip("'") for part in left_clean.split(',')]

                    if len(left_parts) == 3:
                        state = left_parts[0]
                        input_symbol = left_parts[1]
                        stack_top = left_parts[2]

                        right_clean = right.replace('(', '').replace(')', '')
                        right_parts = [part.strip().strip("'") for part in right_clean.split(',')]

                        if len(right_parts) == 3:
                            new_state = right_parts[0]
                            stack_operation = right_parts[1]
                            output_symbols = right_parts[2]

                            transitions[(state, input_symbol, stack_top)] = (new_state, stack_operation, output_symbols)

            elif 'начальное состояние' in line.lower():
                parts = line.split(':')
                if len(parts) == 2:
                    start_state = parts[1].strip()

            elif 'начальный символ стека' in line.lower():
                parts = line.split(':')
                if len(parts) == 2:
                    start_stack_symbol = parts[1].strip()

            elif 'конечные состояния' in line.lower():
                parts = line.split(':')
                if len(parts) == 2:
                    accepting_states = set(part.strip() for part in parts[1].split(','))

        if not start_state or not start_stack_symbol or not accepting_states:
            print("Ошибка: не все параметры автомата указаны в файле")
            return None

        return DPDA(transitions, start_state, start_stack_symbol, accepting_states)

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Введите имя файла с описанием МП-преобразователя: ")

    dpda = read_dpda_from_file(filename)

    if dpda is None:
        print("Не удалось загрузить ДМП-автомат из файла")
        return

    dpda.print_transitions()

    print(f"\nПараметры автомата:")
    print(f"Начальное состояние: {dpda.start_state}")
    print(f"Начальный символ стека: {dpda.start_stack_symbol}")
    print(f"Конечные состояния: {dpda.accepting_states}")

    while True:
        print("\nВыберите режим")
        print("1. Обратная польская нотация")
        print("2. Обычный преобразователь")
        print("q. Выход")
        mode = input(": ")
        if mode.lower() == 'q':
            break

        input_string = input("\nВведите цепочку для проверки: ")
        output_array = []

        accepted, reason = dpda.simulate(input_string, output_array, mode)
        output_array = list(map(lambda x: x if x != 'λ' else '', output_array))
        output_string = ''.join(output_array)

        if accepted:
            print(f"Цепочка '{input_string}' принадлежит заданному языку")
            print(f"Перевод: '{output_string}'")
        else:
            print(f"Цепочка '{input_string}' не принадлежит заданному языку.")
            if reason:
                print(f"Причина: {reason}")


if __name__ == "__main__":
    main()