from sympy import *
from tkinter import *
from tkinter import scrolledtext as st
# import math


class EQ_Solver():
    def __init__(self):
        root = Tk()
        root.geometry('500x500')
        root.title('EQ Solver')

        self.body(root)
        root.mainloop()

    def body(self, root):
        calc = Frame(root, width=500, height=500)
        calc.pack()
        n = 4
        x = ["X+", "Y+", "Z+", "W=", ""]
        t1 = 0
        t2 = 0
        inputs = []

        def focus_next(event):
            if event.widget.tk_focusNext().get("1.0", END)[:1] == "0":
                event.widget.tk_focusNext().delete("1.0", END)
            event.widget.tk_focusNext().focus()
            return ("break")

        def focus_previous(event):
            if event.widget.tk_focusPrev().get("1.0", END)[:1] == "0":
                event.widget.tk_focusPrev().delete("1.0", END)
            event.widget.tk_focusPrev().focus()
            return ("break")
        for i in range(n):
            input1 = []
            for j in range(n + 1):
                t = Text(calc, width=8, height=2)
                t.grid(row=i, column=t2)
                t.insert(END, "0")
                t.bind("<Tab>", focus_next)
                t.bind("<Shift-Tab>", focus_previous)
                input1.append(t)
                l = Label(calc, text=x[t1])
                l.grid(row=i, column=t2 + 1)
                t1 += 1
                t2 += 2
            inputs.append(input1)
            t1 = 0
            t2 = 0
        inputs[0][0].delete("1.0", END)
        inputs[0][0].focus()
        b = Button(calc, text="solve", command=lambda: self.solve(inputs))
        b.grid(row=n + 1, column=n // 2, pady=20,
               sticky="ew", columnspan=n + 1)
        self.res = st.ScrolledText(calc, width=40, height=10)
        self.res.grid(row=n + 2, column=1, columnspan=7)

        Button(calc, text="Clear", command=lambda: self.res.delete(
            "1.0", END)).grid(row=n + 3, column=2, pady=20, columnspan=5)
        Button(calc, text="Reset", command=lambda: self.reset(inputs)).grid(
            row=n + 4, column=2, pady=20, columnspan=5)

    def reset(self, inputs):
        for input1 in inputs:
            for i in input1:
                i.delete("1.0", END)
                i.insert(END, "0")

    def solve(self, inputs):

        cnts = []
        for input1 in inputs:
            cnt = []
            for i in input1:
                t = i.get("1.0", END)
                # print(t,end=" ")
                if t != "0":
                    try:
                        cnt.append(simplify(t))
                    except:
                        cnt.append(simplify(0))

            if len(cnt):
                cnts.append(cnt)
        print(cnts)
        n = len(cnts)

        xs = symbols("x y z w")
        eqs = []
        for i in range(len(cnts)):
            eq = ""
            for j in range(len(cnts[i])):
                # eq+=f"{cnts[i][j]}*{xs[j]}"
                if j in range(0, n):
                    eq += f"{cnts[i][j]}*{xs[j]}"
                    if j != n - 1:
                        eq += "+"
            eqs.append(Eq(sympify(eq), cnts[i][j]))
        res = ""
        tt = ""
        s = solve(tuple(eqs), tuple(xs))
        res += f"{s}\n"
        print(res)
        self.res.insert(END, res)
        for i in xs:
            try:
                tt += f"{i}:{eval(f'{s[i]}')}\n"
            except:
                pass
        tt += "\n"
        for i in eqs:
            t = f"{i}"
            if t == "True":
                continue
            tt += t + "\n"

        self.res.insert(END, tt)
        self.res.yview_moveto(1.0)


EQ_Solver()
