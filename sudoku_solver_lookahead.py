import copy
import random
import time

Row = "ABCDEFGHI"
Col = "123456789"
Digits = "123456789"
Cells = [r + c for r in Row for c in Col]

def cross(A, B):
    return [a+b for a in A for b in B]

Rows = [cross(r, Col) for r in Row]
Cols = [cross(Row, c) for c in Col]
Boxes = [cross(rs, cs) for rs in ("ABC","DEF","GHI") for cs in ("123","456","789")]
Units = Rows + Cols + Boxes

unit_map = {c: [u for u in Units if c in u] for c in Cells}
neighbors = {c: set(sum(unit_map[c], [])) - {c} for c in Cells}

def parse_grid(grid_str):
    values = {c: Digits for c in Cells}
    for c, val in zip(Cells, grid_str):
        if val in Digits:
            if not assign(values, c, val):
                return None
    return values

def assign(values, cell, val):
    other_vals = values[cell].replace(val, '')
    if all(eliminate(values, cell, v) for v in other_vals):
        return True
    return False

def eliminate(values, cell, val):
    if val not in values[cell]:
        return True
    values[cell] = values[cell].replace(val, '')
    if len(values[cell]) == 0:
        return False
    elif len(values[cell]) == 1:
        v = values[cell]
        if not all(eliminate(values, peer, v) for peer in neighbors[cell]):
            return False
    for u in unit_map[cell]:
        places = [c for c in u if val in values[c]]
        if len(places) == 0:
            return False
        elif len(places) == 1:
            if not assign(values, places[0], val):
                return False
    return True

def look_ahead(values):
    changed = True
    while changed:
        changed = False
        for cell in Cells:
            if len(values[cell]) == 1:
                val = values[cell]
                for peer in neighbors[cell]:
                    if val in values[peer]:
                        values[peer] = values[peer].replace(val, '')
                        if len(values[peer]) == 0:
                            return False
                        changed = True
    return True

def look_back(values):
    for cell in Cells:
        if len(values[cell]) == 0:
            for peer in neighbors[cell]:
                if len(values[peer]) > 1:
                    for val in values[peer]:
                        new_values = copy.deepcopy(values)
                        if assign(new_values, peer, val) and look_ahead(new_values):
                            return new_values
            return False
    return values

def solve_sudoku(grid_str):
    values = parse_grid(grid_str)
    if values is None:
        return None
    if not look_ahead(values):
        return None

    for c in Cells:
        if len(values[c]) > 1:
            values[c] = random.choice(values[c])

    for _ in range(100000):
        conflicts = [c for c in Cells if any(values[c] == values[peer] for peer in neighbors[c])]
        if not conflicts:
            return values

        cell = random.choice(conflicts)
        vals = list(Digits)
        random.shuffle(vals)
        for val in vals:
            new_values = copy.deepcopy(values)
            if assign(new_values, cell, val) and look_ahead(new_values):
                values = new_values
                break
        else:
            result = look_back(values)
            if result is False:
                continue
            values = result
    return None

def print_board(values):
    width = 1 + max(len(values[c]) for c in Cells)
    line = "+".join(["-"*(width*3)]*3)
    for r in Row:
        print("".join(values[r+c].center(width) + ("|" if c in "36" else "") for c in Col))
        if r in "CF":
            print(line)

def load_sudoku_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return ''.join(line.strip() for line in lines)

# ==== EJECUCIÓN ====
if __name__ == "__main__":
    sudoku_str = load_sudoku_from_file("sudoku.txt")
    start = time.time()
    solution = solve_sudoku(sudoku_str)
    end = time.time()

    if solution:
        print(f"\u2713 Sudoku resuelto en {end - start:.2f} segundos:")
        print_board(solution)
    else:
        print("\u2717 No se pudo resolver el Sudoku.")
