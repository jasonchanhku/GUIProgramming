"""
Title: To-Do App V3 with sqlite storage system
Author: Jason Chan
Python 3 env
"""

import tkinter as tk
import tkinter.messagebox as msg
import os
import sqlite3


class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        # Concepts of frames and canvases
        """
        Canvases - lets us enjoy graphical capabilities such as scrolling
        Frame - layout component to group together multiple widgets
        
        Use canvas to draw frame into the window to bundle the todo lists  
        """
        # Create one canvas and two frames
        self.tasks_canvas = tk.Canvas(self)

        # This frame is parented to the canvas
        self.tasks_frame = tk.Frame(self.tasks_canvas)

        # This frame is parented to the window
        self.text_frame = tk.Frame(self)

        # Creates a scrollbar within the canvas, we want a vertical scrollbar scrolling in the y direction
        self.scrollbar = tk.Scrollbar(self.tasks_canvas, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Specify title and geometry of GUI
        self.title("To-Do App V3")
        self.geometry("300x400")

        # Creating our text widget parented to the text frame
        self.tasks_create = tk.Text(self.text_frame, height=3, bg="white", fg="black")

        # Pack canvas to the top and fill up and expand as much as possible
        self.tasks_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Pack scrollbar on right, filling up vertical space
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Use canvas to create new window in itself that holds our tasks frame anchoring it to the north
        # we DO NOT PACK OUR TASKS FRAME AS IT WILL NOT APPEAR
        self.canvas_frame = self.tasks_canvas.create_window((0,0), window=self.tasks_frame, anchor="n")

        # Remember that task create is in text frame, pack task create and pack its frame as well
        self.tasks_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # Ensure cursor already in text box
        self.tasks_create.focus_set()

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

        # We not get existing tasks from load_tasks() , fetch from database, iterate through them and pass them through
        # slightly altered add_task method
        current_tasks = self.load_tasks()
        for tasks in current_tasks:
            task_text = tasks[0]
            self.add_task(None, task_text, True)


        # MouseWheel, Button 4 and Button 5 handles scrolling
        # Configure keeps the canvas as large as possible when window size changes
        # Configure is fired when window changes size, provides new width and height
        # Remember to not put parenthesis when passing function, instead of calling it
        self.bind("<Return>", self.add_task)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.tasks_canvas.bind("<Configure>", self.task_width)

    # Gets rid of label widget associated with the task
    def add_task(self, event=None, task_text=None, from_db=False):
        # Get task from user input from task_create
        if not task_text:
            task_text = self.tasks_create.get(1.0, tk.END).strip()

        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.set_task_colour(len(self.tasks), new_task)

            new_task.bind("<Button-1>", self.remove_task)
            # this is the one responsible for packing incoming tasks
            new_task.pack(side=tk.TOP, fill=tk.X)

            # The only reason we append this to new task is so that we keep track of how many items we have so far
            # Must be useful for determining the alternating color schemes
            self.tasks.append(new_task)

        if not from_db:
            self.save_task(task_text)
        # Delete user input after hit <Return>
        self.tasks_create.delete(1.0, tk.END)

    def remove_task(self, event):
        task = event.widget

        # This only executes if user presses "Yes"
        if msg.askyesno("Really Delete?", "Delete " + task.cget("text") + "?"):
            self.tasks.remove(event.widget)

            delete_task_query = "DELETE FROM tasks WHERE task=?"
            delete_task_data = (task.cget("text"),)
            self.runQuery(delete_task_query, delete_task_data)

            event.widget.destroy()
            self.recolour_tasks()

    def recolour_tasks(self):
        for index, task in enumerate(self.tasks):
            self.set_task_colour(index, task)

    def set_task_colour(self, position, task):
        _, task_style_choice = divmod(position, 2)

        my_scheme_choice = self.colour_schemes[task_style_choice]
        task.configure(bg=my_scheme_choice["bg"])
        task.configure(fg=my_scheme_choice["fg"])

    # Method bounded to our main Root <Configure> and will be called whenever window resize
    # bbox all specifies we want entire canvas to be scrollable
    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))

    # Method ensures Labels stay at full width even after resize of window
    def task_width(self, event):
        canvas_width = event.width
        self.tasks_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            # Adjusts view of the tasks canvas
            self.tasks_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
        self.tasks_canvas.yview_scroll(move, "units")

    def save_task(self, task):
        insert_task_query = "INSERT INTO tasks VALUES (?)"
        insert_task_data = (task,)
        self.runQuery(insert_task_query, insert_task_data)

    def load_tasks(self):
        load_tasks_query = "SELECT task FROM tasks"
        my_tasks = self.runQuery(load_tasks_query, receive=True)

        return my_tasks

    # Database handling method
    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect("tasks.db")
        # cursor used to execute queries in database and return data
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive:
            return cursor.fetchall()
        else:
            conn.commit()
        conn.close()

    # Used to create the database file "tasks.db" if it doesn't exist
    @staticmethod
    def firstTimeDb():
        create_tables = "CREATE TABLE tasks (task TEXT)"
        Todo.runQuery(create_tables)

        default_task_query = "INSERT INTO tasks VALUES (?)"
        default_task_data = ("- - - Add Items Here - - -",)
        Todo.runQuery(default_task_query, default_task_data)


if __name__ == "__main__":
    if not os.path.isfile("tasks.db"):
        Todo.firstTimeDb()
    todo = Todo()
    todo.mainloop()
