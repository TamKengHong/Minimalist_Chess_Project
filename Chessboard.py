from Chesspiece import *


class ChessBoard:
    def __init__(self):
        self.board_state = [([None] * 8) for _ in range(8)]
        self.whose_turn = "White"

        # setting up pieces in board.
        self.board_state[7] = [Rook("White"), Knight("White"), Bishop("White"), Queen("White"),
                               King("White"), Bishop("White"), Knight("White"), Rook("White")]
        self.board_state[6] = [Pawn("White") for _ in range(8)]
        self.board_state[0] = [Rook("Black"), Knight("Black"), Bishop("Black"), Queen("Black"),
                               King("Black"), Bishop("Black"), Knight("Black"), Rook("Black")]
        self.board_state[1] = [Pawn("Black") for _ in range(8)]

        # giving the pieces their row and col positions:
        for i in [0, 1, 6, 7]:
            for j in range(len(self.board_state[i])):
                piece = self.board_state[i][j]
                piece.row, piece.col = i, j

    def copy(self):
        copy = [([None] * 8) for _ in range(8)]
        for row in range(8):  # recreate the whole board_state to store
            for col in range(8):
                piece = self.board_state[row][col]
                if piece is not None:
                    if isinstance(piece, Pawn):
                        new_piece = copy[row][col] = Pawn(piece.color)
                    elif isinstance(piece, Rook):
                        new_piece = copy[row][col] = Rook(piece.color)
                    elif isinstance(piece, Bishop):
                        new_piece = copy[row][col] = Bishop(piece.color)
                    elif isinstance(piece, Queen):
                        new_piece = copy[row][col] = Queen(piece.color)
                    elif isinstance(piece, King):
                        new_piece = copy[row][col] = King(piece.color)
                    elif isinstance(piece, Knight):
                        new_piece = copy[row][col] = Knight(piece.color)
                    if isinstance(new_piece, Pawn) or isinstance(new_piece, Rook) or isinstance(new_piece, King):
                        new_piece.first_move = piece.first_move  # inherits the original piece first_moves
                    new_piece.row, new_piece.col = row, col
        return copy

    def can_move(self, start_pos, end_pos):
        piece = self.board_state[start_pos[0]][start_pos[1]]
        if piece is not None:
            if piece.color == self.whose_turn:
                legal_moves = piece.get_legal_moves(self)
                for move in legal_moves:
                    if end_pos == move:
                        return True
        return False

    def move_piece(self, start_pos, end_pos):  # positions are a pair of (row, col)
        piece = self.board_state[start_pos[0]][start_pos[1]]
        # piece.row, piece.col = end_pos[0], end_pos[1]
        self.board_state[start_pos[0]][start_pos[1]] = None
        self.board_state[end_pos[0]][end_pos[1]] = piece

    def can_castle(self, side):
        i = 7 if self.whose_turn == "White" else 0 # get the row
        The_King = self.board_state[i][4]
        if side == "Kingside": # initialise constants to use later
            j,k = 5, 6
            square_one, square_two, square_three = self.board_state[i][5], self.board_state[i][6], None
            The_Rook = self.board_state[i][7]
        else:
            j,k = 3, 2
            square_one, square_two, square_three = self.board_state[i][3],self.board_state[i][2],self.board_state[i][1]
            The_Rook = self.board_state[i][0]

        if isinstance(The_King, King) and isinstance(The_Rook, Rook):  # if it's actually the King and Rook
            if The_King.first_move == True and The_Rook.first_move == True:
                if square_one is None and square_two is None and square_three is None:
                    # Checks empty squares between King and Rook, then sees if the squares are in check.
                    if self.is_square_under_check((i,j)) or self.is_square_under_check((i,k)):
                        return False
                return True
        return False

    def can_castle_kingside(self):
        return self.can_castle("Kingside")

    def can_castle_queenside(self):
        return self.can_castle("Queenside")

    # def can_enpassant

    def castle_queenside(self):
        i = 7 if self.whose_turn == "White" else 0
        self.move_piece((i, 4), (i, 2))
        self.move_piece((i, 0), (i, 3))

    def castle_kingside(self):
        i = 7 if self.whose_turn == "White" else 0
        self.move_piece((i, 4), (i, 6))
        self.move_piece((i, 7), (i, 5))

    def pawn_promotion(self):  # checks the backrank if theres pawns to queen depending on color.
        for i in [7, 0]:
            for j in range(len(self.board_state[0])):
                if isinstance(self.board_state[i][j], Pawn):
                    self.board_state[i][j] = Queen(self.board_state[i][j].color)  # auto queen
                    self.board_state[i][j].row, self.board_state[i][j].col = i, j

    def is_square_under_check(self, square): # feed in a square pair(i,j) and determines if in check.
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[0])):
                piece = self.board_state[row][col]
                if piece is not None and piece.color != self.whose_turn:  # enemy piece
                    legal_moves = piece.get_all_moves(self.board_state)  # check every move if it gives rise to check
                    for move in legal_moves:
                        if move == square: # if there's a piece who can eat the square in next move
                            print(True)
                            return True
        return False

    def is_under_check(self):
        def checker(color):
            for row in range(len(self.board_state)):
                for col in range(len(self.board_state[0])):
                    if isinstance(self.board_state[row][col], King) and self.board_state[row][col].color == color:
                        The_King = self.board_state[row][col]  # selects the correct colored King
            return self.is_square_under_check((The_King.row, The_King.col))

        return checker(self.whose_turn)

    def is_mate(self): #doesnt work
        def has_legal_moves(color):
            for row in range(len(self.board_state)):
                for col in range(len(self.board_state[0])):
                    piece = self.board_state[row][col]
                    if piece is not None and piece.color == color and piece.get_legal_moves(self):
                        return True  # stop once there are legal moves
            return False

        if (not has_legal_moves(self.whose_turn)):  # checks if white or black turn has legal moves
            a = "Checkmate" if self.is_under_check() else "Stalemate"
            if a == "Checkmate":
                print("Checkmate") #doesnt work
                return True
        else:
            return False
