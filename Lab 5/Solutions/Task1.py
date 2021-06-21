from tkinter import Button, Tk, StringVar, Entry
from math import factorial, pi, log10, sqrt
from unicodedata import lookup

expression_to_display = ''
expression_to_execute = ''
pi_symbol = lookup("GREEK CAPITAL LETTER PI")
delete_char_symbol = lookup("LEFTWARDS ARROW")
font_tuple = ("Comic Sans MS", 11, "bold")
accepted_chars_to_delete = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-', '/', '*']


def concat_key(pressed_key):
    global expression_to_display
    global expression_to_execute

    expression_to_display = str(expression_to_display) + pressed_key
    if pressed_key == pi_symbol:
        expression_to_execute = expression_to_execute + ' pi '
    else:
        expression_to_execute = expression_to_execute + pressed_key

    expression_to_calculate.set(expression_to_display)


def execute_button_clear():
    global expression_to_display
    global expression_to_execute

    expression_to_display = ''
    expression_to_execute = ''
    expression_to_calculate.set('')


def execute_button_operator(operator_display, operator_calculate):
    global expression_to_display
    global expression_to_execute

    if operator_display == '!':
        expression_to_display = '(' + str(expression_to_display) + ') ' + operator_display + ' '
        expression_to_execute = operator_calculate + '(' + expression_to_execute + ')'
    elif operator_display == 'sqrt' or operator_display == 'log':
        expression_to_display = operator_display + '(' + str(expression_to_display) + ') '
        expression_to_execute = operator_calculate + '(' + expression_to_execute + ')'
    elif operator_display == '|x|':
        expression_to_display = '|' + str(expression_to_display) + '| ' + ' '
        expression_to_execute = operator_calculate + '(' + expression_to_execute + ')'
    elif operator_display == 'mod' or operator_display == '^':
        expression_to_display = str(expression_to_display) + ' ' + operator_display + ' '
        expression_to_execute = expression_to_execute + operator_calculate
    elif operator_display == '1/':
        expression_to_display = operator_display + '(' + str(expression_to_display) + ') '
        expression_to_execute = expression_to_execute + operator_calculate

    expression_to_calculate.set(expression_to_display)


def execute_button_delete_char():
    global expression_to_display
    global expression_to_execute

    if accepted_chars_to_delete.count(str(expression_to_display)[-1]):
        expression_to_display = str(expression_to_display)[:len(str(expression_to_display)) - 1]
        expression_to_execute = str(expression_to_execute)[:len(str(expression_to_display)) - 1]
        expression_to_calculate.set(expression_to_display)


def execute_button_equal():
    global expression_to_display
    global expression_to_execute

    try:
        expression_to_display = eval(expression_to_execute)
    except Exception as e:
        expression_to_display = e

    expression_to_calculate.set(expression_to_display)


