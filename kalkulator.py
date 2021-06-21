from tkinter import *
import tkinter.messagebox
import math

app = Tk()
app.geometry("400x400+700+100")
app.wm_title("Kalkulator")

def get_position():
    if disp.get() == '0':
        disp.delete(0)
    position = len(disp.get())
    return position


def button_dot_clicked():
    position = len(disp.get())
    disp.insert(position, '.')


def button_1_clicked():
    position = get_position()
    disp.insert(position, '1')


def button_2_clicked():
    pos = get_position()
    disp.insert(pos, '2')


def button_3_clicked():
    pos = get_position()
    disp.insert(pos, '3')


def button_4_clicked():
    pos = get_position()
    disp.insert(pos, '4')


def button_5_clicked():
    pos = get_position()
    disp.insert(pos, '5')


def button_6_clicked():
    pos = get_position()
    disp.insert(pos, '6')


def button_7_clicked():
    pos = get_position()
    disp.insert(pos, '7')


def button_8_clicked():
    pos = get_position()
    disp.insert(pos, '8')


def button_9_clicked():
    pos = get_position()
    disp.insert(pos, '9')


def button_0_clicked():
    pos = get_position()
    disp.insert(pos, '0')


def key_event(*args):
    if disp.get() == '0':
        disp.delete(0, END)


def button_plus_clicked():
    pos = get_position()
    disp.insert(pos, '+')


def button_minus_clicked():
    pos = get_position()
    disp.insert(pos, '-')


def button_multiplication_clicked():
    pos = get_position()
    disp.insert(pos, '*')


def button_division_clicked():
    pos = get_position()
    disp.insert(pos, '/')

def button_left_bracket_clicked():
    pos = get_position()
    disp.insert(pos, '(')


def button_right_bracket_clicked():
    pos = get_position()
    disp.insert(pos, ')')


def button_power_clicked():
    pos = get_position()
    disp.insert(pos, '**')


def button_factorial_clicked():
    try:
        score = float(disp.get())
        score = math.factorial(score)
        disp.delete(0, END)
        disp.insert(0, str(score))
    except Exception:
        tkinter.messagebox.showerror("Value Error", "Sprawdz wartosci i operatory")


def button_sqrt_clicked():
    try:
        score = float(disp.get())
        score = math.sqrt(score)
        disp.delete(0, END)
        disp.insert(0, str(score))
    except Exception:
        tkinter.messagebox.showerror("Value Error", "Sprawdz wartosci i operatory")


def button_abs_clicked():
    try:
        score = float(disp.get())
        score = abs(score)
        disp.delete(0, END)
        disp.insert(0, str(score))
    except Exception:
        tkinter.messagebox.showerror("Value Error", "Sprawdz wartosci i operatory")


def button_mod_clicked():
    pos = get_position()
    disp.insert(pos, '%')


def button_inverse_clicked():
    try:
        score = float(disp.get())
        score = 1/score
        disp.delete(0, END)
        disp.insert(0, str(score))
    except Exception:
        tkinter.messagebox.showerror("Value Error", "Sprawdz wartosci i operatory")


def button_logarithm_clicked():
    try:
        score = float(disp.get())
        score = math.log10(score)
        disp.delete(0, END)
        disp.insert(0, str(score))
    except Exception:
        tkinter.messagebox.showerror("Value Error", "Sprawdz wartosci i operatory")


def button_equal_clicked(*args):
    try:
        score = disp.get()
        score = eval(score)
        disp.delete(0, END)
        disp.insert(0, score)
    except:
        tkinter.messagebox.showerror("Value Error", "Sprawdz wartosci i operatory")


def button_c_clicked(*args):
    disp.delete(0, END)
    disp.insert(0, '0')


def button_del_clicked():
    position = len(disp.get())
    display = str(disp.get())

    if display == '' or display == ' ':
        disp.insert(0, '0')
    elif display == '0':
        pass
    else:
        disp.delete(0, END)
        disp.insert(0, display[0:position-1])


# pole na dzialania i wynik

data = StringVar()

disp = Entry(app, font="Verdana 20", fg="black", bg="#5999b3", bd=0, justify=RIGHT, insertbackground="#5999b3", cursor="arrow")
disp.bind("<Return>", button_equal_clicked)
disp.bind("<Escape>", button_c_clicked)
disp.bind("<Key-1>", key_event)
disp.bind("<Key-2>", key_event)
disp.bind("<Key-3>", key_event)
disp.bind("<Key-4>", key_event)
disp.bind("<Key-5>", key_event)
disp.bind("<Key-6>", key_event)
disp.bind("<Key-7>", key_event)
disp.bind("<Key-8>", key_event)
disp.bind("<Key-9>", key_event)
disp.bind("<Key-0>", key_event)
disp.bind("<Key-.>", key_event)
disp.insert(0, '0')
disp.focus_set()
disp.pack(expand=TRUE, fill=BOTH)

frame_row_0 = Frame(app)
frame_row_0.pack(expand=TRUE, fill=BOTH)

mod_button = Button(frame_row_0, text="mod(x)", font="Segoe 17", relief=GROOVE, bd=0, command=button_mod_clicked, fg="white", bg="#333333")
mod_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

logarithm_button = Button(frame_row_0, text="log(x)", font="Segoe 17", relief=GROOVE, bd=0, command=button_logarithm_clicked, fg="white", bg="#333333")
logarithm_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

factorial_button = Button(frame_row_0, text=" x! ", font="Segoe 18", relief=GROOVE, bd=0, command=button_factorial_clicked, fg="white", bg="#333333")
factorial_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

