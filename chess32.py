import copy

class ChessBoard():
    def __init__(self):
        # Store state of the board as nested list, with a square being indexed
        # first by its rank then by its file (column)
        self.state = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
            ]
        
        # Keep track of whether en passant is possible for some turn
        # and record the location of the vulnerable piece.
        # THIS SHOULD GET RESET AT THE END OF EVERY TURN
        self.enpass = [False, (0,0)]

    def __str__(self):
        # Conversion to unicode for each chess piece
        piece_uni = {
            'wk': '\u2654',
            'wq': '\u2655',
            'wr': '\u2656',
            'wb': '\u2657',
            'wn': '\u2658',
            'wp': '\u2659',
            'bk': '\u265a',
            'bq': '\u265b',
            'br': '\u265c',
            'bb': '\u265d',
            'bn': '\u265e',
            'bp': '\u265f'
            }

        board = ""
        # Add each rank to the print statement at a time
        for rank in range(8):
            # Even ranks start with a white square on
            # the left (where the first rank is even)
            if rank % 2 == 0:
                board += (("#"*4 + " " *4)*4) + '\n'
                # Add each square at a time
                for file in range(8):
                    # If square empty, add empty spaces
                    if self.state[rank][file] == '':
                        if file % 2 == 0:
                            board += '#' * 4
                        else:
                            board += ' ' * 4
                    # If square occupied, add the unicode value for a piece
                    # in the print statement
                    else:
                        if file % 2 == 0:
                            board += f"#{piece_uni[self.state[rank][file]]} #"
                        else:
                            board += f" {piece_uni[self.state[rank][file]]}  "
                board += '\n'
                board += (("#"*4 + " " *4)*4) + '\n'
            # Same for odd ranks, just switch the hatching and the blank spaces
            else:
                board += (((" "*4) + ("#")*4)*4) + '\n'
                for file in range(8):
                    if self.state[rank][file] == '':
                        if file % 2 == 0:
                            board += ' ' * 4
                        else:
                            board += '#' * 4
                    else:
                        if file % 2 == 0:
                            board += f" {piece_uni[self.state[rank][file]]}  "
                        else:
                            board += f"#{piece_uni[self.state[rank][file]]} #"
                board += '\n'
                board += (((" "*4) + ("#")*4)*4) + '\n'
            
        return board

    def in_check(self, player):
        '''
        Checks whether a given player is in check (returns True)
        or not (returns False). Used to determine whether moves are
        valid and when determining checkmate.
        '''
        # Find location of king
        for rank in range(8):
            if f'{player}k' in self.state[rank]:
                # Store as a touple with location = (rank, file)
                loc = (rank, self.state[rank].index(f'{player}k'))

        # Check in each direction if there is a piece that can hit the king
        # Up:
        for x in range(loc[0]-1, -1, -1): # vary the rank
            # Check that test square is nonempty; if empty move on
            if self.state[x][loc[1]] != '':
                # Check if test square is a valid piece of opposite color
                if self.state[x][loc[1]][0] != player and self.state[x][loc[1]][1] in ['q','r']:
                    return True
                break
        
        # Down:
        for x in range(loc[0]+1, 8): # vary the rank
            if self.state[x][loc[1]] != '':
                if self.state[x][loc[1]][0] != player and self.state[x][loc[1]][1] in ['q','r']:
                    return True
                break
        
        # Left:
        for y in range(loc[1]-1, -1, -1): # vary the file
            if self.state[loc[0]][y] != '':
                if self.state[loc[0]][y][0] != player and self.state[loc[0]][y][1] in ['q','r']:
                    return True
                break
        
        # Right:
        for y in range(loc[1]+1, 8): # vary the file
            if self.state[loc[0]][y] != '':
                if self.state[loc[0]][y][0] != player and self.state[loc[0]][y][1] in ['q','r']:
                    return True
                break
        
        # Right Down Diagonal
        check_loc = loc
        while True:
            # Incriment in diagonal direction
            check_loc = (check_loc[0] + 1, check_loc[1] + 1)
            # Check if the square is out of bounds
            if check_loc[0] == 8 or check_loc[1] == 8:
                break
            # Grab value of square
            check_piece = self.state[check_loc[0]][check_loc[1]]
            # Same check as above directions
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break
        
        # Left Down Diagonal
        check_loc = loc
        while True:
            check_loc = (check_loc[0] + 1, check_loc[1] - 1)
            if check_loc[0] == 8 or check_loc[1] == -1:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break

        # Right Up Diagonal
        check_loc = loc
        while True:
            check_loc = (check_loc[0] - 1, check_loc[1] + 1)
            if check_loc[0] == -1 or check_loc[1] == 8:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break
        
        # Left Up Diagonal
        check_loc = loc
        while True:
            check_loc = (check_loc[0] - 1, check_loc[1] - 1)
            if check_loc[0] == -1 or check_loc[1] == -1:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break

        # Pawns:
        # Checking two potential squares
        if player == 'w':
            pawns = [(loc[0] -1, loc[1] -1), (loc[0] -1, loc[1] +1)]
        else:
            pawns = [(loc[0] +1, loc[1] -1), (loc[0] + 1, loc[1] + 1)]
        # Check if the squares are out of bounds
        for square in range(1, -1, -1):
            if (pawns[square][0] in [-1,8]) or (pawns[square][1] in [-1,8]):
                pawns.pop(square)
        # Check if any square contains an enemy pawn
        for square in pawns:
            check_piece = self.state[square[0]][square[1]]
            if check_piece != "":
                if check_piece[0] != player and check_piece[1] == 'p':
                    return True
            
        #Knights:
        knights = [(loc[0] +2, loc[1] +1), # check 8 potential squares
                   (loc[0] +2, loc[1] -1),
                   (loc[0] -2, loc[1] +1),
                   (loc[0] -2, loc[1] -1),
                   (loc[0] +1, loc[1] +2),
                   (loc[0] -1, loc[1] +2),
                   (loc[0] +1, loc[1] -2),
                   (loc[0] -1, loc[1] -2)
                   ]
        # Check squares in bounds
        for square in range(7, -1, -1):
            if (knights[square][0] in [-2,-1,8,9]) or (knights[square][1] in [-2,-1,8,9]):
                knights.pop(square)
        # Check if squares contain enemy knights
        for square in knights:
            check_piece = self.state[square[0]][square[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] == 'n':
                    return True

        # King (used when checking valid moves for kings)
        kings = [(loc[0] -1, loc[1] -1), # check 8 potential squares
                (loc[0] -1, loc[1]),
                (loc[0] -1, loc[1] +1),
                (loc[0], loc[1] -1),
                (loc[0], loc[1] +1),
                (loc[0] +1, loc[1] -1),
                (loc[0] +1, loc[1]),
                (loc[0] +1, loc[1] +1)
                ]
        # Check squares in bounds
        for square in range(7, -1, -1):
            if (kings[square][0] in [-1,8]) or (kings[square][1] in [-1,8]):
                kings.pop(square)
        # Check if squares contain enemy king
        for square in kings:
            check_piece = self.state[square[0]][square[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] == 'k':
                    return True

        # If piece not in check, return false
        return False

    def valid_move(self, player, piece, start, end):
        '''
        Checks whether a specified move from start to end by piece
        is valid (returns True) or not (returns False). Used by the
        move method and when checking for stalemate/checkmate
        '''
        # Check if the target square is occupied by own piece
        if self.state[end[0]][end[1]] != '':
            if self.state[end[0]][end[1]][0] == player:
                return False

        # Check whether move would place the player in check.
        # Move piece to new loc on hypothetical board
        copy_board = ChessBoard()
        copy_board.state = copy.deepcopy(self.state)
        copy_board.state[end[0]][end[1]] = f"{player}{piece}"
        copy_board.state[start[0]][start[1]] = ""
        # Check if hypothetical boardstate places player in check
        if copy_board.in_check(player) == True:
            return False

        # Check if target square can be targeted by piece
        if piece == 'q': # queens
            # Check whether the target square is on the same
            # rank, file, or diagonal as the queen
            if start[0] == end[0]: # same rank
                # Check which direction the target square is
                if start[1] > end[1]: # left
                    # Incriment in direction of the target square
                    # until find a piece or target square
                    square = start
                    while True:
                        square = (square[0], square[1] - 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else: # right
                    square = start
                    while True:
                        square = (square[0], square[1] + 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            elif start[1] == end[1]: # same file
                if start[0] > end[0]: # up
                    square = start
                    while True:
                        square = (square[0] - 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else: # down
                    square = start
                    while True:
                        square = (square[0] + 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            elif abs(start[0] - end[0]) == abs(start[1] - end[1]): # diagonal
                # Check whether target square is up or down
                if start[0] > end[0]: # up
                    # Check whether target square is left or right
                    if start[1] > end[1]: # left
                        # Incriment in direction of the target square
                        # until find a piece or target square
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else: # right
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                else: # down
                    if start[1] > end[1]: # left
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else: # right
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
            else:
                return False # target square not on rank, file, or diagonals            
        elif piece == 'r': # rooks
            # Same exact check as the queens, but only for files and ranks
            if start[0] == end[0]: # same rank
                if start[1] > end[1]: # left
                    square = start
                    while True:
                        square = (square[0], square[1] - 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else: # right
                    square = start
                    while True:
                        square = (square[0], square[1] + 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            elif start[1] == end[1]: # same file
                if start[0] > end[0]: # up
                    square = start
                    while True:
                        square = (square[0] - 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else: # down
                    square = start
                    while True:
                        square = (square[0] + 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            else:
                return False # target square not on rank or file
        elif piece == 'b': # bishops
            # Same check as queens, but only for diagonals
            if abs(start[0] - end[0]) == abs(start[1] - end[1]): # diagonal
                if start[0] > end[0]: # up
                    if start[1] > end[1]: # left
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else: # right
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                else: # down
                    if start[1] > end[1]: # left
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else: # right
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
            else:
                return False # target square not on diagonals
        elif piece == 'n': # knights
            # Check whether target square in the list of 8 possible
            # positions for the knight
            knights = [(start[0] +2, start[1] +1), # check 8 potential squares
                       (start[0] +2, start[1] -1),
                       (start[0] -2, start[1] +1),
                       (start[0] -2, start[1] -1),
                       (start[0] +1, start[1] +2),
                       (start[0] -1, start[1] +2),
                       (start[0] +1, start[1] -2),
                       (start[0] -1, start[1] -2)]
            if end in knights:
                return True
            else:
                return False
        elif piece == 'k': # kings
            # Check whether target square in the list of 8 possible
            # positions for the king
            kings = [(start[0] -1, start[1] -1), # check 8 potential squares
                     (start[0] -1, start[1]),
                     (start[0] -1, start[1] +1),
                     (start[0], start[1] -1),
                     (start[0], start[1] +1),
                     (start[0] +1, start[1] -1),
                     (start[0] +1, start[1]),
                     (start[0] +1, start[1] +1)]
            if end in kings:
                return True
            else:
                return False
        else: # pawns
            # Have to check for each color: whether there is a piece in front
            # of the pawn, whether there are enemy pieces to the sides that
            # can be captured, whether en passant is possible, whether the pawn
            # is on its home rank.
            if player == 'w':
                # Forward move (not attacking):
                if start[1] == end[1]:
                    # Check space in front is clear:
                    if self.state[start[0] - 1][start[1]] == '':
                        if start[0] - end[0] == 1: # move one space forward
                            return True
                        elif start[0] - end[0] == 2: # move two spaces
                            # Check space two in front is clear
                            if self.state[end[0]][end[1]] == '':
                                return True
                            else:
                                return False # piece is two in front of pawn
                        else:
                            return False # move is not in forward two spaces
                    else:
                        return False # not open for pawn to move forward
                # Attacking move:
                elif end in [(start[0] - 1, start[1] - 1), (start[0] - 1, start[1] + 1)]:
                    # Check that opponent's piece occupies target square
                    if self.state[end[0]][end[1]] != '':
                        if self.state[end[0]][end[1]][0] == 'b':
                            return True
                    # Check en passant is possible and is being used
                    elif self.enpass == [True, (end[0] + 1, end[1])]:
                        return True
                    else:
                        return False # no piece to attack
                else:
                    return False # target square not valid
            else: # black
                # Same checks as for white, just in reverse direction
                # Forward move (not attacking):
                if start[1] == end[1]:
                    if self.state[start[0] + 1][start[1]] == '':
                        if start[0] - end[0] == -1: # move one space forward
                            return True
                        elif start[0] - end[0] == -2: # move two spaces
                            if self.state[end[0]][end[1]] == '':
                                return True
                            else:
                                return False # piece is two in front of pawn
                        else:
                            return False # move is not in forward two spaces
                    else:
                        return False # not open for pawn to move forward
                # Attacking move:
                elif end in [(start[0] + 1, start[1] - 1), (start[0] + 1, start[1] + 1)]:
                    if self.state[end[0]][end[1]] != '':
                        if self.state[end[0]][end[1]][0] == 'w':
                            return True
                    elif self.enpass == [True, (end[0] - 1, end[1])]:
                        return True
                    else:
                        return False # no piece to attack
                else:
                    return False # target square not valid
                    
    def move(self, start, end, piece='wp'):
        # Check if move is valid and change the board state if so
        if self.valid_move(piece[0], piece[1], start, end) == True:
            self.state[start[0]][start[1]] = ''
            self.state[end[0]][end[1]] = piece
            return None
        else:
            return "Invalid Move"

    def stalemate(self, player):
        # Loop through all the pieces on the board and at every piece,
        # check if there are any possible moves available to that piece.
        for r1 in range(8):
            for f1 in range(8):
                square = self.state[r1][f1]
                if square != '':
                    if square[0] == player:
                        piece = square[1]
                        for r2 in range(8):
                            for f2 in range(8):
                                if self.valid_move(player, piece, (r1,f1), (r2,f2)):
                                    return False
        return True
        

def main():
    board = ChessBoard()

if __name__ == "__main__":
    main()
