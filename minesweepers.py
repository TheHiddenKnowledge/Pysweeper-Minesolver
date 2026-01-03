from tkinter import *
import random
import time

# Map with MINES and numbers
FULL_MAP = []
# Map of GUI_MAP revealed and HIDDEN
GUI_MAP = []
WIDTH = 8
HEIGHT = 8
MINES = 10
HIDDEN = WIDTH * HEIGHT
GAME_OVER = False
MAX_ITER = 100


# Generates the mines on the map
def GenMines(Width, Height, Mines):
    mine_counter = 0
    mine_cords = []
    # Generate Mines random coordinates
    while mine_counter != Mines:
        mine_cord = [random.randint(0, Width - 1), random.randint(0, Height - 1)]
        if mine_cord not in mine_cords:
            mine_cords.append(mine_cord)
            mine_counter += 1
    # Adding Mines mines to map
    for mine_cord in mine_cords:
        x = mine_cord[0]
        y = mine_cord[1]
        FULL_MAP[y][x] = "*"


# Generates the numbers on the map
def GenNums(Width, Height):
    for x in range(Width):
        for y in range(Height):
            if FULL_MAP[y][x] != "*":
                mine_count = 0
                # Rotation array for NWES and diagonal combinations
                rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
                for rot in rots:
                    x_ = x + rot[0]
                    y_ = y + rot[1]
                    if 0 <= x_ < Width:
                        if 0 <= y_ < Height:
                            # For each rotation add to count if mine
                            if FULL_MAP[y_][x_] == "*":
                                mine_count += 1
                # Add mine count to coordinate on map
                if mine_count > 0:
                    FULL_MAP[y][x] = str(mine_count)


# Generates the map as a whole
def GenMap(Width, Height, Mines):
    MAP_FRAME.grid(row=0, column=0, columnspan=3, sticky="ew")
    # Initializing map GUI elements and map data structure
    for y in range(Height):
        full_row = []
        gui_row = []
        for x in range(Width):
            gui_cord = Label(MAP_FRAME, text=" ", bg="grey", borderwidth=2, relief="groove", height=2, width=5)
            gui_cord.bind("<Button-1>", GridCheck)
            gui_cord.bind("<Button-3>", GridFlag)
            gui_cord.grid(row=y, column=x)
            full_row.append(" ")
            gui_row.append(gui_cord)
        FULL_MAP.append(full_row)
        GUI_MAP.append(gui_row)
    # Necessary GUI initialization
    STATUS.grid(row=1, column=0, sticky="ew")
    STATUS.configure(text="")
    SOLVER.grid(row=1, column=1, sticky="ew")
    RESET.grid(row=1, column=2, sticky="ew")
    # Generating map elements from empty map
    GenMines(Width, Height, Mines)
    GenNums(Width, Height)


# Resets the map
def ResetMap(Width, Height, Mines):
    global FULL_MAP
    global GUI_MAP
    global HIDDEN
    global GAME_OVER
    # Deleting map GUI elements and map data structure
    FULL_MAP = []
    for gui_row in GUI_MAP:
        for gui_cord in gui_row:
            gui_cord.destroy()
    GUI_MAP = []
    # Resetting game STATUS
    HIDDEN = Width * Height
    GAME_OVER = False
    # Generating new map
    GenMap(Width, Height, Mines)


# Fill method for numberless coordinates
def GetFill(X, Y, Width, Height, Fill_List):
    if [X, Y] not in Fill_List:
        Fill_List.append([X, Y])
        rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        for rot in rots:
            x_ = X + rot[0]
            y_ = Y + rot[1]
            if 0 <= x_ < Width:
                if 0 <= y_ < Height:
                    # If rotated coordinate has a number, add to fill list
                    if FULL_MAP[y_][x_] != "*" and FULL_MAP[y_][x_] != " ":
                        if [x_, y_] not in Fill_List:
                            if GUI_MAP[y_][x_]["bg"] == "grey":
                                Fill_List.append([x_, y_])
                    # If rotated coordinate has no number, perform method on coordinate
                    elif FULL_MAP[y_][x_] == " ":
                        GetFill(x_, y_, Width, Height, Fill_List)


