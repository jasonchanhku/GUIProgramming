# -*- coding: utf-8 -*-
"""
Tkinter Day 1
"""

import tkinter as tk

#creates the overall window for tkinter using the Tk() method from tkinter class
root = tk.Tk()

#tk.label() is a Tk widget which holds the text hello world. First argument
# is parent in which it will be placed. In this case, root, the current window 
label = tk.Label(root, text = "Hello World", padx = 10, pady = 10)

#this places the label into the root
label.pack()

#responsible for showing the window
label.mainloop()



