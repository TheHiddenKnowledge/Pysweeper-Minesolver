## @mainpage
# This project aims to create a simple minesweepers game using Tkinter,
# as well as a solver for the game.
# @par Latest Release:
# V1.1 - 1/3/2026
# @par Created by: I. Finney
# @par Revision History:
# @version 1.0 Initial Release.
# @version 1.1 Revised code Base.

import pysweepers
import minesolver
import tkinter as tk

GAME = pysweepers.PySweepers(8, 8 , 6)

SOLVER = minesolver.MineSolver(GAME)

SOLVER.run_solver()

GAME.run_game()