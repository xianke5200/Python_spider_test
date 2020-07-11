#!/usr/bin/env python

from functools import partial as pto
from tkinter import Tk, Button, X
from tkinter.messagebox import showinfo, showwarning, showerror

WARN = 'Warn'
CRIT = 'Crit'
REGU = 'Regu'

SIGNS = {
    'do not enter': CRIT,
    'railroad crossing': WARN,
    '55\nspeed limit': REGU,
    'wrong way': CRIT,
    'merging traffic': WARN,
    'one way': REGU,
}

critCB = lambda : showerror('Error', 'Error Button Pressed')
warnCB = lambda : showwarning('Warning', 'Warning Button Pressed')
infoCB = lambda : showinfo('Info', 'Info Button Pressed')

top = Tk()
top.title('Road  Signs')
Button(top, text='Quit', command=top.quit, bg='red', fg='white').pack()

myButton = pto(Button, top)
CritButton = pto(myButton, command=critCB, bg='white', fg='red')
WarnButton = pto(myButton, command=warnCB, bg='green')
ReguButton = pto(myButton, command=infoCB, bg='white')

for eachSign in SIGNS:
    signType = SIGNS[eachSign]
    #print(signType, signType.title())
    cmd = '%sButton(text=%r%s).pack(fill=X, expand=True)' %(
        signType.title(), eachSign,
        '.upper()' if signType == CRIT else '.title()'
    )
    eval(cmd)
top.mainloop()
