import re
import random


def calculate(formula):
    def tokenize(formula):

        # Удаление текста команды
        formula = re.sub(r'^/roll', r'', formula)
        formula = re.sub(r'^/r', r'', formula)

        # Проверка на количество скобочек
        if formula.count('(') != formula.count(')'):
            raise Exception('Incorrect number of parentheses')

        # Добавление унарного оператора "±" для отрицательных чисел
        formula = re.sub(r'^-', r'±', formula)
        formula = re.sub(r'\(-', r'(±', formula)

        # Добавление унарного оператора "D" для краткой формы записи дайсов
        formula = re.sub(r'(?<!\d)d', r'D', formula)

        # Разбиение формулы на токены
        tokens = re.findall(r'#.*|\[.*]|dh|dl|kh|kl|d|D|\d+\.?\d*|±|\+|-|\*|/|\(|\)|\S', formula)

        # (#.*)                 - Комментарии
        # (dh|dl|kh|kl|d|D)     - Операции с кубасами
        # (\d+\.?\d*)           - Числа
        # (±|\+|\-|\*|\/|\(|\)) - Операторы

        if len(tokens):
            return tokens
        else:
            raise Exception('Command is empty')

    def to_rpn(tokens):
        # Приоритет действий
        precedence = {'+': 1,
                      '-': 1,
                      '*': 2,
                      '/': 2,
                      '±': 3,
                      'D': 4,
                      'd': 4}
        rpn = []
        stack = []

        # Смотрим все токены и переписываем в обратную польскую нотацию
        for token in tokens:

            if re.match(r'\d+\.?\d*', token):
                rpn.append(float(token))

            elif token == '(':
                stack.append(token)

            elif token == ')':
                while stack and stack[-1] != '(':
                    rpn.append(stack.pop())
                stack.pop()

            elif token in precedence:
                while stack and stack[-1] != '(' and precedence[token] <= precedence[stack[-1]]:
                    rpn.append(stack.pop())
                stack.append(token)
            else:
                raise Exception('Incorrect characters entered')
        while stack:
            rpn.append(stack.pop())

        return rpn

    def rpn_calc(rpn):

        stack = []

        for token in rpn:
            if type(token) is float or type(token) is int:
                stack.append(token)
            elif token == '±':
                stack.append(-stack.pop())
            elif token in ['+', '-', '*', '/']:
                b = stack.pop()
                a = stack.pop()
                stack.append(eval(f'{a} {token} {b}'))
            elif token == 'D':
                a = stack.pop()
                stack.append(random.randint(1, a))
            elif token == 'd':
                b = int(stack.pop())
                a = int(stack.pop())
                r = []
                for i in range(a):
                    r.append(random.randint(1, b))
                stack.append(sum(r))
        if len(stack) == 1:
            return stack[0]
        else:
            raise Exception('Wrong command')

    try:
        tokens = tokenize(formula)
        rpn = to_rpn(tokens)
        return re.sub(r'\.0+$', r'', str(rpn_calc(rpn)))
    except Exception as err:
        return str(err)


if __name__ == "__main__":
    formula = "x"
    print("Input: " + formula)
    print("Result: " + calculate(formula))
