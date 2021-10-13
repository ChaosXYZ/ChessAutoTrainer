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
