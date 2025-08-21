import re
from random import randint

class DiceCalculator:
    def __init__(self):
        self.result = {}

    # Токенизатор
    def tokenize(self, expression):
        comment = expression.partition("#")[2].lstrip()
        expression = expression.partition("#")[0].replace(" ", "")
        pattern = r'''
            \d*\.?\d*d\d\.?\d*+k?\d*[l;h]?  # Кубасы
            |\d*\.?\d+                      # Целые числа и десятичные дроби
            |[+\-*/()]                      # Арифметика и скобки
            |.+
        '''
        tokens = re.findall(pattern, expression, re.VERBOSE)
        tokens = self.unary_fix(tokens)
        return tokens, comment

    def roll_dices(self, dice_expr):
        rolls = []
        excluded_rolls = []

        if dice_expr.startswith('d'):
            dice_expr = '1' + dice_expr

        parts = re.split(r'[dkhl]', dice_expr.lower())
        dice_num = int(parts[0])
        dice_sides = int(parts[1])

        for i in range(dice_num):
            rolls.append(randint(1, dice_sides))

        if 'k' not in dice_expr:
            keep_rolls = rolls
            roll_sum = sum(rolls)
        else:
            if parts[2] == '':
                parts[2] = 1

            keep = int(parts[2])

            if keep > dice_num:
                raise Exception('Keeped dices more than total count')

            sorted_rolls = sorted(rolls) if 'l' in dice_expr else sorted(rolls, reverse=True)
            keep_rolls = sorted_rolls[:keep]
            excluded_rolls = sorted_rolls[keep:]
            roll_sum = sum(keep_rolls)
        return roll_sum, keep_rolls, excluded_rolls


    # Добавление нулей перед унарными операциями
    def unary_fix(self, tokens):
        result = []

        for i, token in enumerate(tokens):
            if token in ['-', '+'] and (i == 0 or tokens[i - 1] == '('):
                result.append('0')
            result.append(token)

        return result

    # Преобразование в постфиксную запись
    def to_rpn(self, tokens):
        precedence = {'+': 1,
                      '-': 1,
                      '*': 2,
                      '/': 2}

        rpn = []
        stack = []

        for token in tokens:
            if re.match(r'^\d*d\d+k?\d*[l;h]?$', token):
                rpn.append(token)
            elif re.match(r'^\d*\.?\d+$', token):
                rpn.append(token)
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
                raise Exception('incorrect characters entered')
        if '(' in stack:
            raise Exception('incorrect number of parentheses')
        while stack:
            rpn.append(stack.pop())
        return rpn

    def rpn_evaulate(self, rpn):
        stack = []
        dices = {}

        for token in rpn:
            if re.match(r'^\d*d\d+k?\d*[l;h]?$', token):
                roll = self.roll_dices(token)
                stack.append(roll[0])
                dices[token] = [roll[1], roll[2]]
            elif re.match(r'^\d*\.?\d+$', token):
                stack.append(token)
            elif token in ['+', '-', '*', '/']:
                b = stack.pop()
                a = stack.pop()
                stack.append(eval(f'{a} {token} {b}'))
        if len(stack) == 1:
            return stack[0], dices
        else:
            raise Exception('Wrong command')


    def calculate(self, expression):
        try:
            tokens, comment = self.tokenize(expression)
            rpn = self.to_rpn(tokens)
            answer = self.rpn_evaulate(rpn)

            self.result['expression'] = expression
            self.result['tokens'] = tokens
            self.result['rpn'] = rpn
            self.result['comment'] = comment
            self.result['answer'] = answer[0]
            self.result['dices'] = answer[1]
        except Exception as err:
            return {'expression':expression, 'error':err.args[0]}

        return self.result

def answer_format(answer):
    if 'error' in answer:
        return f'Ошибка: {answer['error']}'
    else:
        text = f'Результат: <b>{answer['answer']}</b>\n<blockquote>'
        for exp, roll in answer['dices'].items():
            text += f'\n{exp}:'
            for dice in roll[0]:
                text += f' <b>{dice}</b>'
            for dice in roll[1]:
                text += f' <s>{dice}</s>'
        text += '</blockquote>'
        if 'comment' in answer:
            text += f'\n\n<i>{answer['comment']}</i>'
        return text


if __name__ == "__main__":
    calc = DiceCalculator()
    #expression = input("Input: ")
    expressions = [
                  "4d6k3h"
                  ]
    # Для особых случаев тестирования:
    test_cases = [
        # Граничные значения
        "1d1",  # минимальный дайс
        "1d1000",  # большой дайс
        "100d6",  # много дайсов
        "1d6k1h",  # keep 1 из 1
        "2d6k2h",  # keep все

        # Сложные выражения
        "2d6 + 3 * (d20 - 5)",
        "4d6k3h + 2d8k1h * 2",

        # Специальные символы
        "2d6 + 3.5",  # дробные числа
    ]

    # Для проверки обработки ошибок:
    error_cases = [
        "2d6 + ",  # незавершенное
        "d",  # неполное
        "2d6 + 3d",  # неполное дайс
        "2d6 + abc",  # недопустимые символы
        "2d6 / 0",  # деление на ноль
        "(2d6 + 3",  # незакрытая скобка
        "2d6 + 3)",  # неоткрытая скобка
    ]

    print('*** expressions ***')
    for expression in expressions:
        output = calc.calculate(expression)
        print(answer_format(output))

 #   print('*** Correct expressions ***')
 #   for expression in test_cases:
 #       output = calc.calculate(expression)
 #       print(answer_format(output))

#    print('*** Incorrect expressions ***')
#    for expression in error_cases:
#        output = calc.calculate(expression)
#        print(answer_format(output))