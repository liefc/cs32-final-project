import copy


class ChessBoard():
    '''
    Stores the board state of a chess game. This includes the positions of
        the pieces, the availability of en passant, and the availability of
        castling. Methods include:

    __init__() : Initializes variables that store the board state
    __str__() : Returns a string that when printed resembles a chess board
    
    in_check(player) : Returns True or False depending on whether the player
                        is in check
                        
    valid_move(player, piece, start, end) : Returns True or False depending on
                                            whether a move of the piece from
                                            start to end by the player is legal
                                            or not.
                                            
    move(player, piece, start, end) : If inputted move is valid, changes the
                                        board state to reflect the move and
                                        returns None. If the move is illegal,
                                        it returns the string "Illegal Move"
                                        
    castle(player, side) : If a castle by a player on the specified side is
                            legal, it edits the board state to reflect this
                            move and returns None. If it is illegal, it
                            returns the string "Illegal Move"
                            
    stalemate(player) : Returns True or False depending on whether the player
                        is stalemated
    '''
    def __init__(self):
        # Store state of the board as nested list, with a square being indexed
        # first by its rank (row) then by its file (column)
        self.state = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", ""],
                      ["", "", "", "", "", "", "", ""],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

        # Keep track of whether en passant is possible for some turn
        # and record the location of the vulnerable piece.
        # Gets reset when a move is made
        self.enpass = [False, (0, 0)]

        # Keep track of whether castling is legal for each color, on
        # the king's side and queen's side. Have the king and
        # rooks been moved or not. Gets changed when rooks and kings
        # make first move by move method
        self.w_castle = {'k': True, 'q': True}
        self.b_castle = {'k': True, 'q': True}

    def __str__(self):
        # Conversion to unicode for each chess piece
        piece_uni = {
            'bk': '\u2654',
            'bq': '\u2655',
            'br': '\u2656',
            'bb': '\u2657',
            'bn': '\u2658',
            'bp': '\u2659',
            'wk': '\u265a',
            'wq': '\u265b',
            'wr': '\u265c',
            'wb': '\u265d',
            'wn': '\u265e',
            'wp': '\u265f'
        }

        board = ""
        # Add each rank to the print statement at a time
        for rank in range(8):
            # Even ranks start with a white square on
            # the left (where the first rank is even)
            if rank % 2 == 0:
                board += '   ' + (("#" * 4 + " " * 4) * 4) + '\n'

                # Add labels
                board += f'{8 - rank}  '

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
                board += '   ' + (("#" * 4 + " " * 4) * 4) + '\n'
            # Same for odd ranks, just switch the hatching and the blank spaces
            else:
                board += "   " + (((" " * 4) + ("#") * 4) * 4) + '\n'

                # Add labels
                board += f'{8 - rank}  '

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
                board += '   ' + (((" " * 4) + ("#") * 4) * 4) + '\n'

        # add labels
        board += '\n    a   b   c   d   e   f   g   h'

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
        for x in range(loc[0] - 1, -1, -1):  # vary the rank
            # Check that test square is nonempty; if empty move on
            if self.state[x][loc[1]] != '':
                # Check if test square is a valid piece of opposite color
                if self.state[x][loc[1]][0] != player and self.state[x][
                        loc[1]][1] in ['q', 'r']:
                    return True
                break

        # Down:
        for x in range(loc[0] + 1, 8):  # vary the rank
            if self.state[x][loc[1]] != '':
                if self.state[x][loc[1]][0] != player and self.state[x][
                        loc[1]][1] in ['q', 'r']:
                    return True
                break

        # Left:
        for y in range(loc[1] - 1, -1, -1):  # vary the file
            if self.state[loc[0]][y] != '':
                if self.state[loc[0]][y][0] != player and self.state[
                        loc[0]][y][1] in ['q', 'r']:
                    return True
                break

        # Right:
        for y in range(loc[1] + 1, 8):  # vary the file
            if self.state[loc[0]][y] != '':
                if self.state[loc[0]][y][0] != player and self.state[
                        loc[0]][y][1] in ['q', 'r']:
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
                if check_piece[0] != player and check_piece[1] in ['q', 'b']:
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
                if check_piece[0] != player and check_piece[1] in ['q', 'b']:
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
                if check_piece[0] != player and check_piece[1] in ['q', 'b']:
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
                if check_piece[0] != player and check_piece[1] in ['q', 'b']:
                    return True
                break

        # Pawns:
        # Checking two potential squares
        if player == 'w':
            pawns = [(loc[0] - 1, loc[1] - 1), (loc[0] - 1, loc[1] + 1)]
        else:
            pawns = [(loc[0] + 1, loc[1] - 1), (loc[0] + 1, loc[1] + 1)]
        # Check if the squares are out of bounds
        for square in range(1, -1, -1):
            if (pawns[square][0] in [-1, 8]) or (pawns[square][1] in [-1, 8]):
                pawns.pop(square)
        # Check if any square contains an enemy pawn
        for square in pawns:
            check_piece = self.state[square[0]][square[1]]
            if check_piece != "":
                if check_piece[0] != player and check_piece[1] == 'p':
                    return True

        #Knights:
        knights = [
            (loc[0] + 2, loc[1] + 1),  # check 8 potential squares
            (loc[0] + 2, loc[1] - 1),
            (loc[0] - 2, loc[1] + 1),
            (loc[0] - 2, loc[1] - 1),
            (loc[0] + 1, loc[1] + 2),
            (loc[0] - 1, loc[1] + 2),
            (loc[0] + 1, loc[1] - 2),
            (loc[0] - 1, loc[1] - 2)
        ]
        # Check squares in bounds
        for square in range(7, -1, -1):
            if (knights[square][0] in [-2, -1, 8, 9]) or (knights[square][1]
                                                          in [-2, -1, 8, 9]):
                knights.pop(square)
        # Check if squares contain enemy knights
        for square in knights:
            check_piece = self.state[square[0]][square[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] == 'n':
                    return True

        # King (used when checking valid moves for kings)
        kings = [
            (loc[0] - 1, loc[1] - 1),  # check 8 potential squares
            (loc[0] - 1, loc[1]),
            (loc[0] - 1, loc[1] + 1),
            (loc[0], loc[1] - 1),
            (loc[0], loc[1] + 1),
            (loc[0] + 1, loc[1] - 1),
            (loc[0] + 1, loc[1]),
            (loc[0] + 1, loc[1] + 1)
        ]
        # Check squares in bounds
        for square in range(7, -1, -1):
            if (kings[square][0] in [-1, 8]) or (kings[square][1] in [-1, 8]):
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
        copy_board = copy.deepcopy(self)
        copy_board.state[end[0]][end[1]] = f"{player}{piece}"
        copy_board.state[start[0]][start[1]] = ""
        # Check if hypothetical boardstate places player in check
        if copy_board.in_check(player) == True:
            return False

        # Check if target square can be targeted by piece
        if piece == 'q':  # queens
            # Check whether the target square is on the same
            # rank, file, or diagonal as the queen
            if start[0] == end[0]:  # same rank
                # Check which direction the target square is
                if start[1] > end[1]:  # left
                    # Incriment in direction of the target square
                    # until find a piece or target square
                    square = start
                    while True:
                        square = (square[0], square[1] - 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else:  # right
                    square = start
                    while True:
                        square = (square[0], square[1] + 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            elif start[1] == end[1]:  # same file
                if start[0] > end[0]:  # up
                    square = start
                    while True:
                        square = (square[0] - 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else:  # down
                    square = start
                    while True:
                        square = (square[0] + 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            elif abs(start[0] - end[0]) == abs(start[1] - end[1]):  # diagonal
                # Check whether target square is up or down
                if start[0] > end[0]:  # up
                    # Check whether target square is left or right
                    if start[1] > end[1]:  # left
                        # Incriment in direction of the target square
                        # until find a piece or target square
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else:  # right
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                else:  # down
                    if start[1] > end[1]:  # left
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else:  # right
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
            else:
                return False  # target square not on rank, file, or diagonals
        elif piece == 'r':  # rooks
            # Same exact check as the queens, but only for files and ranks
            if start[0] == end[0]:  # same rank
                if start[1] > end[1]:  # left
                    square = start
                    while True:
                        square = (square[0], square[1] - 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else:  # right
                    square = start
                    while True:
                        square = (square[0], square[1] + 1)
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            elif start[1] == end[1]:  # same file
                if start[0] > end[0]:  # up
                    square = start
                    while True:
                        square = (square[0] - 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
                else:  # down
                    square = start
                    while True:
                        square = (square[0] + 1, square[1])
                        if square == end:
                            return True
                        elif self.state[square[0]][square[1]] != '':
                            return False
            else:
                return False  # target square not on rank or file
        elif piece == 'b':  # bishops
            # Same check as queens, but only for diagonals
            if abs(start[0] - end[0]) == abs(start[1] - end[1]):  # diagonal
                if start[0] > end[0]:  # up
                    if start[1] > end[1]:  # left
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else:  # right
                        square = start
                        while True:
                            square = (square[0] - 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                else:  # down
                    if start[1] > end[1]:  # left
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] - 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
                    else:  # right
                        square = start
                        while True:
                            square = (square[0] + 1, square[1] + 1)
                            if square == end:
                                return True
                            elif self.state[square[0]][square[1]] != '':
                                return False
            else:
                return False  # target square not on diagonals
        elif piece == 'n':  # knights
            # Check whether target square in the list of 8 possible
            # positions for the knight
            knights = [
                (start[0] + 2, start[1] + 1),  # check 8 potential squares
                (start[0] + 2, start[1] - 1),
                (start[0] - 2, start[1] + 1),
                (start[0] - 2, start[1] - 1),
                (start[0] + 1, start[1] + 2),
                (start[0] - 1, start[1] + 2),
                (start[0] + 1, start[1] - 2),
                (start[0] - 1, start[1] - 2)
            ]
            if end in knights:
                return True
            else:
                return False
        elif piece == 'k':  # kings
            # Check whether target square in the list of 8 possible
            # positions for the king
            kings = [
                (start[0] - 1, start[1] - 1),  # check 8 potential squares
                (start[0] - 1, start[1]),
                (start[0] - 1, start[1] + 1),
                (start[0], start[1] - 1),
                (start[0], start[1] + 1),
                (start[0] + 1, start[1] - 1),
                (start[0] + 1, start[1]),
                (start[0] + 1, start[1] + 1)
            ]
            if end in kings:
                return True
            else:
                return False
        else:  # pawns
            # Have to check for each color: whether there is a piece in front
            # of the pawn, whether there are enemy pieces to the sides that
            # can be captured, whether en passant is possible, whether the pawn
            # is on its home rank.
            if player == 'w':
                # Forward move (not attacking):
                if start[1] == end[1]:
                    # Check space in front is clear:
                    if self.state[start[0] - 1][start[1]] == '':
                        if start[0] - end[0] == 1:  # move one space forward
                            return True
                        elif start[0] - end[0] == 2:  # move two spaces
                            # Check space two in front is clear
                            if self.state[end[0]][end[1]] == '':
                                return True
                            else:
                                return False  # piece is two in front of pawn
                        else:
                            return False  # move is not in forward two spaces
                    else:
                        return False  # not open for pawn to move forward
                # Attacking move:
                elif end in [(start[0] - 1, start[1] - 1),
                             (start[0] - 1, start[1] + 1)]:
                    # Check that opponent's piece occupies target square
                    if self.state[end[0]][end[1]] != '':
                        if self.state[end[0]][end[1]][0] == 'b':
                            return True
                    # Check en passant is possible and is being used
                    elif self.enpass == [True, (end[0] + 1, end[1])]:
                        return True
                    else:
                        return False  # no piece to attack
                else:
                    return False  # target square not valid
            else:  # black
                # Same checks as for white, just in reverse direction
                # Forward move (not attacking):
                if start[1] == end[1]:
                    if self.state[start[0] + 1][start[1]] == '':
                        if start[0] - end[0] == -1:  # move one space forward
                            return True
                        elif start[0] - end[0] == -2:  # move two spaces
                            if self.state[end[0]][end[1]] == '':
                                return True
                            else:
                                return False  # piece is two in front of pawn
                        else:
                            return False  # move is not in forward two spaces
                    else:
                        return False  # not open for pawn to move forward
                # Attacking move:
                elif end in [(start[0] + 1, start[1] - 1),
                             (start[0] + 1, start[1] + 1)]:
                    if self.state[end[0]][end[1]] != '':
                        if self.state[end[0]][end[1]][0] == 'w':
                            return True
                    elif self.enpass == [True, (end[0] - 1, end[1])]:
                        return True
                    else:
                        return False  # no piece to attack
                else:
                    return False  # target square not valid

    def move(self, player, piece, start, end):
        '''
        Updates the board state for a specified move of a piece from start
        to end. Keeps the castling tracker up to date as well as the en passant
        tracker. Returns "Illegal Move" if move is not valid and returns None
        if move is valid. Castling is done with different function.
        '''
        # Check if move is valid and change the board state if so
        if self.valid_move(player, piece, start, end) == True:
            # Change board state
            self.state[start[0]][start[1]] = ''
            self.state[end[0]][end[1]] = f"{player}{piece}"

            # Remove piece if en passant is used
            if self.enpass[0] == True:
                if piece == 'p':
                    if player == 'w':
                        if (end[0] + 1, end[1]) == self.enpass[1]:
                            self.state[self.enpass[1][0]][self.enpass[1]
                                                          [1]] = ''
                    else:
                        if (end[0] - 1, end[1]) == self.enpass[1]:
                            self.state[self.enpass[1][0]][self.enpass[1]
                                                          [1]] = ''

            # Change castling tracker if necessary
            if piece == 'k':
                if player == 'w':
                    self.w_castle['k'] = False
                    self.w_castle['q'] = False
                else:
                    self.b_castle['k'] = False
                    self.b_castle['q'] = False
            elif piece == 'r':
                if player == 'w':
                    if start == (7, 0):
                        self.w_castle['q'] = False
                    elif start == (7, 7):
                        self.w_castle['k'] = False
                else:
                    if start == (0, 0):
                        self.b_castle['q'] = False
                    elif start == (0, 7):
                        self.b_castle['k'] = False

            # Reset en passant
            self.enpass = [False, (0, 0)]
            if piece == 'p':
                if player == 'w':
                    if start[0] == 6 and end[0] == 4:
                        self.enpass = [True, end]
                else:
                    if start[0] == 1 and end[0] == 3:
                        self.enpass = [True, end]

            return None
        else:
            return "Illegal Move"

    def castle(self, player, side):
        '''
        Performs castling on a specified side for a specified player. If
        castling is not possible, returns "Illegal Move". Returns None if
        possible. Keeps en passant and castling trackers updated.
        '''
        if self.in_check(player) == False:  # king not in check
            if player == 'w':  # white castle
                if self.w_castle[side] == True:  # rook and king have not moved
                    if side == 'k':  # kingside white castle
                        # Check that squares between rook and king are empty
                        if self.state[7][5] != '' or self.state[7][6] != '':
                            return "Illegal Move"

                        # Check that king is not moving through a check by
                        # creating hypothetical boards and checking for checks
                        copy_board = copy.deepcopy(self)
                        copy_board.state[7][4] = ''
                        copy_board.state[7][5] = 'wk'
                        if copy_board.in_check('w') == True:
                            return "Illegal Move"
                        copy_board.state[7][5] = ''
                        copy_board.state[7][6] = 'wk'
                        if copy_board.in_check('w') == True:
                            return "Illegal Move"

                        # Move the king and rook
                        self.state[7][4] = ''
                        self.state[7][5] = 'wr'
                        self.state[7][6] = 'wk'
                        self.state[7][7] = ''

                        # Update en passant tracker
                        self.enpass = [False, (0, 0)]

                        # Update castling tracker
                        self.w_castle['k'] = False
                        self.b_castle['q'] = False

                        return None
                    else:  # queenside white castle
                        # Same checks as above
                        if (self.state[7][1] != '' or self.state[7][2] != ''
                                or self.state[7][3] != ''):
                            return "Illegal Move"

                        copy_board = copy.deepcopy(self)
                        copy_board.state[7][4] = ''
                        copy_board.state[7][3] = 'wk'
                        if copy_board.in_check('w') == True:
                            return "Illegal Move"
                        copy_board.state[7][3] = ''
                        copy_board.state[7][2] = 'wk'
                        if copy_board.in_check('w') == True:
                            return "Illegal Move"

                        # Move the king and rook
                        self.state[7][0] = ''
                        self.state[7][2] = 'wk'
                        self.state[7][3] = 'wr'
                        self.state[7][4] = ''

                        # Update en passant tracker
                        self.enpass = [False, (0, 0)]

                        # Update castling tracker
                        self.w_castle['k'] = False
                        self.b_castle['q'] = False

                        return None
            else:  # black castle
                if self.b_castle[side] == True:  # rook and king have not moved
                    if side == 'k':  # kingside black castle
                        # Same checks as above
                        if self.state[0][5] != '' or self.state[0][6] != '':
                            return "Illegal Move"

                        copy_board = copy.deepcopy(self)
                        copy_board.state[0][4] = ''
                        copy_board.state[0][5] = 'bk'
                        if copy_board.in_check('b') == True:
                            return "Illegal Move"
                        copy_board.state[0][5] = ''
                        copy_board.state[0][6] = 'bk'
                        if copy_board.in_check('b') == True:
                            return "Illegal Move"

                        # Move the king and rook
                        self.state[0][4] = ''
                        self.state[0][5] = 'br'
                        self.state[0][6] = 'bk'
                        self.state[0][7] = ''

                        # Update en passant tracker
                        self.enpass = [False, (0, 0)]

                        # Update castling tracker
                        self.w_castle['k'] = False
                        self.b_castle['q'] = False

                        return None
                    else:  # queenside black castle
                        # Same checks as above
                        if (self.state[0][1] != '' or self.state[0][2] != ''
                                or self.state[0][3] != ''):
                            return "Illegal Move"

                        copy_board = copy.deepcopy(self)
                        copy_board.state[0][4] = ''
                        copy_board.state[0][3] = 'bk'
                        if copy_board.in_check('b') == True:
                            return "Illegal Move"
                        copy_board.state[0][3] = ''
                        copy_board.state[0][2] = 'bk'
                        if copy_board.in_check('b') == True:
                            return "Illegal Move"

                        # Move the king and rook
                        self.state[0][0] = ''
                        self.state[0][2] = 'bk'
                        self.state[0][3] = 'br'
                        self.state[0][4] = ''

                        # Update en passant tracker
                        self.enpass = [False, (0, 0)]

                        # Update castling tracker
                        self.w_castle['k'] = False
                        self.b_castle['q'] = False

                        return None

        return "Illegal Move"

    def stalemate(self, player):
        '''
        Checks whether a player has no viable moves. Returns False
        if there are viable moves, returns True if there are no moves.
        '''
        # Loop through all the pieces on the board and at every piece,
        # check if there are any possible moves available to that piece.
        # (Note castling is not possible if the king cannot move, so we
        # don't need to check for that)
        for r1 in range(8):
            for f1 in range(8):
                square = self.state[r1][f1]  # loop through all squares
                if square != '':
                    if square[0] == player:
                        piece = square[1]  # check all of player's pieces
                        for r2 in range(8):
                            for f2 in range(8):
                                # Check if piece can be moved anywhere on board
                                if self.valid_move(player, piece, (r1, f1),
                                                   (r2, f2)):
                                    return False
        return True


def main():
    '''
    Runs a chess game that operates through user input in the console. The
    board is printed in the console. There is full functionality except for
    draw by repetition of position (but this can be done by players offering
    draws). main() is built on the ChessBoard class. The board state is stored
    in the ChessBoard class as well as functions for editing the board state,
    printing the board state, checking for valid moves, and checking for
    stalemate. Pawn promotion is the only feature primarily executed in the
    main() function because it is heavily reliant on user input and editing the
    board state is only one line of code.
    '''

    # Initialize game
    print("Welcome to Chess!\n")
    board = ChessBoard()
    print(board)
    print()

    help = f"Enter a location of a piece in the form 'c4'.\nTo castle, enter 'castle'. To resign, enter 'resign'. To offer a draw, enter 'draw'.\nType 'help' to review the options.\n"
    print(help)

    player = 'w'
    while True:
        # Have variables for the full word and the notation
        if player == 'w':
            turn = 'white'
        else:
            turn = 'black'

        # Take input
        print()
        start = input(
            f"It's {turn}'s turn! Enter the location of a piece to move: ")
        start = start.strip().lower()

        # Check if input is valid
        while (start not in ['resign', 'draw', 'castle']) or start == 'help':
            # Check for valid regular move
            if len(start) == 2:
                if (start[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and
                        start[1] in ['1', '2', '3', '4', '5', '6', '7', '8']):
                    break

            print()
            print(help)
            start = input(
                f"It's {turn}'s turn! Enter the location of a piece to move: ")
            start = start.strip().lower()

        # Parse the inputs
        print()
        if start == 'resign':  # resignation by player
            if player == 'w':
                print('White resigns. Black wins!')
                break
            else:
                print('Black resigns. White wins!')
                break
        elif start == 'draw':  # offer of a draw
            # Grab input for accepting the draw
            draw = input(
                f"{turn.capitalize()} offers a draw. Do you accept? [y/n]: ")
            draw = draw.strip().lower()

            # Check valid input
            while draw not in ['y', 'n']:
                print()
                print("Please enter either 'y' or 'n'.")
                draw = input(
                    f"{turn.capitalize()} offers a draw. Do you accept? [y/n]: "
                )
                draw = draw.strip().lower()

            # End game if accepted
            if draw == 'y':
                print()
                print("The game is a draw.")
                break
            else:
                pass
        elif start == 'castle':  # player attempts to castle
            # Grab input for which side to castle on
            side = input("Which side to castle on? [king/queen]: ")
            side = side.strip().lower()

            # Check valid input
            while side not in ['king', 'queen']:
                print()
                print("Please enter either 'king' or 'queen'.")
                side = input("Which side to castle on? [king/queen]: ")
                side = side.strip().lower()

            # Convert to notation
            if side == 'king':
                side = 'k'
            else:
                side = 'q'

            # Attempt to castle
            castle = board.castle(player, side)
            if castle == 'Illegal Move':  # illegal -> loop through turn again
                print()
                print("Illegal move. Please try again.")
            else:  # succeeds
                print()
                print(board)

                # Switch players for next turn
                if player == 'w':
                    player = 'b'
                else:
                    player = 'w'

                # Check if position is now stalemate for the next player
                if board.stalemate(player):
                    if board.in_check(player):  # stalemate + check = checkmate
                        print()
                        print(f"Checkmate! {turn.capitalize()} wins!")
                        break
                    else:
                        print()
                        print("Stalemate! The game is a draw!")
                        break

                # Check if the next player is now in check and alert them if so
                if board.in_check(player):
                    if player == 'w':
                        print()
                        print("White is in check!")
                    else:
                        print()
                        print("Black is in check!")
        else:  # player attempts a regular move
            # Convert locations to index notation
            letter_to_num = {
                'a': 0,
                'b': 1,
                'c': 2,
                'd': 3,
                'e': 4,
                'f': 5,
                'g': 6,
                'h': 7,
            }
            start = (8 - int(start[1]), letter_to_num[start[0]])

            # Find piece at start location, check if it is player's piece
            if board.state[start[0]][start[1]] != '':
                if board.state[start[0]][start[1]][0] == player:
                    # Find piece at start location
                    piece = board.state[start[0]][start[1]][1]

                    # Get end location of piece
                    end = input("Enter the location of where to move it: ")
                    end = end.strip().lower()

                    # Check if input valid
                    while True:
                        if len(end) == 2:
                            if (end[0] in [
                                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
                            ] and end[1] in [
                                    '1', '2', '3', '4', '5', '6', '7', '8'
                            ]):
                                break
                        print()
                        end = input(
                            "Please enter a location in the form 'c4': ")
                        end = end.strip().lower()

                    # Convert to notation
                    end = (8 - int(end[1]), letter_to_num[end[0]])

                    # Attempt to move the piece
                    move = board.move(player, piece, start, end)
                    if move == "Illegal Move":  # illegal -> loop through turn
                        print()
                        print("Illegal move. Please try again.")
                    else:  # succeeds
                        print()
                        print(board)

                        # Pawn promotion
                        if piece == 'p':
                            if ((player == 'w' and end[0] == 0)
                                    or (player == 'b' and end[0] == 7)):
                                # Get input
                                print()
                                promote = input(
                                    "Promote the pawn [queen/rook/bishop/knight]: "
                                )
                                promote = promote.strip().lower()

                                # Check if input is valid
                                while promote not in [
                                        'queen', 'rook', 'bishop', 'knight'
                                ]:
                                    print()
                                    promote = input(
                                        "Please enter either 'queen', 'rook', 'bishop', or 'knight': "
                                    )
                                    promote = promote.strip().lower()

                                # Convert to notation
                                if promote == 'queen':
                                    promote = 'q'
                                elif promote == 'bishop':
                                    promote = 'b'
                                elif promote == 'rook':
                                    promote = 'r'
                                else:
                                    promote = 'n'

                                # Change board to reflect the promotion
                                board.state[end[0]][
                                    end[1]] = f'{player}{promote}'
                                print()
                                print(board)

                        # Change players for next turn
                        if player == 'w':
                            player = 'b'
                        else:
                            player = 'w'

                        # Check if new player now in stalemate
                        if board.stalemate(player):
                            if board.in_check(player):  # checkmate
                                print()
                                print(f"Checkmate! {turn.capitalize()} wins!")
                                break
                            else:
                                print()
                                print("Stalemate! The game is a draw!")
                                break

                        # New player now in check
                        if board.in_check(player):
                            if player == 'w':
                                print()
                                print("White is in check!")
                            else:
                                print()
                                print("Black is in check!")
                else: # player's piece not on square, loop through turn again
                    print(
                        "You don't have a piece on this square. Please try again.")
            else:  # if player's piece not on square, loop through turn again
                print(
                    "You don't have a piece on this square. Please try again.")


if __name__ == "__main__":
    main()
