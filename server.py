# flask run server.py
#OR
# FLASK_APP=server.py flask run
# flask --app server.py --debug run

from flask import Flask,render_template,request,redirect,url_for
from jinja2 import Template

app = Flask(__name__,template_folder="templates", static_folder= "static")
'''
Post = namedtuple('Post',['title'])
user_to_posts={
    'alice':[
    ]
}
'''
import pandas as pd
from record import *
games_filename = "/Users/yunhan/week5/tictactoe/game_record.csv"
move_filename = "/Users/yunhan/week5/tictactoe/move_record.csv"
result_filename = "/Users/yunhan/week5/tictactoe/result.csv"

def make_empty_board():
    return [
        [None,None,None],
        [None,None,None],
        [None,None,None],
    ]

def game_type():
    game_type = int(input("Please input the number of the player(1 or 2):"))
    return game_type

class Game():
    def __init__(self):
        self.board = make_empty_board()
        self.player_number = game_type()
        if self.player_number == 1:
            self.start_game(1,self.board)
        elif self.player_number == 2:
            self.start_game(2,self.board)
    
    def get_winner(self,Board):
        iswin = None
        if Board[0][0] == Board[1][1] == Board[2][2] or Board[0][2] == Board[1][1] == Board[2][0]:
            iswin = Board[1][1]
        else:
            for i in range(0,3):
                if Board[i][0] == Board[i][1] == Board[i][2]:
                    iswin = Board[i][0]
                    break
                elif Board[0][i] == Board[1][i] == Board[2][i]:
                    iswin = Board[0][i]
                    break
        return iswin


    def game_state(self,winner,Board):
        iswin = winner
        if iswin == 'X' or iswin == 'O':
            return iswin
        elif (None in Board[0]) or (None in Board[1]) or (None in Board[2]):
            return None
        else:
            return 'Draw'

    def update_board(self,board,target_position,current_player):
        target_position_row = int(target_position[0])-1
        target_position_col = int(target_position[1])-1
        board[target_position_row][target_position_col] = current_player
        return board

    def print_board(self,board):
        output_board = ''
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    str_new = ' '
                else:
                    str_new = str(board[i][j])
                output_board = output_board + '|' + str_new 
            output_board = output_board + '|' + '\n'
            output_board = output_board + '-------'
            output_board = output_board + '\n'
        return output_board

    def first_player(self):
        first_player = input("Please input the icon you want(X or O):")
        return first_player

    def get_player_name(self,current_player):
    # Get player name
        player_name = input("Please input the player name of %s:"%current_player)
        return player_name
    
    def other_player(self,player):
        if player == 'X':
            return 'O' 
        elif player == 'O':
            return 'X'
    
    def record_result(self, result, player_name,winner_name):
        exist = result.loc[result['PlayerName'] == player_name]
        if exist.empty:
            result.loc[len(result)] = {
                "PlayerName":player_name,
                "WinTimes":0,
                "LoseTimes":0,
                "DrawTimes":0
            }
            exist = result.loc[len(result)-1]
        if winner_name == player_name:
            result.loc[result[result["PlayerName"] == player_name].index, "WinTimes"] += 1
        elif winner_name == "Draw":
            result.loc[result[result["PlayerName"] == player_name].index, "DrawTimes"] += 1
        else:
            result.loc[result[result["PlayerName"] == player_name].index, "LoseTimes"] += 1
        return result

    # def start_game(self,game_type,board):
    #     games = begin_data()
    #     # start record game

    #     moves = record_move()
    #     # start record move

    #     result = result_record()
    #     # all player rank result file

    #     turn = 1

    #     board = self.board
    #     winner = None
    #     if game_type == 2:
    #         current_player = self.first_player()
    #         if current_player == "X":
    #             player_name_X = self.get_player_name(current_player)
    #             player_name_O = self.get_player_name("O")
    #         else:
    #             player_name_O = self.get_player_name(current_player)
    #             player_name_X = self.get_player_name("X")

    #     else:
    #         current_player = 'O'
    #         player_name_O = self.get_player_name(current_player)
    #         player_name_X = "Bot"

    #     #print board
    #     print(self.print_board(board))
    #     while winner == None:
    #         #get move
    #         human = Human()
    #         target_position = human.get_move()
    #         #update & print board
    #         board = self.update_board(board,target_position,current_player)
    #         print(self.print_board(board))
    #         #get winner
    #         is_win = self.get_winner(board)
    #         winner = self.game_state(is_win,board)
    #         if current_player == "X":
    #             current_player_name = player_name_X
    #         else:
    #             current_player_name = player_name_O
    #         # record move
    #         moves.loc[len(moves)] = {
    #             "Game ID":len(games)+1,
    #             "Turn":turn,
    #             "Player":current_player_name,
    #             "Position":(target_position[0],target_position[1])}
    #         turn = turn + 1
    #         if winner == None:
    #             # Robot player
    #             if game_type == 1:
    #                 current_player = self.other_player(current_player)
    #                 bot = Bot()
    #                 target_position = bot.random_move(board)
    #                 board = self.update_board(board,target_position,current_player)
    #                 print(self.print_board(board))
    #                 is_win = self.get_winner(board)
    #                 winner = self.game_state(is_win,board)
    #                 # record move
    #                 moves.loc[len(moves)] = {
    #                     "Game ID":len(games)+1,
    #                     "Turn":turn,
    #                     "Player":"Bot",
    #                     "Position":(target_position[0],target_position[1])}
    #                 turn = turn + 1
    #             # Human player
    #             current_player = self.other_player(current_player)
    #             print("Take a turn, %s turn" %current_player)
    #     if winner == "X":
    #         winner_name = player_name_X
    #     elif winner == "O":
    #         winner_name = player_name_O
    #     else:
    #         winner_name = "Draw"
        
    #     if winner == "X" or winner == "O":
    #         print("The winner is %s !" %winner_name)
    #     elif winner == "Draw":
    #         print("This game is draw!")
        
    #     games.loc[len(games)] = {
    #         "Game ID":len(games)+1,
    #         "Player 1":player_name_O,
    #         "Player 2":player_name_X,
    #         "Winner":winner_name,
    #         }
    #     self.record_result(result, player_name_X,winner_name)
    #     self.record_result(result, player_name_O,winner_name)

        

    #     moves.to_csv(move_filename, encoding='utf-8', index=False)
    #     games.to_csv(games_filename, encoding='utf-8', index=False)
    #     result.to_csv(result_filename, encoding='utf-8', index=False)

