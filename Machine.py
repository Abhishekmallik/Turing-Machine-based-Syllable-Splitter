import time
import sys
from tkinter import *
import tkinter as tk
from TuringMachine import TuringMachine
from TMTape import TMTape
from TMStatus import TMStatus

#input Alphabets
input_alphabet = {
    'c': [' ', 'B', 'b', 'C', 'c', 'D', 'd', 'F', 'f', 'G', 'g', 'H', 'h', 'J', 'j', 'K', 'k',
          'L', 'l', 'M', 'm', 'N', 'n', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'V',
          'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'],
    'v': ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u'],
    '#': ['#']
}

# tape alphabet
tape_alphabet = {
    'c': [' ', 'B', 'b', 'C', 'c', 'D', 'd', 'F', 'f', 'G', 'g', 'H', 'h', 'J', 'j', 'K', 'k',
          'L', 'l', 'M', 'm', 'N', 'n', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'V',
          'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z'],
    'v': ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u'],
    '#': ['#'],
    '-': ['-']
}

# set of states
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'}

# initial state
initial_state = 'q0'
accept_state = 'q7'
reject_state = 'q8'

# Transitions
transitions = {
    'q0': {
        'c': ('q2', 'c', 'R'),
        'v': ('q1', 'v', 'R'),
        '#': (reject_state, '', 'R')	#reject
    },
    'q1': {
        'c': ('q3', 'c', 'R'),
        'v': (reject_state, '', 'R'),	#reject
        '#': (accept_state, '', 'R')	#accept

    },
    'q2': {
        'c': ('q2', 'c', 'R'),
        'v': ('q1', 'v', 'R'),
        '#': (accept_state, '', 'R')	#accept
    },
    'q3': {
        'c': ('q4', 'c', 'R'),
        'v': ('q6', 'v', 'L'),
        '#': (accept_state, '', 'R')	#accept
    },
    'q4': {
        'c': ('q5', 'c', 'R'),
        'v': ('q6', 'v', 'L'),
        '#': (accept_state, '', 'R')	#accept
    },
    'q5': {
        'c': ('q2', 'c', 'R'),
        'v': ('q6', 'v', 'L'),
        '#': (accept_state, '', 'R')	#accept
    },
    'q6': {
        'c': ('q6', tape_alphabet['-'][0] + 'c', 'R'),
        'v': ('q1', 'v', 'R'),
        '#': (accept_state, '', 'R')	#accept
    }
}

blank = '#'
animation = Tk()
animation.title('Syllable Splitter')
turing_input = StringVar()

current_input_tr = ''

def create_ovalq1(canvas, text, x_0, y_0, x_1, y_1, color="SeaGreen3", width=0.0, ocolor="SeaGreen"):
    canvas.create_oval(x_0, y_0, x_1, y_1, fill=color, width=width, outline=ocolor)
    canvas.create_text(x_0 + 20, y_0 + 20, text=text)

