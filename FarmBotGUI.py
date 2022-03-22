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

        ttk.Button(mainframe, text="Move", command=self.move).grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe, text="Home All", command=self.home_all).grid(column=1, row=2, sticky=W)

        ttk.Button(mainframe, text="Home-X", command=self.x_find_home).grid(column=2, row=2, sticky=W)
        ttk.Button(mainframe, text="Home-Y", command=self.y_find_home).grid(column=3, row=2, sticky=W)
        ttk.Button(mainframe, text="Home-Z", command=self.z_find_home).grid(column=4, row=2, sticky=W)

        ttk.Button(mainframe, text="Calibrate-X", command=self.x_calibrate).grid(column=2, row=3, sticky=W)
        ttk.Button(mainframe, text="Calibrate-Y", command=self.y_calibrate).grid(column=3, row=3, sticky=W)
        ttk.Button(mainframe, text="Calibrate-Z", command=self.z_calibrate).grid(column=4, row=3, sticky=W)


        ###### Current Coordinate #######

        ttk.Label(mainframe, text="Current X: ").grid(column=1, row=5, sticky=W)
        self.current_x = StringVar()
        ttk.Label(mainframe, textvariable=self.current_x).grid(column=2, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Current Y: ").grid(column=1, row=6, sticky=W)
        self.current_y = StringVar()
        ttk.Label(mainframe, textvariable=self.current_y).grid(column=2, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Current Z: ").grid(column=1, row=7, sticky=W)
        self.current_z = StringVar()
        ttk.Label(mainframe, textvariable=self.current_z).grid(column=2, row=7, sticky=(W, E))

        ###### Encoder-Scaled #######
        ttk.Label(mainframe, text="Encoder-Scaled X: ").grid(column=3, row=5, sticky=W)
        self.x_encoder_scaled = StringVar()
        ttk.Label(mainframe, textvariable=self.x_encoder_scaled).grid(column=4, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Encoder-Scaled Y: ").grid(column=3, row=6, sticky=W)
        self.y_encoder_scaled = StringVar()
        ttk.Label(mainframe, textvariable=self.y_encoder_scaled).grid(column=4, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Encoder-Scaled Z: ").grid(column=3, row=7, sticky=W)
        self.z_encoder_scaled = StringVar()
        ttk.Label(mainframe, textvariable=self.z_encoder_scaled).grid(column=4, row=7, sticky=(W, E))

        #############

        ###### Encoder-Raw #######
        ttk.Label(mainframe, text="Encoder-Raw X: ").grid(column=5, row=5, sticky=W)
        self.x_encoder_raw = StringVar()
        ttk.Label(mainframe, textvariable=self.x_encoder_raw).grid(column=6, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Encoder-Raw Y: ").grid(column=5, row=6, sticky=W)
        self.y_encoder_raw = StringVar()
        ttk.Label(mainframe, textvariable=self.y_encoder_raw).grid(column=6, row=6, sticky=(W, E))

        ttk.Label(mainframe, text="Encoder-Raw Z: ").grid(column=5, row=7, sticky=W)
        self.z_encoder_raw = StringVar()
        ttk.Label(mainframe, textvariable=self.z_encoder_raw).grid(column=6, row=7, sticky=(W, E))

        #############


        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        x_coordinate_entry.focus()
        self.root.bind("<Return>", self.move)
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):

        self.current_x.set(self.farmbot.status.x)
        self.current_y.set(self.farmbot.status.y)
        self.current_z.set(self.farmbot.status.z)

        self.x_encoder_scaled.set(self.farmbot.status.x_encoder_scaled)
        self.y_encoder_scaled.set(self.farmbot.status.y_encoder_scaled)
        self.z_encoder_scaled.set(self.farmbot.status.z_encoder_scaled)

        self.x_encoder_raw.set(self.farmbot.status.x_encoder_raw)
        self.y_encoder_raw.set(self.farmbot.status.y_encoder_raw)
        self.z_encoder_raw.set(self.farmbot.status.z_encoder_raw)

        self.root.after(self.internal_values_update_interval, self.update_clock)

    def move(self, *args):
        try:
            x_value = float(self.x_coordinate.get())
            y_value = float(self.y_coordinate.get())
            z_value = float(self.z_coordinate.get())
            self.farmbot.move(x_value, y_value, z_value)

        except ValueError:
            pass

    def home_all(self):
        self.farmbot.move_home_all()

    def x_find_home(self):
        self.farmbot.home_x_axis()

    def y_find_home(self):
        self.farmbot.home_y_axis()

    def z_find_home(self):
        self.farmbot.home_z_axis()

    def x_calibrate(self):
        self.farmbot.calibrate_x_axis()

    def y_calibrate(self):
        self.farmbot.calibrate_y_axis()

    def z_calibrate(self):
        self.farmbot.calibrate_z_axis()