class Human():
    def __init__(self):
        super().__init__()
        return None
        
    def get_move(self):
        target_position = input("Please input the position you want to put(eg: 13 for row 1 and col 3):")
        return target_position

class Bot():
    def __init__(self):
        super().__init__()
        return None

    def random_move(self,board):
        import random
        target_row = 4
        target_col = 4
        while target_row == 4 or target_col == 4:
            row = random.randint(1,3) #same as the input with the user row 1-3 and col 1-3
            col = random.randint(1,3)
            if board[row-1][col-1] == None:
                target_row = row
                target_col = col
        target_position = str(target_row)+str(target_col)
        return target_position


class Data():
    player_1_name = None
    player_2_name = None
    game_type = 1
    board = None
    winner = None
    current_player = "O"

data = Data()


@app.route("/", methods = ["POST","GET"])
def index():
    if request.method == "POST":
        return redirect("/play")
    else:
        return render_template("index.html")


@app.route("/play",methods=["POST","GET"])
def play():
    if request.method == "POST":
        target_position_row = request.form["Row"]
        target_position_col = request.form["Column"]
        target_position = target_position_row + target_position_col
        data.board = update_board(data.board,target_position,data.current_player)
        data.current_player = other_player(data.current_player)
        iswin = get_winner(data.board)
        data.winner = game_state(iswin,data.board)
        if data.current_player == "O":
            playername = data.player_1_name
        else:
            playername = data.player_2_name
        if data.winner == None:
            if data.game_type == "Bot":
                bot = Bot()
                target_position = bot.random_move(data.board)
                data.board = update_board(data.board,target_position,data.current_player)
                iswin = get_winner(data.board)
                data.winner = game_state(iswin,data.board)
                data.current_player = other_player(data.current_player)
                if data.current_player == "O":
                    playername = data.player_1_name
                else:
                    playername = data.player_2_name
                return render_template("play.html",playername = playername,board = data.board,target_position = target_position_col)
            return render_template("play.html",playername = playername,board = data.board,target_position = target_position_col)
        else:
            return redirect("/stats")
    else:
        playername = request.args.get("player1")
        data.player_1_name = request.args.get("player1")
        data.game_type = request.args.get("gametype")
        if data.game_type == "Human":
            data.player_2_name  = request.args.get("player2")
        board = make_empty_board()
        data.board = board
        return render_template("play.html",playername = playername,board = board)

@app.route("/stats")
def stats():
    if data.winner == "O":
        winner_name = data.player_1_name
        output = "%s win the game"%winner_name
    elif data.winner == "X":
        winner_name = data.player_2_name
        output = "%s win the game"%winner_name
    else:
        output = "The game is Draw"
    return render_template("stats.html",winner = output,board = data.board)

def update_board(board,target_position,current_player):
    target_position_row = int(target_position[0])-1
    target_position_col = int(target_position[1])-1
    board[target_position_row][target_position_col] = current_player
    return board

def get_winner(Board):
    iswin = None
    if Board[0][0] == Board[1][1] == Board[2][2] or Board[0][2] == Board[1][1] == Board[2][0]:
        iswin = Board[1][1]
    else:
        for i in range(0,3):
            if Board[i][0] == Board[i][1] == Board[i][2]:
                iswin = Board[i][0]
                break
            elif Board[0][i] == Board[1][i] == Board[2][i]:
                iswin = Board[0][i]
                break
    return iswin

def game_state(winner,Board):
    iswin = winner
    if iswin == 'X' or iswin == 'O':
        return iswin
    elif (None in Board[0]) or (None in Board[1]) or (None in Board[2]):
        return None
    else:
        return 'Draw'

def other_player(player):
    if player == 'X':
        return 'O' 
    elif player == 'O':
        return 'X'




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
