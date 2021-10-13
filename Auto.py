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


def doPuzzle(puzzle):
    print("You are playing {}.".format(colour(puzzle[0])))
    original = puzzle[0]
    s.set_fen_position(original)
    bestMove = s.get_best_move()
    origeval = ast.literal_eval(str(s.get_evaluation()))['value']
    print("In the game, you played {}. This was a mistake, find a better move.".format(puzzle[1]))

    while True:
        s.set_fen_position(original)
        print(s.get_board_visual())
        
        move = input("Enter Move: ")
    
        s.make_moves_from_current_position([move])
        print(s.get_board_visual())
        if move == bestMove:
            print("Well done! This is the best move.")
            break

        elif origeval - ast.literal_eval(str(s.get_evaluation()))['value'] > 100:
            
            print("That was a mistake. What would you like to do?")
            option = int(input("1. Try Again\n2. See Refutation\n3. Give up\n4. Exit\n"))
            if option == 4:
                print("Closing Program")
                return 3
            elif option == 3:
                print("The best move was {}.".format(s.get_best_move()))
                break
            elif option == 1:
                continue
            elif option == 2:
                print("Refutation: \n")
                refute(original, move)
                break
            else:
                print("Invalid choice, closing program")
                break
        else:
            print("Your move was satisfactory, it was not the best but it was not a mistake.")
            option = int(input("1. Try Again\n2. Continue\n3. Exit\n"))
            if option == 1:
                continue
            elif option == 2:
                print("The correct move was {}.".format(bestMove))
                break
            elif option == 3:
                print("Closing program")
                break
def play(colour, c):
    
    boardval = 50
    mistakes = []
    if colour == 1:
        s.make_moves_from_current_position([s.get_best_move()])
    while True:
        if ast.literal_eval(str(s.get_evaluation()))['value'] == 0:
            break
        
        print(s.get_board_visual())
        currpos = s.get_fen_position()
        
        move = input("Enter Move: ")
        if move == "resign":
            break
        s.make_moves_from_current_position([move])
        
        if boardval - ast.literal_eval(str(s.get_evaluation()))['value'] > 150:
            dbadd = "INSERT INTO Puzzles VALUES ('"+currpos+"', '"+move+"', 1)"
            c.execute(dbadd)

            
        boardval = ast.literal_eval(str(s.get_evaluation()))['value']
        s.make_moves_from_current_position([s.get_best_move()])

        if ast.literal_eval(str(s.get_evaluation()))['value'] == 0:
            dbadd = "INSERT INTO Puzzles VALUES ('"+currpos+"', '"+move+"', 1)"
            c.execute(dbadd)
            mistakes.append((currpos, move))
            break

    return mistakes

def train(c):
    c.execute("SELECT * FROM Puzzles WHERE  Counter = 1")
    result = c.fetchall()
    for i in result:
        if doPuzzle(i) == 3:
            break


