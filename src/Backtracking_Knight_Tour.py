import pandas as pd
import timeit

# CONST VARIABLE
BLANK = " "
SIZE = 8
MOVE = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]

## Default Chess Board
IDX_V = [str(SIZE-i) for i in range(SIZE)]
IDX_H = [chr(65+i) for i in range(SIZE)]
DEFAULT_BOARD = [[h+v for h in IDX_H] for v in IDX_V]

# SHOW BOARD WITH TITLE
def show_board(papan, teks):
    length = max([len("".join(row)) for row in papan]) + SIZE*2
    print()
    print(f'{"╔"}{"═"*length}{"╗"}')
    print(f'║{BLANK*((length+1-len(teks))//2)}{teks.title()}{BLANK*round((length-len(teks))/2)}║')
    print(f'{"╚"}{"═"*length}{"╝"}')
    print(pd.DataFrame(papan, index=IDX_V, columns=IDX_H))
    print()

# OPEN KNIGHT'S TOUR
def validate_move(papan, pos_x, pos_y):
    if (pos_x >= 0 and pos_y >= 0 and pos_x < SIZE and pos_y < SIZE):
        return papan[pos_x][pos_y] == "0"
    return False

def valid_move(papan, pos_x, pos_y):
    return [(x, y) for x, y in MOVE if validate_move(papan, x+pos_x, y+pos_y)]

def sort_move_byCountNextValidMove(papan, pos_x, pos_y):
    move_withCountNextValidMove = [ (len(valid_move(papan, pos_x+x, pos_y+y)), x, y) for x,y in valid_move(papan, pos_x, pos_y)]
    return [(pos[1], pos[2]) for pos in sorted(move_withCountNextValidMove)]

# CLOSED KNIGHT'S TOUR
def is_neighbour(pos_x, pos_y, origin):
    return next((True for i in range(SIZE) if MOVE[i][0]+pos_x == origin[0] and MOVE[i][1]+pos_y == origin[1]), False)

def is_full_neighbour(papan, origin):
    return next((False for x,y in valid_move(papan, origin[0], origin[1]) if papan[x][y] == "0"), True)

# RECURSIVE SOLVING
def recursive_solving(tipe, papan, pos_x, pos_y, origin, n_step):
    if tipe == "close":
        if n_step == (SIZE**2)+1 and is_neighbour(pos_x, pos_y, origin):
            return True
    else:
        if n_step == (SIZE**2)+1:
            return True
    
    for x,y in sort_move_byCountNextValidMove(papan, pos_x, pos_y):
        new_pos_x = pos_x + x
        new_pos_y = pos_y + y

        papan[new_pos_x][new_pos_y] = f"({n_step})" if n_step == SIZE**2 else f"{n_step}"
        #show_board(papan, "proses")
        if recursive_solving(tipe, papan, new_pos_x, new_pos_y, origin, n_step+1):
            return True

        # else
        papan[new_pos_x][new_pos_y]= "0"
        #show_board(papan, "mundur")
    
    return False

def knights_tour():
    show_board(DEFAULT_BOARD, "papan catur")
    # Asumsi inputan valid
    first_loc = input("Masukkan posisi awal: ")
    tipe = input("Masukkan tipe (close/open): ")

    v0 = IDX_H.index(first_loc[0].upper())
    h0 = IDX_V.index(first_loc[1])

    init_board = [[str(0) for i in range(SIZE)] for j in range(SIZE)]
    init_board[h0][v0] = "(1)"
    n_step = 2

    print("\n--- Perhitungan waktu dimulai ---")
    start = timeit.default_timer()

    show_board(init_board, "first loc")

    if not recursive_solving(tipe, init_board, h0, v0, (h0,v0), n_step):
        stop = timeit.default_timer()
        print("\n--- Perhitungan waktu selesai ---\n")

        print(f"Solusi tidak ditemukan,\nwaktu yang diperlukan {stop - start} detik\n")
    else:
        stop = timeit.default_timer()
        print("\n--- Perhitungan waktu selesai ---\n")

        show_board(init_board, "hasil akhir")
        print(f"Solusi ditemukan,\nwaktu yang diperlukan {stop - start} detik\n")

if __name__ == "__main__":
    knights_tour()