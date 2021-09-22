from Tkinter import Tk,Label,Button
import ttk

def cbox_do(event):
    'Used for cbox.'
    clabel.config(text=cbox.get())

a = Tk()
cbox = ttk.Combobox(a, value=('Luke','Biggs','Wedge'), takefocus=0)
cbox.bind("<<ComboboxSelected>>", cbox_do)
cbox.pack()
clabel = Label(a)
clabel.pack()
a.mainloop()