# Checks selected coordinate on left click
def GridCheck(EVENT):
    global GAME_OVER
    global HIDDEN
    if not GAME_OVER:
        gui_cord = EVENT.widget
        x = gui_cord.grid_info()["column"]
        y = gui_cord.grid_info()["row"]
        # Only reveal HIDDEN or non-flagged coordinates
        if gui_cord["bg"] != "white" and gui_cord["text"] != "⚑":
            # If coordinate has a number, reveal coordinate
            if FULL_MAP[y][x] != "*" and FULL_MAP[y][x] != " ":
                gui_cord.configure(text=FULL_MAP[y][x], bg="white")
                HIDDEN -= 1
            # If coordinate has no number, fill area
            elif FULL_MAP[y][x] == " ":
                fill_list = []
                GetFill(x, y, WIDTH, HEIGHT, fill_list)
                for fill_cord in fill_list:
                    x_ = fill_cord[0]
                    y_ = fill_cord[1]
                    GUI_MAP[y_][x_].configure(text=FULL_MAP[y_][x_], bg="white")
                    HIDDEN -= 1
            # If coordinate is a mine, reveal mine and end game
            elif FULL_MAP[y][x] == "*":
                gui_cord.configure(text=FULL_MAP[y][x], bg="red")
                GAME_OVER = True
                STATUS.configure(text="You lost!")
        # If all HIDDEN coordinates are revealed, end game
        if HIDDEN == MINES:
            GAME_OVER = True
            STATUS.configure(text="You won!")


# Flags selected coordinate on right click
def GridFlag(EVENT):
    if not GAME_OVER:
        gui_cord = EVENT.widget
        # Toggle logic for flagging a coordinate
        if gui_cord["bg"] == "grey":
            if gui_cord["text"] != "⚑":
                gui_cord.configure(text="⚑")
            else:
                gui_cord.configure(text=" ")


# Reveals random coordinate in rectangle determined by bounding coordinates
def PickRand(X0, Y0, X1, Y1, Width, Height):
    x = random.randint(X0, X1)
    y = random.randint(Y0, Y1)
    while 0 > x >= Width or 0 > y >= Height:
        x = random.randint(X0, X1)
        y = random.randint(Y0, Y1)
    GUI_MAP[y][x].update()
    GUI_MAP[y][x].event_generate("<Button-1>")


# Flags the mines determined by qualifying edge coordinates
def FlagEdges(Width, Height):
    flag_count = 0
    for x in range(Width):
        for y in range(Height):
            gui_cord = GUI_MAP[y][x]
            if gui_cord["text"] != " " and gui_cord["text"] != "⚑":
                # Coordinates that are hidden
                hidden_cords = []
                # Coordinates that are flagged 
                flagged_cords = []
                rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
                for rot in rots:
                    x_ = x + rot[0]
                    y_ = y + rot[1]
                    if 0 <= x_ < Width:
                        if 0 <= y_ < Height:
                            if GUI_MAP[y_][x_]["bg"] == "grey":
                                # Marks hidden and flagged coordinates 
                                if GUI_MAP[y_][x_]["text"] != "⚑":
                                    hidden_cords.append(GUI_MAP[y_][x_])
                                else:
                                    flagged_cords.append(GUI_MAP[y_][x_])
                # Flags hidden coordinates only if the hidden coordinate count matches the number on the map 
                if len(hidden_cords) + len(flagged_cords) == int(gui_cord["text"]):
                    if len(flagged_cords) != int(gui_cord["text"]):
                        for hidden_cord in hidden_cords:
                            if hidden_cord["text"] != "⚑":
                                hidden_cord.update()
                                hidden_cord.event_generate("<Button-3>")
                        flag_count += 1
    # Does not keep flagging edges if no more edges qualify 
    if flag_count > 0:
        return True
    else:
        return False


# Clears hidden blocks within 3x3 square centered at [X, Y]
def ClearSquare(X, Y, Width, Height):
    reveal_count = 0
    rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
    for rot in rots:
        x_ = X + rot[0]
        y_ = Y + rot[1]
        if 0 <= x_ < Width:
            if 0 <= y_ < Height:
                gui_cord = GUI_MAP[y_][x_]
                # Only clears hidden and non-flagged coordinates 
                if gui_cord["bg"] == "grey" and gui_cord["text"] != "⚑":
                    gui_cord.update()
                    gui_cord.event_generate("<Button-1>")
                    reveal_count += 1
    if reveal_count > 0:
        return True
    else:
        return False


