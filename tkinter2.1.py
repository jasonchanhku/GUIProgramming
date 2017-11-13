#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:26:39 2017

@author: jasonchan
"""

# chapter 2-1: To-do list

import tkinter as tk


class ToDo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        # when using mutable type of object, convert it to list within init
        # creates an empty list if no tasks else accepts value from variable tasks
        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        # specify title and layout resolution, ensuring its vertical (long)

        self.title = "To-Do App V1"
        self.geometry = "300x500"

        todo1 = tk.Label(self, text="---Add Your Items Here---", bg="lightgrey", fg="black", pady=10)

        # a default "task" is added to prevent it from being a big blank space at the bottom
        # we do this by creating a label, adding it to our tasks list and packaging it

        self.tasks.append(todo1)

        # use a loop to package tasks, this will be clear later

        for task in self.tasks:
            # this means widget is packed to the top and fill in the X direction (horizontally)
            task.pack(side=tk.TOP, fill=tk.X)

        # create a text box at the bottom for the user to input sentences
        self.task_create = tk.Text(self, height=3, bg="white", fg="black")

        # pack this widget at the bottom and fills it horizontally (X-Axis)
        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)

        # so that user don't have to click in the box to type
        self.task_create.focus_set()

        # binds the return key to activate a function. Did not input () as want to pass function, not calling it
        self.bind("<Return>", self.add_task)

        # add color schemes to alternate colors between new tasks using a list of dictionaries
        self.color_schemes = [{"bg": "white", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    def add_task(self, event=None):
        # get the task text user input from __init__:, using get() function, from first char(1.0) to END
        # strip() is to strip new line when user presses <Return>
        task_text = self.task_create.get(1.0, tk.END).strip()

        if len(task_text) > 0:
            # add a label widget with the text input from the user after hitting enter
            new_task = tk.Label(self, text=task_text, pady=10)

            # alternating color
            # _ represents variable we don't intend to use in Python
            # task_style_choice can only be 0 or 1
            _, task_style_choice = divmod(len(self.tasks), 2)

            my_scheme_choice = self.color_schemes[task_style_choice]

            # configure is used to set property of the widget
            new_task.configure(bg=my_scheme_choice["bg"])
            new_task.configure(fg=my_scheme_choice["fg"])

            new_task.pack(side=tk.TOP, fill=tk.X)
            self.tasks.append(new_task)

        # delete the textbox after user typed inside
        self.task_create.delete(1.0, tk.END)


if __name__ == "__main__":
    root = ToDo()
    root.mainloop()
