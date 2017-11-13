"""
Title: To-Do App V2
Author: Jason Chan
Python 3 env
"""

import tkinter as tk
import tkinter.messagebox as msg


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
        self.title("To-Do App V2")
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

        # Adds todo1 to tasks_frame
        todo1 = tk.Label(self.tasks_frame, text="--- Add Items Here ---", bg="lightgrey", fg="black", pady=10)
        # Binds the function remove_task to it being clicked (Button-1)
        todo1.bind("<Button-1>", self.remove_task)
        self.tasks.append(todo1)

        for task in self.tasks:
            # only used to pack our default task Label
            task.pack(side=tk.TOP, fill=tk.X)

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

        self.colour_schemes = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

    # Gets rid of label widget associated with the task
    def add_task(self, event=None):
        # Get task from user input from task_create
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

        # Delete user input after hit <Return>
        self.tasks_create.delete(1.0, tk.END)

    def remove_task(self, event):
        task = event.widget

        # This only executes if user presses "Yes"
        if msg.askyesno("Really Delete?", "Delete " + task.cget("text") + "?"):
            self.tasks.remove(event.widget)
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

if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()
