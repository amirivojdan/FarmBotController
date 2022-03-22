from tkinter import *
from tkinter import ttk

from FarmBot import FarmBot


class FarmBotGUI:
    def __init__(self, farmbot: FarmBot):

        self.farmbot = farmbot
        self.internal_values_update_interval = 10

        self.root = Tk()
        self.root.title("FarmBot Controller")

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.x_coordinate = StringVar()
        x_coordinate_entry = ttk.Entry(mainframe, width=7, textvariable=self.x_coordinate)
        x_coordinate_entry.grid(column=2, row=1, sticky=(W, E))

        self.y_coordinate = StringVar()
        y_coordinate_entry = ttk.Entry(mainframe, width=7, textvariable=self.y_coordinate)
        y_coordinate_entry.grid(column=3, row=1, sticky=(W, E))

        self.z_coordinate = StringVar()
        z_coordinate_entry = ttk.Entry(mainframe, width=7, textvariable=self.z_coordinate)
        z_coordinate_entry.grid(column=4, row=1, sticky=(W, E))

        ttk.Button(mainframe, text="Move", command=self.move).grid(column=3, row=6, sticky=W)

        ttk.Label(mainframe, text="Current X: ").grid(column=1, row=2, sticky=W)
        self.current_x = StringVar()
        ttk.Label(mainframe, textvariable=self.current_x).grid(column=2, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="Current Y: ").grid(column=1, row=3, sticky=W)
        self.current_y = StringVar()
        ttk.Label(mainframe, textvariable=self.current_y).grid(column=2, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="Current Z: ").grid(column=1, row=4, sticky=W)
        self.current_z = StringVar()
        ttk.Label(mainframe, textvariable=self.current_z).grid(column=2, row=4, sticky=(W, E))

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        x_coordinate_entry.focus()
        self.root.bind("<Return>", self.move)
        self.update_clock()
        self.root.mainloop()

    def move(self, *args):
        try:
            x_value = float(self.x_coordinate.get())
            y_value = float(self.y_coordinate.get())
            z_value = float(self.z_coordinate.get())
            self.farmbot.move(x_value, y_value, z_value)

        except ValueError:
            pass

    def update_clock(self):
        self.current_x.set(self.farmbot.status.x)
        self.current_y.set(self.farmbot.status.y)
        self.current_z.set(self.farmbot.status.z)
        self.root.after(self.internal_values_update_interval, self.update_clock)
