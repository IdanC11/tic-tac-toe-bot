# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 05:11:27 2023

@author: edanc
"""
from numpy import array
import numpy as np
import random
from tabulate import tabulate
import sqlite3 as lite
import datetime

db_file_name = 'ttt_db.db'

squares = {'tl': 0, 'tc': 0, 'tr': 0,
           'ml': 0, 'mc': 0, 'mr': 0,
           'bl': 0, 'bc': 0, 'br': 0}

squares_Nums = {1: 'tl'}

opposites = {'t': 'b',
             'b': 't',
             'l': 'r',
             'r': 'l',
             'c': 'c',
             'm': 'm'}

corners = ['tl', 'tr', 'bl', 'br']

wins1 = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 1, 0, 0, 0],
                  [1, 0, 0, 1, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 1, 1],
                  [0, 1, 0, 0, 1, 0, 0, 1, 0],
                  [0, 0, 1, 0, 0, 1, 0, 0, 1],
                  [1, 0, 0, 0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 0, 1, 0, 1, 0, 0]])

def ConnectToDB():
    conn = lite.connect(db_file_name)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE GameTable(player1 TEXT, player2 TEXT, date DATE, score TEXT)")
    except:
        pass

    return conn, cursor
    
#def Insert_Name_DB(name):
    

def Is_Opp_Corner(corner1, corner2):
    if corner1[0] != corner2[0] and corner1[1] != corner2[1]:
        return True
    return False

def Is_Touching(square1, square2):
    if (square1 in corners) and (square2 in corners):
        return False
    elif square1[0] == square2[0] or square1[1] == square2[1]:
       return True
    return False

def Is_Side(square):
    if square[0] == 'm' or square[1] == 'c':
        return True
    return False

def X_Turn():
    if not Is_Winner():
        move = input("X Turn: \nchoose your play: ")
        while move not in squares.keys():
            move = input('Wrong input, try again: ')
        while squares[move] != 0:
            move = input('Cell already taken, try again: ')
        
        squares[move] = 1
        Print_Board_Game()

        return move
    
def O_Turn():
    if not Is_Winner():
        move = input("O Turn: \nchoose your play: ")
        while move not in squares.keys():
            move = input('Wrong input, try again: ')
        while squares[move] != 0:
            move = input('Cell already taken, try again: ')
        #while squares[move] != 0:
         #   move = input("O Turn: Incorrect Input \nchoose your play: ")

        squares[move] = -1
        Print_Board_Game()
        return move
    
def Print_Board_Start():
    board = """
          tl | tc | tr
         -------------
          ml | mc | mr
         -------------
          bl | bc | br
    """

    print(board)
    
def Print_Board_Game():
   variables = ['', '', '', '', '', '', '', '', '',]
   i = -1
   for key in squares:
       i = i + 1
       if squares[key] == 0:
           variables[i] = ' '
       if squares[key] == -1:
           variables[i] = 'O'
       if squares[key] == 1: 
           variables[i] = 'X'
   board = f"""
         l   c   r
         
     t   {variables[0]} | {variables[1]} | {variables[2]}
        -----------
     m   {variables[3]} | {variables[4]} | {variables[5]}
        -----------
     b   {variables[6]} | {variables[7]} | {variables[8]}
   """

   print(board)

def Is_Winner():
    sums = np.dot(wins1, list(squares.values()))
    for i in sums:
        if 3 in sums:
            print("X Player Won!")
            return True
        if -3 in sums:
            print("O Player Won!")
            return True
    return False

def Two_Players():
    Player1_Name = input('Player 1, Enter your name: ')
    Player2_Name = input('Player 2, Enter your name: ')
    Player1_Shape = input('Player 1, Pick your shape (X/O): ')
    while Player1_Shape != 'X' and Player1_Shape != 'O':
        Player1_Shape = input('Wrong input, pick again (X/O): ')
    if Player1_Shape == 'X':
        Player2_Shape = 'O'
        print('Player 2, your shape is O.')
    else:
        Player2_Shape = 'X'
        print('Player 2, your shape is X.')
        
    randNum = random.randint(0, 1)
    
    for i in range(9):
        if randNum == 1:
            X_Turn()
            randNum = 0
            if Is_Winner():
                if Player1_Shape == 'X':
                    return Player1_Name, Player2_Name, Player1_Name
                else:
                    return Player1_Name, Player2_Name, Player2_Name

            
        else:
            O_Turn()
            randNum = 1
            if Is_Winner():
                if Player1_Shape == 'O':
                    return Player1_Name, Player2_Name, Player1_Name
                else:
                    return Player1_Name, Player2_Name, Player2_Name
    print("It's a TIE!")
    return Player1_Name, Player2_Name, 'Tie'
            
def PC_Bot_Second(turn, shape, last_moveP, first_moveP, shape_Player):
    if turn == 2:
        if squares['mc'] == 0:
            squares['mc'] = shape
            print(squares)            
            return
        else:
            squares['tl'] = shape
            print(squares)            
            return
        
    if turn == 4:
        if first_moveP == 'mc': #MIDDLE
            if last_moveP in corners:
                for i in range(4):
                    if squares[corners[i]] == 0:
                        squares[corners[i]] = shape
                        print(squares)            
                        return
            else:
                for key in squares:
                    if squares[key] == 0:
                        squares[key] = shape_Player
                        if Is_Winner():
                            squares[key] = shape
                            print(squares)            
                            return
                        else:
                            squares[key] = 0
                            
        else:
            if last_moveP in corners:
                if Is_Opp_Corner(last_moveP, first_moveP):
                    for key in squares:
                        if squares[key] == 0 and Is_Touching(key, first_moveP):
                            squares[key] = shape
                            print(squares)            
                            return
                else:
                    for key in squares:
                        if squares[key] == 0:
                            squares[key] = shape_Player
                            if Is_Winner():
                                squares[key] = shape
                                print(squares)            
                                return
                            else:
                                squares[key] = 0
            else:
                if Is_Touching(last_moveP, first_moveP):
                    for key in squares:
                        if squares[key] == 0:
                            squares[key] = shape_Player
                            if Is_Winner():
                                squares[key] = shape
                                print(squares)            
                                return
                            else:
                                squares[key] = 0
                else:
                    for i in range(4):
                        if squares[corners[i]] == 0:
                            squares[corners[i]] = shape
                            print(squares)            
                            return
                
                        
    if turn == 6:
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                if Is_Winner():
                    print(squares)            
                    return
                else:
                    squares[key] = 0
        
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape_Player
                if Is_Winner():
                    squares[key] = shape
                    print(squares)            
                    return
                else:
                    squares[key] = 0
                    
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                print(squares)            
                return
                
    if turn == 8:
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                if Is_Winner():
                    print(squares)            
                    return
                else:
                    squares[key] = 0
        
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape_Player
                if Is_Winner():
                    squares[key] = shape
                    print(squares)            
                    return
                else:
                    squares[key] = 0
                    
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                print(squares)            
                return
            
    return

def PC_Bot_First(turn, last_moveP, shape, first_move, first_moveP, shape_Player):
    if turn == 1:
        squares['tl'] = shape
        print(squares)            
        return #'tl'
    
    if turn == 3:
        if last_moveP == 'mc':
            for i in range(4):
                if Is_Opp_Corner(first_move, corners[i]):
                    squares[corners[i]] = shape
                    print(squares)            
                    return
                
                    
        
        if last_moveP[0] == 'm' or last_moveP[1] == 'c': # ***SIDES OPTIONS***
            for i in range(1,4):
                if not Is_Touching(corners[i], last_moveP) and not Is_Opp_Corner(corners[i], first_move):
                    squares[corners[i]] = shape
                    print(squares)
                    return
                
                    
        if last_moveP in corners:
            for i in range(4):
                if squares[corners[i]] == 0:
                    squares[corners[i]] = shape
                    print(squares)            
                    return
    if turn == 5:
        if first_moveP == 'mc':
            if last_moveP in corners:
                for i in range(4):
                    if squares[corners[i]] == 0:
                        squares[corners[i]] = shape
                        print(squares)            
                        return
            else:
                for key in squares:
                    if squares[key] == 0:
                        squares[key] = shape_Player
                        if Is_Winner():
                            squares[key] = shape
                            print(squares)            
                            return
                        else:                   # WILL NEVER BE REACHED
                            squares[key] = 0
                            
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                if Is_Winner():
                    print(squares)            
                    return
                else:
                    squares[key] = 0
                    
                    
        if first_moveP[0] == 'm' or first_moveP[1] == 'c':
            for i in range(4):
                if Is_Opp_Corner(corners[i], first_move):
                    squares[corners[i]] = shape
                    print(squares)            
                    return
        
        for i in range(4):
            if squares[corners[i]] == 0:
                squares[corners[i]] = shape
                print(squares)            
                return
            
    if turn == 7:
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                if Is_Winner():
                    print(squares)            
                    return
                else:
                    squares[key] = 0
                    
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape_Player
                if Is_Winner():
                    squares[key] = shape
                    print(squares)            
                    return
                else:                   # WILL NEVER BE REACHED
                    squares[key] = 0
                        
    if turn == 9:
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                if Is_Winner():
                    print(squares)            
                    return
                else:
                    squares[key] = 0
                    
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape_Player
                if Is_Winner():
                    squares[key] = shape
                    print(squares)            
                    return
                else:                   
                    squares[key] = 0
                    
        for key in squares:
            if squares[key] == 0:
                squares[key] = shape
                print(squares)            
                return
         
    print(squares)            
    return

            
def PC_VS_Player():
    player = input('please enter your name: ')
    randNum = random.randint(0, 1) # 1 - pc starts, 0 - player starts
    randShape = random.randint(0, 1)
    pc_shape = int(1) # X - PC
    player_shape = int(-1) # O - Player
    if randShape == 0:
        pc_shape = int(-1) # O - PC
        player_shape = int(1) # X - Player
    starter = randNum
    turn = int(0)
    move = 'br'
    first_move = 'tl'
    first_moveP = 'ff'
    if randNum == 1:
        print('PC STARTS!')
    else:
        print('PLAYER STARTS!')
    
    for i in range(9):
        turn = i + 1
        if randNum == 1:
            randNum = 0
            if starter == 0:
                PC_Bot_Second(turn, pc_shape, move, first_moveP, player_shape)
            else:
                PC_Bot_First(turn, move, pc_shape, first_move, first_moveP, player_shape)
            Print_Board_Game();
            if Is_Winner():
                return 'PC', player, 'PC'
            
        else:
            if player_shape == -1: 
                move = O_Turn()
            else:
                move = X_Turn()
            if turn == 1:
                first_moveP = move
            if turn == 2 and first_moveP == 'ff':
                first_moveP = move
            randNum = 1
            if Is_Winner():
                return 'PC', player, player
            
    return 'PC', player, 'Tie'
    
            
conn, cursor = ConnectToDB()

print("[1] player vs player")
print("[2] player vs pc")
print("[3] veiw statistics")
print("[4] clear statistics")
result = input('please choose from the menu: ')
while result not in ['1','2','3','4']:
    result = input('wrong choice, please choose from the menu: ')

if result == '1':
    print("This is the board's coordinates: ")
    Print_Board_Start()
    player1, player2, winner = Two_Players()
    # insert to DB
    d = datetime.datetime.now()
    cursor.execute("INSERT INTO GameTable(player1, player2, date, score)VALUES(?,?,?,?)",
                   (player1, player2, str(d.year)+'-'+str(d.month)+'-'+str(d.day), winner))
    conn.commit()
    
elif result == '2':
    print("This is the board's coordinates: ")
    Print_Board_Start()
    player1, player2, winner = PC_VS_Player()
    # insert to DB
    d = datetime.datetime.now()
    cursor.execute("INSERT INTO GameTable(player1, player2, date, score)VALUES(?,?,?,?)",
                   (player1, player2, str(d.year)+'-'+str(d.month)+'-'+str(d.day), winner))
    conn.commit()
    
elif result == '3':
    player = input(r"please enter player's name to view statistics: ")
    cursor.execute("SELECT player1, player2, date, score FROM GameTable WHERE player1=? or player2=?",
                   (player, player))
    all_games = cursor.fetchall()
    wins = 0
    looses = 0
    ties = 0
    for game in all_games:
        if game[3] == player:
            wins = wins + 1
        elif game[3] == 'Tie':
            ties = ties + 1
        else:
            looses = looses + 1
    print(f"{player} won {wins} times, lost {looses} times, and made a tie for {ties} times")
    
elif result == '4':
    result = input(r"are you sure you want to clean the statistics? y/[n]: ")
    if result == 'y':
        cursor.execute('DROP TABLE GameTable')
        conn.commit()
    print('the Table was cleared successfully')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    