def main_graph(canvas, current_state, control):
    x0 = 300 - 150
    y0 = 300 - 80
    x1 = 300 + 100
    y1 = 300 + 30
    x2 = 300 + 100
    y2 = 300 - 200
    x3 = 300 + 250
    y3 = 300 + 120
    x4 = 300 + 450
    y4 = 300 + 150
    x5 = 300 + 550
    y5 = 300 - 150
    x6 = 300 + 350
    y6 = 300 - 50
    x7 = 300 + 800
    y7 = 300
    x8 = 300 - 50
    y8 = 300 + 180
    xc = 50
    yc = 10
    xv = 50
    yv = 50
    xh = 50
    yh = 90

    # Ovals
    # reject
    if current_state == 'reject':
        create_ovalq1(canvas, 'reject', x8, y8, x8 + 40, y8 + 40,
                      color="SkyBlue1", width=10, ocolor="gold")
        canvas.create_rectangle(x8 + 70, y8, x8 + 40 + 150, y8 + 40, fill='red',
                                width=5, outline='gold')
        canvas.create_text(x8 + 70 + 50, y8 + 20, text='REJECTED!')
    else:
        create_ovalq1(canvas, 'reject', x8, y8, x8 + 40, y8 + 40,
                      color="SkyBlue1")
    # accept
    if current_state == 'accept':
        create_ovalq1(canvas, 'accept', x7, y7, x7 + 40, y7 + 40, color='SkyBlue1', width=10, ocolor="gold")
        canvas.create_rectangle(x7 + 70, y7, x7 + 100 + 40 + 90, y7 + 40, fill='SeaGreen3',
                                width=5, outline='gold')
        canvas.create_text(x7 + 120 + 20, y7 + 20, text='ACCEPTED!')
    else:
        create_ovalq1(canvas, 'accept', x7, y7, x7 + 40, y7 + 40, color='SkyBlue1')

    # q0
    if current_state == 'q0':
        create_ovalq1(canvas, 'q0', x0, y0, x0 + 40, y0 + 40, color='SkyBlue1', width=10, ocolor="gold")
    else:
        create_ovalq1(canvas, 'q0', x0, y0, x0 + 40, y0 + 40, color='SkyBlue1')

    # q1
    if current_state == 'q1':
        create_ovalq1(canvas, 'q1', x1, y1, x1 + 40, y1 + 40, color="SkyBlue1", width=10, ocolor="gold")
    else:
        create_ovalq1(canvas, 'q1', x1, y1, x1 + 40, y1 + 40, color="SkyBlue1")

    # q2
    if current_state == 'q2':
        create_ovalq1(canvas, 'q2', x2, y2, x2 + 40, y2 + 40, color="SkyBlue1", width=10, ocolor="gold")
    else:
        create_ovalq1(canvas, 'q2', x2, y2, x2 + 40, y2 + 40, color="SkyBlue1")
    
    # q3
    if current_state == 'q3':
        create_ovalq1(canvas, 'q3', x3, y3, x3 + 40, y3 + 40, color="SkyBlue1", width=10,
                      ocolor="gold")
    else:
        create_ovalq1(canvas, 'q3', x3, y3, x3 + 40, y3 + 40, color="SkyBlue1")

    # q4
    if current_state == 'q4':
        create_ovalq1(canvas, 'q4', x4, y4, x4 + 40, y4 + 40, color="SkyBlue1", width=10,
                      ocolor="gold")
    else:
        create_ovalq1(canvas, 'q4', x4, y4, x4 + 40, y4 + 40, color="SkyBlue1")

    # q5
    if current_state == 'q5':
        create_ovalq1(canvas, 'q5', x5, y5, x5 + 40, y5 + 40, color="SkyBlue1", width=10,
                      ocolor="gold")
    else:
        create_ovalq1(canvas, 'q5', x5, y5, x5 + 40, y5 + 40, color="SkyBlue1")

    #q6
    if current_state == 'q6':
        create_ovalq1(canvas, 'q6', x6, y6, x6 + 40, y6 + 40, color="SkyBlue1", width=10,
                      ocolor="gold")
    else:
        create_ovalq1(canvas, 'q6', x6, y6, x6 + 40, y6 + 40, color="SkyBlue1")

    # Arrows
    # q2 -> q2
    canvas.create_line(x2, y2 + 20, x2 - 40, y2 - 10, arrow=tk.LAST, fill="purple")
    canvas.create_line(x2 - 40, y2 - 10, x2 + 20, y2, arrow=tk.LAST, fill="purple")
    # q6 -> q6
    canvas.create_line(x6, y6 + 20, x6 - 40, y6 - 10, arrow=tk.LAST, fill="purple")
    canvas.create_line(x6 - 40, y6 - 10, x6 + 20, y6, arrow=tk.LAST, fill="purple")
    # q0 -> q2
    canvas.create_line(x0 + 40, y0 + 20, x2, y2 + 20, arrow=tk.LAST, fill="purple")
    # q0 -> q1
    canvas.create_line(x0 + 40, y0 + 20, x1, y1 + 20, arrow=tk.LAST, fill="Red")
    # q2 -> q1
    canvas.create_line(x2 + 20, y2 + 40, x1 + 20, y1, arrow=tk.LAST, fill="Red")
    # q0 -> q8
    canvas.create_line(x0 + 40, y0 + 20, x8 + 20, y8, arrow=tk.LAST, fill="SeaGreen3")
    # q5 -> q2
    canvas.create_line(x5, y5 + 20, x2 + 40, y2 + 20, arrow=tk.LAST, fill="purple")
    # q6 -> q1
    canvas.create_line(x6, y6 + 20, x1 + 40, y1 + 20, arrow=tk.LAST, fill="Red")
    # q1 -> q8
    canvas.create_line(x1 + 20, y1 + 40, x8 + 20, y8, arrow=tk.LAST, fill="Red")
    # q1 -> q3
    canvas.create_line(x1 + 20, y1 + 40, x3, y3 + 20, arrow=tk.LAST, fill="purple")
    # q3 -> q6
    canvas.create_line(x3 + 40, y3 + 20, x6 + 20, y6 + 40, arrow=tk.LAST, fill="Red")
    # q3 -> q4
    canvas.create_line(x3 + 40, y3 + 20, x4, y4 + 20, arrow=tk.LAST, fill="purple")
    # q4 -> q6
    canvas.create_line(x4 + 20, y4, x6 + 20, y6 + 40, arrow=tk.LAST, fill="Red")
    # q4 -> q5
    canvas.create_line(x4 + 20, y4, x5 + 20, y5 + 40, arrow=tk.LAST, fill="purple")
    # q5 -> q6
    canvas.create_line(x5, y5 + 20, x6 + 40, y6 + 20, arrow=tk.LAST, fill="Red")
    # q1 -> q7
    canvas.create_line(x1 + 40, y1 + 20, x7, y7 + 20, arrow=tk.LAST, fill="SeaGreen3")
    # q2 -> q7
    canvas.create_line(x2 + 40, y2 + 20, x7, y7 + 20, arrow=tk.LAST, fill="SeaGreen3")
    # q3 -> q7
    canvas.create_line(x3 + 40, y3 + 20, x7, y7 + 20, arrow=tk.LAST, fill="SeaGreen3")
    # q4 -> q7
    canvas.create_line(x4 + 40, y4 + 20, x7, y7 + 20, arrow=tk.LAST, fill="SeaGreen3")
    # q5 -> q7
    canvas.create_line(x5 + 40, y5 + 20, x7, y7 + 20, arrow=tk.LAST, fill="SeaGreen3")
    # q6 -> q7
    canvas.create_line(x6 + 40, y6 + 20, x7, y7 + 20, arrow=tk.LAST, fill="SeaGreen3")

    # Legends
    # Legend for consonants
    create_ovalq1(canvas, 'c', xc, yc, xc + 40, yc + 40, color="SkyBlue1")
    canvas.create_line(xc + 40, yc + 20, xc + 40 + 50, yc + 20, arrow=tk.LAST, fill="purple")
    # Legend for Vowels
    create_ovalq1(canvas, 'v', xv, yv, xv + 40, yv + 40, color="SkyBlue1")
    canvas.create_line(xv + 40, yv + 20, xv + 40 + 50, yv + 20, arrow=tk.LAST, fill="Red")
    # Legen for #
    create_ovalq1(canvas, '#', xh, yh, xh + 40, yh + 40, color="SkyBlue1")
    canvas.create_line(xh + 40, yh + 20, xh + 40 + 50, yh + 20, arrow=tk.LAST, fill="SeaGreen3")
    
