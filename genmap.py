full_map = [[" " for i in range(5)] for i in range(5)]
full_map[0][0] = "*"
full_map[0][4] = "*"
full_map[1][4] = "*"
full_map[3][1] = "*"
full_map[2][2] = "*"
hidden_map = [["□" for i in range(5)] for i in range(5)]
mines = 5
hidden = 25
rots = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]


def getnums():
    h = len(full_map)
    w = len(full_map[0])
    for i in range(h):
        for j in range(w):
            if full_map[i][j] != "*":
                count = 0
                for rot in rots:
                    i_ = i + rot[1]
                    j_ = j + rot[0]
                    if i_ >= 0 and i_ < h:
                        if j_ >= 0 and j_ < w:
                            if full_map[i_][j_] == "*":
                                count += 1
                if count > 0:
                    full_map[i][j] = str(count)


getnums()


def fill(x, y, fill_list):
    h = len(full_map)
    w = len(full_map[0])
    rotc = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    if [x, y] not in fill_list:
        fill_list.append([x, y])
        for rot in rotc:
            i_ = y + rot[1]
            j_ = x + rot[0]
            if i_ >= 0 and i_ < h:
                if j_ >= 0 and j_ < w:
                    if full_map[i_][j_] != "*" and full_map[i_][j_] != " ":
                        if [j_, i_] not in fill_list:
                            if hidden_map[j_][i_] == "□":
                                fill_list.append([j_, i_])
                    elif full_map[i_][j_] == " ":
                        fill(j_, i_, fill_list)


def pickgrid(x, y):
    global hidden
    if full_map[y][x] != "*" and full_map[y][x] != " ":
        hidden_map[y][x] = full_map[y][x]
        hidden -= 1
        return False
    elif full_map[y][x] == " ":
        fill_list = []
        fill(x, y, fill_list)
        for filly in fill_list:
            x_ = filly[0]
            y_ = filly[1]
            hidden_map[y_][x_] = full_map[y_][x_]
            hidden -= 1
        return False
    else:
        hidden_map[y][x] = full_map[y][x]
        return True


while (1 == 1):
    print(mines)
    print(hidden)
    for row in hidden_map:
        print("".join(row))
    x = int(input("Pick a grid (x): "))
    y = int(input("Pick a grid (y): "))
    print("\n")
    if pickgrid(x, y):
        for row in hidden_map:
            print("".join(row))
        print("You suck!")
        break
    else:
        if mines == hidden:
            for row in hidden_map:
                print("".join(row))
            print("You rock!")
            break