sqrt_button = Button(frame_row_0, text=" √x ", font="Segoe 18", relief=GROOVE, bd=0, command=button_sqrt_clicked, fg="white", bg="#333333")
sqrt_button.pack(side=LEFT, expand=TRUE, fill=BOTH)


frame_row_1 = Frame(app)
frame_row_1.pack(expand=TRUE, fill=BOTH)

inverse_button = Button(frame_row_1, text=" 1/x ", font="Segoe 18", relief=GROOVE, bd=0, command=button_inverse_clicked, fg="white", bg="#333333")
inverse_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_7 = Button(frame_row_1, text="7", font="Segoe 23", relief=GROOVE, bd=0, command=button_7_clicked, fg="white", bg="#333333") # TUUU
button_7.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_8 = Button(frame_row_1, text="8", font="Segoe 23", relief=GROOVE, bd=0,  command=button_8_clicked, fg="white", bg="#333333")
button_8.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_9 = Button(frame_row_1, text="9", font="Segoe 23", relief=GROOVE, bd=0, command=button_9_clicked, fg="white", bg="#333333")
button_9.pack(side=LEFT, expand=TRUE, fill=BOTH)

multiplication_button = Button(frame_row_1, text="*", font="Segoe 23", relief=GROOVE, bd=0, command=button_multiplication_clicked, fg="white", bg="#333333")
multiplication_button.pack(side=LEFT, expand=TRUE, fill=BOTH)


frame_row_2 = Frame(app)
frame_row_2.pack(expand=TRUE, fill=BOTH)

sqrt_button = Button(frame_row_2, text=" |x| ", font="Segoe 18", relief=GROOVE, bd=0, command=button_abs_clicked, fg="white", bg="#333333")
sqrt_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_4 = Button(frame_row_2, text="4", font="Segoe 23", relief=GROOVE, bd=0, command=button_4_clicked, fg="white", bg="#333333")
button_4.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_5 = Button(frame_row_2, text="5", font="Segoe 23", relief=GROOVE, bd=0, command=button_5_clicked, fg="white", bg="#333333")
button_5.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_6 = Button(frame_row_2, text="6", font="Segoe 23", relief=GROOVE, bd=0, command=button_6_clicked, fg="white", bg="#333333")
button_6.pack(side=LEFT, expand=TRUE, fill=BOTH)

subtraction_button = Button(frame_row_2, text="-", font="Segoe 23", relief=GROOVE, bd=0, command=button_minus_clicked, fg="white", bg="#333333")
subtraction_button.pack(side=LEFT, expand=TRUE, fill=BOTH)


frame_row_3 = Frame(app)
frame_row_3.pack(expand=TRUE, fill=BOTH)

pow_button = Button(frame_row_3, text="x^y", font="Segoe 20", relief=GROOVE, bd=0, command=button_power_clicked, fg="white", bg="#333333")
pow_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_1 = Button(frame_row_3, text="1", font="Segoe 23", relief=GROOVE, bd=0, command=button_1_clicked, fg="white", bg="#333333")
button_1.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_2 = Button(frame_row_3, text="2", font="Segoe 23", relief=GROOVE, bd=0, command=button_2_clicked, fg="white", bg="#333333")
button_2.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_3 = Button(frame_row_3, text="3", font="Segoe 23", relief=GROOVE, bd=0, command=button_3_clicked, fg="white", bg="#333333")
button_3.pack(side=LEFT, expand=TRUE, fill=BOTH)

sum_button = Button(frame_row_3, text="+", font="Segoe 23", relief=GROOVE, bd=0, command=button_plus_clicked, fg="white", bg="#333333")
sum_button.pack(side=LEFT, expand=TRUE, fill=BOTH)


frame_row_4 = Frame(app)
frame_row_4.pack(expand=TRUE, fill=BOTH)

left_bracket_button = Button(frame_row_4, text=" ( ", font="Segoe 21", relief=GROOVE, bd=0, command=button_left_bracket_clicked, fg="white", bg="#333333")
left_bracket_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

right_bracket_button = Button(frame_row_4, text=" ) ", font="Segoe 21", relief=GROOVE, bd=0, command=button_right_bracket_clicked, fg="white", bg="#333333")
right_bracket_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

c_button = Button(frame_row_4, text="C", font="Segoe 23", relief=GROOVE, bd=0, command=button_c_clicked, fg="white", bg="#333333")
c_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

del_button = Button(frame_row_4, text="DEL", font="Segoe 20", relief=GROOVE, bd=0, command=button_del_clicked, fg="white", bg="#333333")
del_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

button_0 = Button(frame_row_4, text="0", font="Segoe 23", relief=GROOVE, bd=0, command=button_0_clicked, fg="white", bg="#333333")
button_0.pack(side=LEFT, expand=TRUE, fill=BOTH)

dot_button = Button(frame_row_4, text=" • ", font="Segoe 21", relief=GROOVE, bd=0, command=button_dot_clicked, fg="white", bg="#333333")
dot_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

equals_button = Button(frame_row_4, text="=", font="Segoe 23", relief=GROOVE, bd=0, command=button_equal_clicked, fg="white", bg="#333333")
equals_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

division_button = Button(frame_row_4, text="/", font="Segoe 23", relief=GROOVE, bd=0, command=button_division_clicked, fg="white", bg="#333333")
division_button.pack(side=LEFT, expand=TRUE, fill=BOTH)

app.mainloop()