def create_rects(animation, pointed_index, input='                      '):
    canvas = Canvas(animation, width=2000, height=300, bg='lightblue')

    # input = input.upper()

    lngt = 50
    width_count = 0
    change = 0
    current_x = 0
    current_y = 0
    startpoint = 30
    if (len(input) < 21):
        startpoint = (2000 - (len(input) * lngt)) / 2

    point_state = 0
    for i in range(len(input)):

        current_x = i * lngt + startpoint
        if (i > 36 and i < 74):
            current_x -= 37 * 50
            current_y = 125
            point_state = 37 * 50
            canvas.create_rectangle(current_x, current_y, current_x + lngt, current_y + lngt, fill="SkyBlue3", width=3)
            canvas.create_text(current_x + 20, current_y + 10, text=input[i])

        if (i > 73 and i < 101):
            current_x -= 74 * 50
            current_y = 225
            point_state = 74 * 50
            canvas.create_rectangle(current_x, current_y, current_x + lngt, current_y + lngt, fill="SkyBlue3", width=3)
            canvas.create_text(current_x + 20, current_y + 10, text=input[i])
        if (i < 37):
            current_y = 25
            point_state = 0
            canvas.create_rectangle(current_x, current_y, current_x + lngt, current_y + lngt, fill="SkyBlue3", width=3)
            canvas.create_text(current_x + 20, 20 + current_y, text=input[i])
            # [150,75,225,0,300,75]
            # [spoint, sheigth, mid_width, mid_start, lastpoinX, laspointY]

        # points = [0,30,22,0,44,30]
        triangle_x = (pointed_index * 50 + startpoint) - point_state
        if i == pointed_index:
            points = [triangle_x, 30 + current_y + 50, triangle_x + 22, current_y + 50 + 0, triangle_x + 44,
                      current_y + 30 + 50]
            canvas.create_polygon(points, outline='yellow',
                                  fill='DodgerBlue2', width=3)
        canvas.pack()
    return canvas


