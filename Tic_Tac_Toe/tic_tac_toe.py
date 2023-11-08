from tkinter import *
import random
import math

root = Tk()
root.title('Tic Tac Toe')
root.geometry('890x600')
BACKGROUND_COLOR = 'light grey'
FONT_COLOR = 'blue'
root.config(bg=BACKGROUND_COLOR)

def new_game(event=None):
    global turn
    l1 = Label(root, text='TIC TAC TOE', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '40'), bd=3, relief='solid',justify='center')
    l1.grid(row=0, column=0, columnspan=15,sticky=W+E)
    turn = True
    for i in boxes:
        for j in i:
            j.config(state='normal')
            j.delete(0,END)

def animation_of_button(event):
    #When the mouse hover over the button the button color and font changes
    if 'Enter' in str(event):
        b1.config(fg='black',relief='solid',bg='grey94')   
    else:
        b1.config(fg=FONT_COLOR,relief='raised',bg=BACKGROUND_COLOR)


def validate_input_entry(value):
    # check if the value is valid for the input in all the mode
    if value.upper() in ['X','O','']:
        return True
    else:
        return False

def input_validation_based_on_mode(value):
    # Check if the value is valid for a particular mode
    if mode.get() == 'PvP':
        if turn is True and value == 'X':
            pass
        elif turn is False and value == 'O':
            pass
        else:
            return False
    elif mode.get() in ['Computer Easy','Computer Hard']:
        if value != 'X':
            return False
        
    return True

def wining_condition(board):
    for i in range(0,9,3):
        if (board[i] == board[i+1] == board[i+2] ) and board[i] != '':
            return board[i]
    
    for i in range(0,3):
        if (board[i] == board[i+3] == board[i+6] ) and board[i] != '':
            return board[i]
    
    if (board[0] == board[4] == board[8] ) and board[4] != '':
            return board[4]
        
    if (board[2] == board[4] == board[6] ) and board[4] != '':
            return board[4]
        
    if '' not in board:
        return 'Tie'
    
    return False

def minimax(board,player):
    max_player = 'X'  
    other_player = 'O' if player == 'X' else 'X'
    num_empty_squares = len(['' for i in board if i==''])
    
    if wining_condition(board) == other_player:
        return {'position': None, 'score': 1 * (num_empty_squares + 1) if other_player == max_player else -1 * (
                    num_empty_squares + 1)}
    elif '' not in board:
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}  # each score should minimize
    else:
        best = {'position': None, 'score': math.inf}  # each score should maximize
    for position,possible_move in enumerate(board):
        if possible_move != '':
            continue
        board[position]= player
        sim_score = minimax(board, other_player)  # simulate a game after making that move

        # undo move
        board[position] = ''
        sim_score['position'] = position  # this represents the move optimal next move

        if player == max_player:  # X is max player
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best
            

def game_play(value,box):
    global l3,turn
    value_1 = value.char.upper()
    
    if not input_validation_based_on_mode(value_1):
        return None
    box.insert(0,value_1)
    box.config(state='disabled')
    
    # Changes the label to show which player/computer turn it is
    l3.destroy()
    text = players[mode.get()][turn]
    l3 = Label(root, text=text, fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '15'),justify='center')
    l3.grid(row=1, column=6,columnspan=4)
    
    if mode.get() == 'PvP':
        turn = not turn #changes player turn
        
    elif mode.get() =='Computer Easy':
        while True:
            num_of_empty_spaces_left = len(['' for i in boxes for j in i if j.get()==''])
            if num_of_empty_spaces_left==0:
                break           #No empty spaces is left,it is a tie
            rand = boxes[random.randint(0,2)][random.randint(0,2)]
            if rand.get() == '':
                rand.insert(0,"O")
                rand.config(state='disabled')
                break
    elif mode.get() =='Computer Hard':
        ans = minimax([j.get() for i in boxes for j in i],False)
        if ans['position'] is not None:
            box = boxes[ans['position']//3][ans['position']%3]
            box.insert(0,"O")
            box.config(state='disabled')
            
            
    win = wining_condition([j.get() for i in boxes for j in i])
    if win == 'Tie':
        for i in boxes:
            for j in i:
                j.config(state='disabled')
        l1 = Label(root, text=f"It's a Tie ", fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '40'), bd=3, relief='solid',justify='center')
        l1.grid(row=0, column=0, columnspan=15,sticky=W+E)
    elif win is not False:
        num = 0 if win == 'X' else 1
        l1 = Label(root, text=f'Congratulation {players[mode.get()][num]} won the game', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '40'), bd=3, relief='solid',justify='center')
        l1.grid(row=0, column=0, columnspan=15,sticky=W+E)


vcmd = (root.register(validate_input_entry), '%P')
boxes = []
players = {'PvP':('Player 1', 'Player 2'),"Computer Easy":('Player', 'Computer'),"Computer Hard":('Player', 'Computer')}
turn = True

l1 = Label(root, text='TIC TAC TOE', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '40'), bd=3, relief='solid',justify='center')
l1.grid(row=0, column=0, columnspan=15,sticky=W+E)

l2 = Label(root, text='Game Mode---->', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '12'), bd=3, relief='solid',justify='center')
l2.grid(row=1, column=0,columnspan=2)
mode = StringVar()
options_list = ["PvP", "Computer Easy", "Computer Hard"] 
mode.set('Computer Hard')
o1 = OptionMenu(root,mode,*options_list,command=new_game)
o1.grid(row=1,column=2,columnspan=3) 
o1.config(fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '10'), bd=3, relief='raised',justify='center',width=20)

l3 = Label(root, text='Player 1', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '15'),justify='center')
l3.grid(row=1, column=6,columnspan=4)

b1 = Button(root,text = 'NEW GAME',fg=FONT_COLOR,bg = BACKGROUND_COLOR,font= ('Times New Roman', '15'),command=new_game,width=15,relief='raised',justify='center')
b1.grid(row=1,column=11,columnspan=3) 
b1.bind('<Enter>',animation_of_button)
b1.bind('<Leave>',animation_of_button)


for i in range(2,18):
    if i in [2,7,12,17]:
        Label(root, text='-'*220, fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '8'), bd=3, relief='flat',justify='center').grid(row=i, column=0, columnspan=15,sticky=W+E)
        if i==17:
            break
        box__ = []
        for j in [0,5,10]:
            e1 = Entry(root, fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '50'), bd=3, relief='groove',width=5,justify='center',validate='key',validatecommand=vcmd)
            e1.grid(row=i+1, column=j,columnspan=5,rowspan=5)
            box__.append(e1)
            e1.bind('<Key>',lambda event,box=e1:game_play(event,box))
        boxes.append(box__)
    else:
        Label(root, text='|', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '15'), bd=3, relief='flat',justify='center').grid(row=i, column=5)
        Label(root, text='|', fg=FONT_COLOR, bg=BACKGROUND_COLOR ,font=('Times', '15'), bd=3, relief='flat',justify='center').grid(row=i, column=9)
    
mainloop()
