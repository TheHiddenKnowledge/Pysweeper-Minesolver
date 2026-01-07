## @file minesolver.py
# @brief Implements a solver for pysweepers using on the game GUI.

import random as rnd
import time as t

## @class MineSolver
# @brief Contains methods and attributes used for solving pysweepers.
class MineSolver:
    def __init__(self, game):
        ## @brief Pysweepers instance
        # @hideinitializer
        self.__game = game
        ## @brief Maximum solver iterations
        # @hideinitializer
        self.__max_iter = 100

    ## @brief Reveals a random coordinate in rectangle determined by the
    # bounding coordinates.
    # @param x0 Bottom left x coordinate
    # @param y0 Bottom left y coordinate
    # @param x1 Top right x coordinate
    # @param y1 Top right y coordinate
    def __pick_random(self, x0, y0, x1, y1):
        x = rnd.randint(x0, x1)
        y = rnd.randint(y0, y1)
        while 0 > x >= self.__game.width or 0 > y >= self.__game.height:
            x = rnd.randint(x0, x1)
            y = rnd.randint(y0, y1)
        self.__game.gui_map[y][x].update()
        self.__game.gui_map[y][x].event_generate("<Button-1>")

    ## @brief Flags the mines determined by qualifying edge coordinates.
    def __flag_edges(self):
        flag_count = 0
        for x in range(self.__game.width):
            for y in range(self.__game.height):
                gui_cell = self.__game.gui_map[y][x]
                if gui_cell["text"] != " " and gui_cell["text"] != "⚑":
                    # Coordinates that are hidden
                    hidden_cells = []
                    # Coordinates that are flagged 
                    flagged_cells = []
                    rots = [[0, 1], [0, -1], [1, 0], [-1, 0],
                            [1, 1], [-1, -1], [1, -1], [-1, 1]]
                    for rot in rots:
                        x_dir = x + rot[0]
                        y_dir = y + rot[1]
                        adjacent_cell = self.__game.gui_map[y_dir][x_dir]
                        if (0 <= x_dir < self.__game.width
                            and 0 <= y_dir < self.__game.height):
                            if adjacent_cell["bg"] == "grey":
                                # Marks hidden and flagged coordinates
                                if adjacent_cell["text"] != "⚑":
                                    hidden_cells.append(
                                        adjacent_cell)
                                else:
                                    flagged_cells.append(
                                        adjacent_cell)
                    # Flags hidden coordinates only if the hidden coordinate
                    # count matches the number on the map
                    if len(hidden_cells) + len(flagged_cells) == int(
                            gui_cell["text"]):
                        if len(flagged_cells) != int(gui_cell["text"]):
                            for hidden_cell in hidden_cells:
                                if hidden_cell["text"] != "⚑":
                                    hidden_cell.update()
                                    hidden_cell.event_generate("<Button-3>")
                                    flag_count += 1
        # Does not keep flagging edges if no more edges qualify
        if flag_count > 0:
            return True
        else:
            return False

    ## @brief Clears hidden blocks within 3x3 square centered at [x, y].
    # @param x Cell x coordinate
    # @param y Cell y coordinate
    def __clear_square(self, x, y):
        reveal_count = 0
        rots = [[0, 1], [0, -1], [1, 0], [-1, 0],
                [1, 1], [-1, -1], [1, -1], [-1, 1]]
        for rot in rots:
            x_dir = x + rot[0]
            y_dir = y + rot[1]
            if (0 <= x_dir < self.__game.width and
                    0 <= y_dir < self.__game.height):
                adjacent_cell = self.__game.gui_map[y_dir][x_dir]
                # Only clears hidden and non-flagged coordinates
                if (adjacent_cell["bg"] == "grey"
                        and adjacent_cell["text"] != "⚑"):
                    adjacent_cell.update()
                    adjacent_cell.event_generate("<Button-1>")
                    reveal_count += 1
        if reveal_count > 0:
            return True
        else:
            return False

    ## @brief Checks if coordinate map number at [x, y]
    # is equal to number of surrounding flags.
    # @param x Cell x coordinate
    # @param y Cell y coordinate
    def __check_square(self, x, y):
        flag_count = 0
        gui_cell = self.__game.gui_map[y][x]
        rots = [[0, 1], [0, -1], [1, 0], [-1, 0],
                [1, 1], [-1, -1], [1, -1], [-1, 1]]
        for rot in rots:
            x_dir = x + rot[0]
            y_dir = y + rot[1]
            adjacent_cell = self.__game.gui_map[y_dir][x_dir]
            if (0 <= x_dir < self.__game.width
                    and 0 <= y_dir < self.__game.height):
                # Adds surrounding flags to flag count
                if adjacent_cell["text"] == "⚑":
                    flag_count += 1
        if flag_count == int(gui_cell["text"]):
            return True
        else:
            return False

    ## @brief Eliminates qualifying edge coordinates.
    def __eliminate_edge(self):
        elim_count = 0
        for x in range(self.__game.width):
            for y in range(self.__game.height):
                gui_cell = self.__game.gui_map[y][x]
                # Checks revealed coordinates with numbers
                if gui_cell["text"] != " " and gui_cell["text"] != "⚑":
                    # Clear 3x3 square if the coordinate qualifies
                    if self.__check_square(x, y):
                        if self.__clear_square(x, y):
                            elim_count += 1
        # Does not keep eliminating edges if no more edges qualify
        if elim_count > 0:
            return True
        else:
            return False

    ## @brief Predicts edge coordinate to eliminate.
    def __predict_edge(self):
        # Keeps track of most probable edge coordinate
        min_numbers = 9
        min_cells = []
        for x in range(self.__game.width):
            for y in range(self.__game.height):
                gui_cell = self.__game.gui_map[y][x]
                # Checks only hidden and non-flagged coordinates
                if gui_cell["bg"] == "grey" and gui_cell["text"] != "⚑":
                    numbers_count = 0
                    rots = [[0, 1], [0, -1], [1, 0], [-1, 0],
                            [1, 1], [-1, -1], [1, -1], [-1, 1]]
                    for rot in rots:
                        x_dir = x + rot[0]
                        y_dir = y + rot[1]
                        adjacent_cell = self.__game.gui_map[y_dir][x_dir]
                        if (0 <= x_dir < self.__game.width
                                and 0 <= y_dir < self.__game.height):
                            # If the surrounding coordinate has a number add to count
                            if (adjacent_cell["text"] != " "
                                    and adjacent_cell["text"] != "⚑"):
                                numbers_count += 1
                    if numbers_count != 0 and numbers_count < min_numbers:
                        min_numbers = numbers_count
                        min_cells = [x, y]
        # Reveal most probable coordinate (can be wrong)
        if len(min_cells) != 0:
            min_x = min_cells[0]
            min_y = min_cells[1]
            self.__game.gui_map[min_y][min_x].update()
            self.__game.gui_map[min_y][min_x].event_generate("<Button-1>")

    ## @brief Runs the solver algorithm.
    def run_solver(self):
        # CPU time capped by maximum iteration count 
        for a in range(self.__max_iter):
            # Just for visualization
            t.sleep(.1)
            if self.__game.game_over:
                break
            reveal_count = (self.__game.width * self.__game.height -
                              self.__game.hidden)
            reveal_threshold = int(self.__game.width * self.__game.height / 10)
            # Pick rnd coordinates until at least 10% of the map is revealed 
            if reveal_count < reveal_threshold:
                self.__pick_random(
                    0, 0, self.__game.width - 1, self.__game.height - 1)
            else:
                # Flags the edges, if not then eliminates the edges,
                # if not then makes a prediction
                if not self.__flag_edges():
                    if not self.__eliminate_edge():
                        self.__predict_edge()
