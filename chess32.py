class ChessBoard():
    def __init__(self):
        self.pieces = []
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

    def __str__(self):
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
        for rank in range(8):
            if rank % 2 == 0:
                board += ((" "*4 + "#" *4)*4) + '\n'
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
                board += ((" "*4 + "#" *4)*4) + '\n'
            else:
                board += ((("#"*4) + (" ")*4)*4) + '\n'
                for file in range(8):
                    if self.state[rank][file] == '':
                        if file % 2 == 0:
                            board += '#' * 4
                        else:
                            board += ' ' * 4
                    else:
                        if file % 2 == 0:
                            board += f"#{piece_uni[self.state[rank][file]]} #"
                        else:
                            board += f" {piece_uni[self.state[rank][file]]}  "
                board += '\n'
                board += ((("#"*4) + (" ")*4)*4) + '\n'
            
        return board

    def in_check(self, player):
        # Find location of king
        for rank in range(8):
            if f'{player}k' in self.state[rank]:
                loc = (self.state[rank].index(f'{player}k'), rank)

        # Check in each direction if there is a piece that can hit the king
        # Cardinal directions:
        for x in range(loc[0]-1, -1, -1):
            if self.state[x][loc[1]] != '':
                if self.state[x][loc[1]][0] != player and self.state[x][loc[1]][1] in ['q','r']:
                    return True
                break
        for x in range(loc[0]+1, 8):
            if self.state[x][loc[1]] != '':
                if self.state[x][loc[1]][0] != player and self.state[x][loc[1]][1] in ['q','r']:
                    return True
                break
        for y in range(loc[1]-1, -1, -1):
            if self.state[loc[0]][y] != '':
                if self.state[loc[0]][y][0] != player and self.state[loc[0]][y][1] in ['q','r']:
                    return True
                break
        for y in range(loc[1]+1, 8):
            if self.state[loc[0]][y] != '':
                if self.state[loc[0]][y][0] != player and self.state[loc[0]][y][1] in ['q','r']:
                    return True
                break
            
        # Diagonals:
        check_loc = loc
        while True:
            check_loc = (check_loc[0] + 1, check_loc[1] + 1)
            if check_loc[0] == 8 or check_loc[1] == 8:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break
        check_loc = loc
        while True:
            check_loc = (check_loc[0] + 1, check_loc[1] - 1)
            if check_loc[0] == 8 or check_loc[1] == 8:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break
        check_loc = loc
        while True:
            check_loc = (check_loc[0] - 1, check_loc[1] + 1)
            if check_loc[0] == 8 or check_loc[1] == 8:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break
        check_loc = loc
        while True:
            check_loc = (check_loc[0] - 1, check_loc[1] - 1)
            if check_loc[0] == 8 or check_loc[1] == 8:
                break
            check_piece = self.state[check_loc[0]][check_loc[1]]
            if check_piece != '':
                if check_piece[0] != player and check_piece[1] in ['q','b']:
                    return True
                break

        #Pawns:
        #Knights:

    def move(self, player, piece, loc):
        # First do checks to see if move is valid
        # Check if the target square is occupied by own piece
        if self.state[loc[0]][loc[1]] != '':
            if self.state[loc[0]][loc[1]][0] == player:
                return "Invalid move"

        # Check if target square can be targeted by piece
        valid_pieces = []
        if piece == 'q':
            for x in range(loc[0]-1, -1, -1):
                if self.state[x][loc[1]] != '':
                    if self.state[x][loc[1]] == f'{player}q':
                        valid_pieces.append((x,loc[1]))
                    break
            for x in range(loc[0]+1, 8):
                if self.state[x][loc[1]] != '':
                    if self.state[x][loc[1]] == f'{player}q':
                        valid_pieces.append((x,loc[1]))
                    break
            for y in range(loc[1]-1, -1, -1):
                if self.state[loc[0]][y] != '':
                    if self.state[loc[0]][y] == f'{player}q':
                        valid_pieces.append((loc[0],y))
                    break
            for y in range(loc[1]+1, 8):
                if self.state[loc[0]][y] != '':
                    if self.state[loc[0]][y] == f'{player}q':
                        valid_pieces.append((loc[0],y))
                    break

class Piece():
    def __init__(self, piece, color, loc, board):
        self.piece = piece
        self.color = color
        self.loc = loc
        self.board = board
        self.moves = []
        self.check_moves()
        
    def check_moves(self, in_check):
        
        if self.piece == 'q':
            for x in range(self.loc[0]-1, -1. -1):
                if self.board.state[x][loc[1]] != '':
                    if self.board.state[x][loc[1]][0] != self.color:

def main():
    board = ChessBoard()
    print(board)

if __name__ == "__main__":
    main()
