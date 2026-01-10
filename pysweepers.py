## @mainpage
# This project aims to create a simple minesweepers game using Tkinter,
# as well as a solver for the game.
# @par Latest Release:
# V1.1 - 1/3/2026
# @par Created by: I. Finney
# @par Revision History:
# @version 1.0 Initial Release.
# @version 1.1 Revised code Base.

## @file pysweepers.py
# @brief Implements a fully functional version of minesweepers using tkinter.

import tkinter as tk
import random as rnd
from tkinter import ttk


## @class PySweepers
# @brief Contains methods and attributes used for running pysweepers.
class PySweepers:
    ## @param width Map width
    # @param height Map height
    # @param mines Mine count
    def __init__(self, width, height, mines):
        ## @brief Map width
        # @hideinitializer
        self.width = width
        ## @brief Map height
        # @hideinitializer
        self.height = height
        ## @brief Mine count
        # @hideinitializer
        self.__mines = mines
        ## @brief Total hidden cells
        # @hideinitializer
        self.hidden = width * height
        ## @brief Array containing full game map
        # @hideinitializer
        self.__map = [[]]
        ## @brief Array of cell GUI elements
        # @hideinitializer
        self.gui_map = [[]]
        ## @brief Game status
        # @hideinitializer
        self.game_status = "running"
        # Initializing GUI
        master = tk.Tk(className="Py Sweepers")
        ttk.Style().theme_use("winnative")
        ## @brief Frame used to contain the cells
        # @hideinitializer
        self.__map_frame = tk.Frame(master)
        self.__map_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        ## @brief Status label GUI element
        # @hideinitializer
        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=1, column=0, sticky="ew")
        self.status_label.configure(text="")
        resize_button = tk.Button(master, command=lambda:
        self.__create_resize_popup(), text="Resize")
        resize_button.grid(row=1, column=1, sticky="ew")
        reset_button = tk.Button(master, command=lambda:
        self.reset_map(), text="Reset")
        reset_button.grid(row=1, column=2, sticky="ew")
        self.reset_map()

    ## @brief Creates a popup window to resize the game map.
    def __create_resize_popup(self):
        popup = tk.Toplevel()
        popup.title("Resize")
        int_check = popup.register(lambda text : text == "" or text.isdigit())
        width_label = tk.Label(popup, text="Width", width=20)
        width_label.grid(row=0, column=0, sticky="ew")
        width_entry = tk.Entry(popup, width=20, validate="all",
                               validatecommand=(int_check, "%P"))
        width_entry.grid(row=0, column=1, sticky="ew")
        height_label = tk.Label(popup, text="Height", width=20)
        height_label.grid(row=1, column=0, sticky="ew")
        height_entry = tk.Entry(popup, width=20, validate="all",
                               validatecommand=(int_check, "%P"))
        height_entry.grid(row=1, column=1, sticky="ew")
        mines_label = tk.Label(popup, text="Mines", width=20)
        mines_label.grid(row=2, column=0, sticky="ew")
        mines_entry = tk.Entry(popup, width=20, validate="all",
                               validatecommand=(int_check, "%P"))
        mines_entry.grid(row=2, column=1, sticky="ew")
        resize_button = tk.Button(popup, text="Resize Map", command=lambda:
        self.resize_map(width_entry.get(),
                        height_entry.get(),
                        mines_entry.get()))
        resize_button.grid(row=3, column=0, columnspan=2, sticky="ew")

    ## @brief Resizes the map.
    # @param width Map width
    # @param height Map height
    # @param mines Mine count
    def resize_map(self, width, height, mines):
        # Handling string instances of the arguments
        if isinstance(width, str):
            width = 0 if width == "" else int(width)
        if isinstance(height, str):
            height = 0 if height == "" else int(height)
        if isinstance(mines, str):
            mines = 0 if mines == "" else int(mines)
        # Only resizes map if the width, height, and mine count are within
        # the allowable ranges
        if (5 <= width <= 20 and 5 <= height <= 20
                and mines < width * height):
            self.width = width
            self.height = height
            self.__mines = mines
            self.reset_map()

    ## @brief Generates the mines on the map data structure.
    def __generate_mines(self):
        mine_counter = 0
        mine_cells = []
        # Generate mine random coordinates
        while mine_counter != self.__mines:
            mine_cell = [rnd.randint(0, self.width - 1),
                         rnd.randint(0, self.height - 1)]
            if mine_cell not in mine_cells:
                mine_cells.append(mine_cell)
                mine_counter += 1
        # Adding mines to map
        for mine_cell in mine_cells:
            self.__map[mine_cell[1]][mine_cell[0]] = "*"

    ## @brief Generates the numbers on the map data structure.
    def __generate_numbers(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.__map[y][x] != "*":
                    mine_count = 0
                    # Rotation array for NWES and diagonal combinations
                    rots = [[0, 1], [0, -1], [1, 0], [-1, 0],
                            [1, 1], [-1, -1], [1, -1], [-1, 1]]
                    for rot in rots:
                        x_dir = x + rot[0]
                        y_dir = y + rot[1]
                        if 0 <= x_dir < self.width:
                            if 0 <= y_dir < self.height:
                                # For each rotation add to count if mine
                                if self.__map[y_dir][x_dir] == "*":
                                    mine_count += 1
                    # Add mine count to coordinate on map
                    if mine_count > 0:
                        self.__map[y][x] = str(mine_count)

    ## @brief Generates the GUI map and map data structure.
    # @param is_resized Boolean variable for determining if the map is resized
    def __generate_map(self, is_resized):
        # Initializing map GUI elements and map data structure
        if is_resized:
            # Resetting map data structure
            self.__map = []
            # Resetting map GUI elements
            for gui_map_row in self.gui_map:
                for gui_cell in gui_map_row:
                    gui_cell.destroy()
            self.gui_map = []
            for y in range(self.height):
                map_row = []
                gui_map_row = []
                for x in range(self.width):
                    gui_cell = tk.Label(self.__map_frame, text=" ", bg="grey",
                                        borderwidth=2, relief="groove",
                                        height=2, width=5)
                    ## @cond
                    gui_cell.bind("<Button-1>", self.__check_grid)
                    gui_cell.bind("<Button-3>", self.__flag_grid)
                    ## @endcond
                    gui_cell.grid(row=y, column=x)
                    map_row.append(" ")
                    gui_map_row.append(gui_cell)
                self.__map.append(map_row)
                self.gui_map.append(gui_map_row)
        else:
            for y in range(self.height):
                for x in range(self.width):
                    self.__map[y][x] = " "
                    gui_cell = self.gui_map[y][x]
                    gui_cell.configure(text=" ", bg="grey")
        # Generating map elements from empty map
        self.__generate_mines()
        self.__generate_numbers()

    ## @brief Resets the map.
    def reset_map(self):
        # Generating new map
        is_resized = (len(self.__map) != self.height
                      or len(self.__map[0]) != self.width)
        self.__generate_map(is_resized)
        # Resetting game variables
        self.hidden = self.width * self.height
        self.game_status = "running"
        self.status_label.configure(text="")

    ## @brief Fill method for numberless coordinates.
    # @param x Cell x coordinate
    # @param y Cell y coordinate
    # @param fill_list List of cells to fill
    def __fill_blanks(self, x, y, fill_list):
        if [x, y] not in fill_list:
            fill_list.append([x, y])
            rots = [[0, 1], [0, -1], [1, 0], [-1, 0],
                    [1, 1], [-1, -1], [1, -1], [-1, 1]]
            for rot in rots:
                x_dir = x + rot[0]
                y_dir = y + rot[1]
                if 0 <= x_dir < self.width:
                    if 0 <= y_dir < self.height:
                        # If rotated coordinate has a number, add to fill list
                        if (self.__map[y_dir][x_dir] != "*"
                                and self.__map[y_dir][x_dir] != " "):
                            if [x_dir, y_dir] not in fill_list:
                                if self.gui_map[y_dir][x_dir]["bg"] == "grey":
                                    fill_list.append([x_dir, y_dir])
                        # If rotated coordinate has no number,
                        # perform method on coordinate
                        elif self.__map[y_dir][x_dir] == " ":
                            self.__fill_blanks(x_dir, y_dir, fill_list)

    ## @brief Checks selected coordinate on left click.
    # @param event Tkinter event variable
    def __check_grid(self, event):
        if self.game_status == "running":
            gui_cell = event.widget
            x = gui_cell.grid_info()["column"]
            y = gui_cell.grid_info()["row"]
            # Only reveal hidden or non-flagged coordinates
            if gui_cell["bg"] != "white" and gui_cell["text"] != "⚑":
                # If coordinate has a number, reveal coordinate
                if self.__map[y][x] != "*" and self.__map[y][x] != " ":
                    gui_cell.configure(text=self.__map[y][x], bg="white")
                    self.hidden -= 1
                # If coordinate has no number, fill area
                elif self.__map[y][x] == " ":
                    fill_list = []
                    self.__fill_blanks(x, y, fill_list)
                    for fill_cord in fill_list:
                        x_dir = fill_cord[0]
                        y_dir = fill_cord[1]
                        self.gui_map[y_dir][x_dir].configure(
                            text=self.__map[y_dir][x_dir], bg="white")
                        self.hidden -= 1
                # If coordinate is a mine, reveal mine and end game
                elif self.__map[y][x] == "*":
                    gui_cell.configure(text=self.__map[y][x], bg="red")
                    self.game_status = "lost"
                    self.status_label.configure(text="You lost!")
            # If all hidden coordinates are revealed, end game
            if self.hidden == self.__mines:
                self.game_status = "won"
                self.status_label.configure(text="You won!")

    ## @brief Flags selected coordinate on right click.
    # @param event Tkinter event variable
    def __flag_grid(self, event):
        if self.game_status == "running":
            gui_cell = event.widget
            # Toggle logic for flagging a coordinate
            if gui_cell["bg"] == "grey":
                if gui_cell["text"] != "⚑":
                    gui_cell.configure(text="⚑")
                else:
                    gui_cell.configure(text=" ")

    ## @brief Runs the game instance (must be present at bottom of code)
    def run_game(self):
        tk.mainloop()