# bez drzewa/slownika
import math
from tkinter import *

root = Tk()
root.title("Kalkulator")
# this removes the maximize button
root.resizable(0,0)

# buttons settings
x_of_button = 12
y_of_button = 10

expression_to_show = ''
expression_to_calculate = ''
current_number = ''

label_expresion = Label(root, text=expression_to_show)
label_current_number = Label(root, text=current_number)

# wstawia tabulatory w miejsce label_current_number
def cleanCurrentNumberSpace():
    label_clean = Label(root, text="\t" * (len(current_number)//7 + 1))
    label_clean.grid(row=1, column=0, columnspan=4, sticky='E')

def concatenateWithExpression(character_to_show, character_to_calculate):
    global expression_to_show
    global expression_to_calculate
    global current_number

    # po obliczeniu wyrazenia i dalszego korzystania z kalkulatora czysci 'historie wpisywania'
    if expression_to_calculate == '':
        # wstawia tabulatory w miejsce label_expression
        label_clean = Label(root, text="\t" * (len(expression_to_show)//7 + 1))
        label_clean.grid(row=0, column=0, columnspan=4, sticky='E')
        expression_to_show = ''
        #print('czyszczenie')

    expression_to_show += character_to_show
    expression_to_calculate += character_to_calculate
    cleanCurrentNumberSpace()
    current_number = ''
    
    global label_expresion
    label_expresion = Label(root, text=expression_to_show)
    label_expresion.grid(row=0, column=0, columnspan=4, sticky='E')
    #print(expression_to_calculate)
    
def buildNumber(character):
    global current_number
    current_number += character
    
    global label_current_number
    label_current_number = Label(root, text=current_number)
    label_current_number.grid(row=1, column=0, columnspan=4, sticky='E')

def pushedButtonEqual():
    global expression_to_show
    global expression_to_calculate
    global current_number
    global label_current_number
    concatenateWithExpression(current_number +' =', current_number)
    try:
        current_number = str(eval(expression_to_calculate))
    except:
        current_number = 'error'

    label_current_number = Label(root, text=current_number)
    label_current_number.grid(row=1, column=0, columnspan=4, sticky='E')

    expression_to_calculate = ''

def pushedButtonClear():
    global current_number
    cleanCurrentNumberSpace()
    current_number = ''

# create buttons
button_0 = Button(root, text="0", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('0'))
button_1 = Button(root, text="1", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('1'))
button_2 = Button(root, text="2", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('2'))
button_3 = Button(root, text="3", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('3'))
button_4 = Button(root, text="4", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('4'))
button_5 = Button(root, text="5", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('5'))
button_6 = Button(root, text="6", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('6'))
button_7 = Button(root, text="7", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('7'))
button_8 = Button(root, text="8", width=x_of_button, pady=y_of_button, bg="#FFFFFF", command=lambda: buildNumber('8'))
button_9 = Button(root, text="9", width=x_of_button, pady=y_of_button, bg="white", command=lambda: buildNumber('9'))

button_dot = Button             (root, text=".", width=x_of_button, pady=y_of_button, bg='white', command=lambda: buildNumber('.'))
button_plus = Button            (root, text="+", width=x_of_button, pady=y_of_button, bg='#C0C0C0', command=lambda: concatenateWithExpression(current_number + ' + ', current_number + ' + '))
button_minus = Button           (root, text="-", width=x_of_button, pady=y_of_button, bg='#C0C0C0', command=lambda: concatenateWithExpression(current_number + ' - ', current_number + ' - '))
button_multiply = Button        (root, text="×", width=x_of_button, pady=y_of_button, bg='#C0C0C0', command=lambda: concatenateWithExpression(current_number + ' × ', current_number + ' * '))
button_divide = Button          (root, text="÷", width=x_of_button, pady=y_of_button, bg='#C0C0C0', command=lambda: concatenateWithExpression(current_number + ' ÷ ', current_number + ' / '))
button_left_bracket = Button    (root, text="(", width=x_of_button//2, pady=y_of_button, bg='#C0C0C0', command=lambda: concatenateWithExpression(current_number + ' ( ', current_number + ' ( '))
button_right_bracket = Button   (root, text=")", width=x_of_button//2, pady=y_of_button, bg='#C0C0C0', command=lambda: concatenateWithExpression(current_number + ' ) ', current_number + ' ) '))
button_equal = Button           (root, text="=", width=x_of_button, pady=y_of_button, bg="#75B4D2", command=pushedButtonEqual)
button_clear = Button           (root, text="CLEAR", width=x_of_button*4 + 4, pady=y_of_button, bg="#75B4D2", command=pushedButtonClear)

button_power = Button           (root, text="x^y", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression(current_number + ' ^ ', current_number + '**'))
button_factorial = Button       (root, text="n!", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression(current_number + '! ', 'math.factorial(' + current_number+ ')'))
button_sqrt = Button            (root, text="sqrt(x)", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression('sqrt('+ current_number + ') ', 'math.sqrt(' + current_number + ')'))
button_abs = Button             (root, text="|x|", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression('|' + current_number + '| ', 'abs(' + current_number + ')'))
button_modulo = Button          (root, text="mod(x)", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression(current_number + 'mod', current_number + '%'))
button_inverse = Button         (root, text="1/x", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression('1/' + current_number + " ", current_number + '**-1'))
button_log = Button             (root, text="log(x)", width=x_of_button, pady=y_of_button, bg='#A8DFD0', command=lambda: concatenateWithExpression('log(' + current_number + ") ", 'math.log10(' + current_number + ')'))

# show buttons
which_row = 0

label_expresion.grid        (row=which_row, column=3, columnspan=1, sticky='E')
which_row += 1

label_current_number.grid   (row=which_row, column=3, columnspan=1, sticky='E')
which_row += 1

button_clear.grid           (row=which_row, column=0, columnspan=4)
which_row += 1

button_abs.grid             (row=which_row, column=0)
button_modulo.grid          (row=which_row, column=1)
button_inverse.grid         (row=which_row, column=2)
button_log.grid             (row=which_row, column=3)
which_row += 1

button_power.grid           (row=which_row, column=0)
button_factorial.grid       (row=which_row, column=1)
button_sqrt.grid            (row=which_row, column=2)
button_divide.grid          (row=which_row, column=3)
which_row += 1

button_7.grid               (row=which_row, column=0)
button_8.grid               (row=which_row, column=1)
button_9.grid               (row=which_row, column=2)
button_multiply.grid        (row=which_row, column=3)
which_row += 1

button_4.grid               (row=which_row, column=0)
button_5.grid               (row=which_row, column=1)
button_6.grid               (row=which_row, column=2)
button_minus.grid           (row=which_row, column=3)
which_row += 1

button_1.grid               (row=which_row, column=0)
button_2.grid               (row=which_row, column=1)
button_3.grid               (row=which_row, column=2)
button_plus.grid            (row=which_row, column=3)
which_row += 1

button_left_bracket.grid    (row=which_row, column=0, sticky='W')
button_right_bracket.grid   (row=which_row, column=0, sticky='E')
button_0.grid               (row=which_row, column=1)
button_dot.grid             (row=which_row, column=2)
button_equal.grid           (row=which_row, column=3)

root.mainloop()