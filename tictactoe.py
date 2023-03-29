import math
import copy
from  itertools import chain 

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Khoi tao trang thai khoi dong cua ban co.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):

    """
    Tra ve ai la nguoi choi tiep theo.
    """
    x_num = 0
    o_num = 0

    for i in range(len(board)):
        x_num += board[i].count(X)
        o_num += board[i].count(O)
    
    if x_num > o_num:
        return O
    else:
        return X
   
def actions(board):
    """
    Ham tra ve cac o trong duoi dang (i,j).
    """
    actions_list = set() #khoi tao ds cac o trong

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_list.add((i, j))

    return actions_list

def result(board, action):
    """
    Tra ve cai ban co sau khi di o o (i,j).
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Move not valid")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Ham tra ve ai la nguoi chien thang.
    """
    X_win = [X,X,X]
    O_win = [O,O,O]

    # win theo chieu ngang
    if X_win in (board[0], board[1], board[2]):
        return X
    if O_win in (board[0], board[1], board[2]):
        return O

    # win theo chieu doc
    if X_win in (([item[0] for item in board]),([item[1] for item in board]),([item[2] for item in board])):
        return X #moi lan duyet mot hang lay mot item theo cot 
    if O_win in (([item[0] for item in board]),([item[1] for item in board]),([item[2] for item in board])):
        return O

    # win theo chieuef xeo
    if X_win in (([board[0][0], board[1][1], board [2][2]]), ([board[0][2], board[1][1], board [2][0]])):
        return X
    if O_win in (([board[0][0], board[1][1], board [2][2]]), ([board[0][2], board[1][1], board [2][0]])):
        return O

    return None #everyone win or tie

def terminal(board):
    """
    Tra ve ket qua tro choi ket thuc hay chua ( true,fale).
    """
    if winner(board) != None:
        return True #co ng win thi ket thuc(true)
    
    if EMPTY not in chain(*board): #k co o trong thi tie(true)
        return True

    return False # k win k tie thi (false)

def utility(board):
    """
    Tra ve ket qua tran dau (10: x thang, -10: o thang,0:tie)
    """
    if winner(board) == X:
        return 10
    
    if winner(board) == O:
        return -10
    
    return 0

def minimax(board):
    """
    Tra ve vi tri toi uu nhat (i,j).
    """
    alpha = float('-inf')
    beta = float('inf')

    def maximizer(board): # vua so vua cat
        if terminal(board):
            return utility(board) # tra ve diem so ( vi du 0 10 -10)
        
        alpha = float('-inf')
        

        for action in actions(board): #duywt cac o rong
            alpha = max(alpha, minimizer(result(board, action))) #so - vo cung voi min
            if alpha > beta:
                break

        return alpha

    def minimizer(board):
        if terminal(board):# jet thuc hay chua, neu chua thi bo qua nhay xuong duoi
            return utility(board)# la thi tra gia tri no ( 10 or -10 or 0)
        
        # nhay toi day 
        beta = float('inf')

        for action in actions(board):# duyet o trong
            beta = min(beta, maximizer(result(board, action))) 
            if beta < alpha:
                break
            
        return beta

    if terminal(board):
        return None #neu tro choi da ket thuc k tra ve gi ca

    if player(board) == X: #10 la max
        alpha = maximizer(board)
        for action in actions(board):
            if alpha == minimizer(result(board, action)):
                return action            
                
    if player(board) == O: #-10 la min
        beta = minimizer(board) #kiem -10 neu kiem dc thi duyet o trong
        for action in actions(board): #duyet o trong
            if beta == maximizer(result(board, action)): #kiem tra xem max co la 10 hay k? neu la 10 thi bo qua o do else thi
                
                return action