def gui_execute(animation, input):
    spelling_turing_machine = TuringMachine(states, input_alphabet, tape_alphabet, blank, transitions, initial_state,
                                            accept_state, reject_state)

    output_tape, result, steps = spelling_turing_machine.execute(input)

    print("The word {} is {}, the final tape: {}".format(input, result, output_tape))
    print("The machine steps: ", steps)

    change_input = input
    tape = TMTape(input, blank=blank)
    index_update = 0

    # Set the current status with start state and tape
    cur_status = TMStatus(initial_state, transitions)
    status = True
    control_str=[]
    for i in range(len(steps)):
        key = steps[i][0]
        value = steps[i][1]
        if (i == 0):

            canvas = Canvas(animation, width=2000, height=530, bg='white')
            canvas.pack()
            main_graph(canvas, key, control_str)

            table = create_rects(animation, value, change_input)

            animation.update()
            time.sleep(1)
        else:
            status, control = cur_status.update(tape)
            control_str.append(control[0])

            main_graph(canvas, key, control_str)
            animation.update()
            time.sleep(1)

        if i != len(steps) - 1 and i != 0:
            canvas.destroy()
            table.destroy()
            canvas = Canvas(animation, width=2000, height=530, bg='white')

            # time.sleep(1)
            canvas.pack()


            change_input = tape.get_tape()

            table = create_rects(animation, value, change_input[:len(change_input) - 1])

            animation.update()


def tr_input():
    if canvas.winfo_exists() == 1 and table.winfo_exists() == 1:
        canvas.destroy()
        table.destroy()
    elif canvas.winfo_exists() == 1:
        canvas.destroy()
    if turing_input.get() != current_input_tr:
        list = animation.pack_slaves()
        for l in list:
            l.destroy()
        animation.update()
        inputt = Canvas(animation, width=2000, height=100, bg='LightBlue3')

        mLabel = Label(inputt, text="Enter a word").pack()  # this is placed in 0 0

        # 'Entry' is used to display the input-field
        mEntry = Entry(inputt, textvariable=turing_input).pack()  # this is placed in 0 1
        mButton = Button(inputt, text="Turing Machine", command=tr_input, fg="tan2").pack()

        inputt.pack()
        animation.update()
    gui_execute(animation, turing_input.get())

    return


def reset(canvas, table):
    canvas.destroy()
    table.destroy()
    animation.update()

    canvas = Canvas(animation, width=2000, height=530, bg='white')
    canvas.pack()
    listt = []
    main_graph(canvas, ' ', listt)
    canvas.pack()

    table = create_rects(animation, -1, '          ')
    animation.update()
    return


inputt = Canvas(animation, width=2000, height=100, bg='LightBlue3')

mLabel = Label(inputt, text="Enter a word").pack()  # this is placed in 0 0

# 'Entry' is used to display the input-field
mEntry = Entry(inputt, textvariable=turing_input).pack()  # this is placed in 0 1
mButton = Button(inputt, text="Turing Machine", command=tr_input, fg="tan2").pack()

inputt.pack()
animation.update()

canvas = Canvas(animation, width=2000, height=530, bg='white')
canvas.pack()
listt=[]
main_graph(canvas, ' ', listt)
canvas.pack()

table = create_rects(animation, -1, '          ')
animation.update()

animation.mainloop()