if __name__ == '__main__':
    calculator = Tk()

    calculator.configure(background='gray71')

    calculator.title('Scientific calculator')

    calculator.geometry('544x796')

    expression_to_calculate = StringVar()

    expression_field = Entry(calculator, textvariable=expression_to_calculate, font="Calibri 20")

    expression_field.grid(columnspan=4, ipadx=130, ipady=30)

    button_absolute_value = Button(calculator, text=' |x| ', fg='black', bg='gray77',
                                   command=lambda: execute_button_operator('|x|', 'abs'), height=4, width=14,
                                   font=font_tuple)

    button_absolute_value.grid(row=2, column=0)

    button_PI = Button(calculator, text=pi_symbol, fg='black', bg='gray77',
                       command=lambda: concat_key(pi_symbol), height=4, width=14, font=font_tuple)

    button_PI.grid(row=2, column=1)

    button_modulo = Button(calculator, text=' mod(x) ', fg='black', bg='gray77',
                           command=lambda: execute_button_operator('mod', '%'),
                           height=4, width=14, font=font_tuple)

    button_modulo.grid(row=4, column=1)

    button_open_paren = Button(calculator, text=' ( ', fg='black', bg='gray77',
                               command=lambda: concat_key('('), height=4, width=14, font=font_tuple)

    button_open_paren.grid(row=8, column=0)

    button_close_paren = Button(calculator, text=' ) ', fg='black', bg='gray77',
                                command=lambda: concat_key(')'), height=4, width=14, font=font_tuple)

    button_close_paren.grid(row=8, column=2)

    button_divide = Button(calculator, text=' / ', fg='black', bg='gray77', command=lambda: concat_key('/'), height=4,
                           width=14, font=font_tuple)

    button_divide.grid(row=4, column=3)

    button_reverse = Button(calculator, text=' 1/x ', fg='black', bg='gray77',
                            command=lambda: execute_button_operator('1/', '**-1'),
                            height=4, width=14, font=font_tuple)

    button_reverse.grid(row=3, column=3)

    button_7 = Button(calculator, text=' 7 ', fg='black', bg='gray83', command=lambda: concat_key('7'), height=4,
                      width=14, font=font_tuple)

    button_7.grid(row=5, column=0)

    button_8 = Button(calculator, text=' 8 ', fg='black', bg='gray83', command=lambda: concat_key('8'), height=4,
                      width=14, font=font_tuple)

    button_8.grid(row=5, column=1)

    button_9 = Button(calculator, text=' 9 ', fg='black', bg='gray83', command=lambda: concat_key('9'), height=4,
                      width=14, font=font_tuple)

    button_9.grid(row=5, column=2)

    button_multiply = Button(calculator, text=' * ', fg='black', bg='gray77', command=lambda: concat_key('*'), height=4,
                             width=14, font=font_tuple)

    button_multiply.grid(row=5, column=3)

    button_sqrt = Button(calculator, text=' sqrt(x) ', fg='black', bg='gray77',
                         command=lambda: execute_button_operator('sqrt', 'sqrt'), height=4, width=14,
                         font=font_tuple)

    button_sqrt.grid(row=4, column=0)

    button_4 = Button(calculator, text=' 4 ', fg='black', bg='gray83', command=lambda: concat_key('4'), height=4,
                      width=14, font=font_tuple)

    button_4.grid(row=6, column=0)

    button_5 = Button(calculator, text=' 5 ', fg='black', bg='gray83', command=lambda: concat_key('5'), height=4,
                      width=14, font=font_tuple)

    button_5.grid(row=6, column=1)

    button_6 = Button(calculator, text=' 6 ', fg='black', bg='gray83', command=lambda: concat_key('6'), height=4,
                      width=14, font=font_tuple)

    button_6.grid(row=6, column=2)

    button_subtract = Button(calculator, text=' - ', fg='black', bg='gray77', command=lambda: concat_key('-'), height=4,
                             width=14, font=font_tuple)

    button_subtract.grid(row=6, column=3)

    button_expo = Button(calculator, text=' x^y ', fg='black', bg='gray77',
                         command=lambda: execute_button_operator('^', '**'),
                         height=4, width=14, font=font_tuple)

    button_expo.grid(row=3, column=1)

    button_1 = Button(calculator, text=' 1 ', fg='black', bg='gray83', command=lambda: concat_key('1'), height=4,
                      width=14, font=font_tuple)

    button_1.grid(row=7, column=0)

    button_2 = Button(calculator, text=' 2 ', fg='black', bg='gray83', command=lambda: concat_key('2'), height=4,
                      width=14, font=font_tuple)

    button_2.grid(row=7, column=1)

    button_3 = Button(calculator, text=' 3 ', fg='black', bg='gray83', command=lambda: concat_key('3'), height=4,
                      width=14, font=font_tuple)

    button_3.grid(row=7, column=2)

    button_addition = Button(calculator, text=' + ', fg='black', bg='gray77', command=lambda: concat_key('+'), height=4,
                             width=14, font=font_tuple)

    button_addition.grid(row=7, column=3)

    button_log = Button(calculator, text=' log(x) ', fg='black', bg='gray77',
                        command=lambda: execute_button_operator('log', 'log10'),
                        height=4, width=14, font=font_tuple)

    button_log.grid(row=3, column=2)

    button_decimal = Button(calculator, text='.', fg='black', bg='gray77', command=lambda: concat_key('.'), height=4,
                            width=14, font=font_tuple)

    button_decimal.grid(row=4, column=2)

    button_0 = Button(calculator, text=' 0 ', fg='black', bg='gray83', command=lambda: concat_key('0'), height=4,
                      width=14, font=font_tuple)

    button_0.grid(row=8, column=1)

    button_clear = Button(calculator, text='C', fg='black', bg='gray77', command=lambda: execute_button_clear(),
                          height=4,
                          width=14, font=font_tuple)

    button_clear.grid(row=2, column=3)

    button_equal = Button(calculator, text=' = ', fg='black', bg='SkyBlue3', command=lambda: execute_button_equal(),
                          height=4,
                          width=14, font=font_tuple)

    button_equal.grid(row=8, column=3)

    button_fact = Button(calculator, text=' x! ', fg='black', bg='gray77',
                         command=lambda: execute_button_operator('!', 'factorial'),
                         height=4,
                         width=14, font=font_tuple)

    button_fact.grid(row=3, column=0)

    button_delete_char = Button(calculator, text=' ' + delete_char_symbol + ' ', fg='black', bg='gray77',
                                command=lambda: execute_button_delete_char(),
                                height=4,
                                width=14, font=font_tuple)

    button_delete_char.grid(row=2, column=2)

    calculator.mainloop()
