#!/usr/bin/env python

from tkinter import *

def resize(ev=None):
    label.config(font='Helvetica -%d bold' %scale.get())

top = Tk()
top.geometry('250x150')
label = Label(top, text='Hello World!', font='Helvetica -12 bold')
label.pack(fill=Y)

scale = Scale(top, from_=10, to=40, orient=HORIZONTAL, command=resize)
scale.set(12)
scale.pack(fill=X, expand=1)

#quit = Button(top, text = 'Quit', command = top.quit, bg='red', fg='white')
quit = Button(top, text = 'Quit', command = top.quit, activeforeground='white', activebackground='red')
quit.pack()
mainloop()