class ChessBoard():
    def __init__(self):
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

def main():
    board = ChessBoard()
    print(board)

if __name__ == "__main__":
    main()
