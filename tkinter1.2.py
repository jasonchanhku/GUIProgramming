#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:03:40 2017

@author: jasonchan
"""

#1.2 Using Classes
import tkinter as tk

"""
the use of classes are crucial in keeping track of individual widgets that
need reference to each other, not just replying on global variables as 
the app grows
"""

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #label now belongs to the root class rather than a variabe
        #self in tk.label refer's to tk's self
        #without super() we can't do tk.label in Root()
        self.label = tk.Label(self, text = "Hello World", padx = 10, pady = 10)
        
        self.label.pack()
        
#main body
if __name__ == "__main__":
    root = Root()
    root.mainloop()
    