# Checks if coordinate map number at [X, Y] is equal to number of surrounding flags 
def CheckSquare(X, Y, Width, Height):
    flag_count = 0
    gui_cord = GUI_MAP[Y][X]
    rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
    for rot in rots:
        x_ = X + rot[0]
        y_ = Y + rot[1]
        if 0 <= x_ < Width:
            if 0 <= y_ < Height:
                # Adds surrounding flags to flag count
                if GUI_MAP[y_][x_]["text"] == "⚑":
                    flag_count += 1
    if flag_count == int(gui_cord["text"]):
        return True
    else:
        return False


# Eliminates qualifying edge coordinates 
def ElimEdges(Width, Height):
    elim_count = 0
    for x in range(Width):
        for y in range(Height):
            gui_cord = GUI_MAP[y][x]
            # Checks revealed coordinates with numbers
            if gui_cord["text"] != " " and gui_cord["text"] != "⚑":
                # Clear 3x3 square if the coordinate qualifies
                if CheckSquare(x, y, Width, Height):
                    if ClearSquare(x, y, Width, Height):
                        elim_count += 1
    # Does not keep eliminating edges if no more edges qualify  
    if elim_count > 0:
        return True
    else:
        return False


# Predicts edge coordinate to eliminate
def PredictEdge(Width, Height):
    # Keeps track of most probable edge coordinate
    min_numbers = 9
    min_cords = []
    for x in range(Width):
        for y in range(Height):
            gui_cord = GUI_MAP[y][x]
            # Checks only hidden and non-flagged coordinates
            if gui_cord["bg"] == "grey" and gui_cord["text"] != "⚑":
                numbers_count = 0
                rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
                for rot in rots:
                    x_ = x + rot[0]
                    y_ = y + rot[1]
                    if 0 <= x_ < Width:
                        if 0 <= y_ < Height:
                            # If the surrounding coordinate has a number add to count
                            if GUI_MAP[y_][x_]["text"] != " " and GUI_MAP[y_][x_]["text"] != "⚑":
                                numbers_count += 1
                if numbers_count != 0 and numbers_count < min_numbers:
                    min_numbers = numbers_count
                    min_cords = [x, y]
    # Reveal most probable coordinate (can be wrong)
    if len(min_cords) != 0:
        min_x = min_cords[0]
        min_y = min_cords[1]
        GUI_MAP[min_y][min_x].update()
        GUI_MAP[min_y][min_x].event_generate("<Button-1>")


# Runs the solver algorithm 
def SolveAlg(Width, Height):
    # CPU time capped by maximum iteration count 
    for iter in range(MAX_ITER):
        # Just for visualization
        # time.sleep(.1)
        if GAME_OVER:
            break
        # Pick random coordinates until at least 10% of the map is revealed 
        if Width * Height - HIDDEN < int(Width * Height / 10):
            PickRand(0, 0, Width - 1, Height - 1, Width, Height)
        else:
            # Flags the edges, if not then eliminates the edges, if not then makes a prediction
            if not FlagEdges(Width, Height):
                if not ElimEdges(Width, Height):
                    PredictEdge(Width, Height)


MASTER = Tk(className="Mine Sweepers")
MAP_FRAME = Frame(MASTER)
STATUS = Label(MASTER, text="")
SOLVER = Button(MASTER, command=lambda Width=WIDTH, Height=HEIGHT: SolveAlg(Width, Height), text="Solver")
RESET = Button(MASTER, command=lambda Width=WIDTH, Height=HEIGHT, Mines=MINES: ResetMap(Width, Height, Mines),
               text="Reset")
SUCCESS = 0
TOTAL = 0
for a in range(16):
    MINES = a + 3
    ResetMap(WIDTH, HEIGHT, MINES)
    for b in range(200):
        TOTAL += 1
        SolveAlg(WIDTH, HEIGHT)
        if STATUS["text"] == "You won!":
            SUCCESS += 1
        ResetMap(WIDTH, HEIGHT, MINES)
    print("Mines: " + str(MINES) + " " + "Rate: " + str(SUCCESS / TOTAL))
    SUCCESS = 0
    TOTAL = 0
mainloop()
