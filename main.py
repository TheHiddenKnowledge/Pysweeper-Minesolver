import pysweeper
import minesolver

GAME = pysweeper.PySweeper(10, 10, 10)

SOLVER = minesolver.MineSolver(GAME)

won = 0
lost = 0

for a in range(100):
    SOLVER.run_solver(False)
    if GAME.game_status == "won":
        won += 1
    elif GAME.game_status == "lost":
        lost += 1
    GAME.reset_map()
print(won/(won+lost))

GAME.run_game()