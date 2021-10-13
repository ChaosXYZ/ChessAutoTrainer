from stockfish import Stockfish
import ast
import sqlite3
import time

s = Stockfish("/Users/44751/Desktop/stockfish.exe")
s.set_skill_level(20)

#Utility Functions
def colour(FEN):
    """
    Gets colour from FEN 
    """
    fen = FEN.split(" ")
    if fen[1] == "w":
        return "White"
    return "Black"

def createTable(c):
    c.execute("""CREATE TABLE puzzles(
                FEN text,
                Move text,
                Counter integer
                )""")

def refute(FEN, Move):
    s.set_fen_position(FEN)
    s.make_moves_from_current_position([Move])
    evaluation = ast.literal_eval(str(s.get_evaluation()))['value']
    ply = 10
    while ply != 0 or evaluation - ast.literal_eval(str(s.get_evaluation()))['value'] > 100:
        print(s.get_best_move())
        s.make_moves_from_current_position([s.get_best_move()])
        print(s.get_board_visual())
        time.sleep(1)
        
        ply -= 1

