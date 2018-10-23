import tkinter
top = tkinter.Tk()
inputs = {}
values = {}

def callback(sv):
    val = sv.get()[:1]
    sv.set(val)
    values[sv.ipt.index] = val
    if len(values) < len(inputs):
        inputs[len(values)].focus()
    else:
        top.quit()

for i in range(6):
    sv = tkinter.StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    entry =tkinter.Entry(top, width=1, bd=1, textvariable=sv)
    inputs[i].grid(row=1, column=i)

    sv.ipt = inputs[i]
    sv.ipt.index = i

class StrVar(object):
    def __init__(self, var=None, entry=None, index=None):
        self.var = var
        self.entry = entry
        self.index = index



top.lift()
top.attributes("-topmost", True)
top.mainloop()
''.join([values[i] for i in range(len(values))])
