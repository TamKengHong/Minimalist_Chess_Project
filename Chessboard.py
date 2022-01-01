from Chesspiece import *


class ChessBoard:
    def __init__(self):
        self.board_state = [([None] * 8) for _ in range(8)]
        self.whose_turn = "White"

        # setting up pieces in board.
        self.board_state[7] = [Rook("White"), Knight("White"), Bishop("White"), Queen("White"),
                               King("White"), Bishop("White"), Knight("White"), Rook("White")]
        self.board_state[6] = [Pawn("White")] * 8
        self.board_state[0] = [Rook("Black"), Knight("Black"), Bishop("Black"), Queen("Black"),
                               King("Black"), Bishop("Black"), Knight("Black"), Rook("Black")]
        self.board_state[1] = [Pawn("Black")] * 8

        # giving the pieces their row and col positions:
        for i in [0, 1, 6, 7]:
            for j in range(len(self.board_state[i])):
                piece = self.board_state[i][j]
                piece.row, piece.col = i, j

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
        if start_pos[0] not in range(8) or start_pos[1] not in range(8):
            if end_pos[0] not in range(8) or end_pos[1] not in range(8):
                return False
            return False
        piece = self.board_state[start_pos[0]][start_pos[1]]
        # if (isinstance(piece, Pawn) or isinstance(piece, Rook) or isinstance(piece, King)) and piece.first_move == True:
        #     piece.first_move = False  # pawns will now only be able to move 1 step, or King/Rook can't castle anymore.
        if piece is not None:
            piece.row, piece.col = end_pos[0], end_pos[1]
        self.board_state[start_pos[0]][start_pos[1]] = None
        self.board_state[end_pos[0]][end_pos[1]] = piece

        return True

    def can_castle(self, side):
        i = 0 if self.whose_turn == "White" else 7 # get the row
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
        i = 0 if self.whose_turn == "White" else 7
        self.move_piece((i, 4), (i, 2))
        self.move_piece((i, 0), (i, 3))

    def castle_kingside(self):
        i = 0 if self.whose_turn == "White" else 7
        self.move_piece((i, 4), (i, 6))
        self.move_piece((i, 7), (i, 5))

    def pawn_promotion(self):  # checks the backrank if theres pawns to queen depending on color.
        for i in [7, 0]:
            for j in range(len(self.board_state[0])):
                piece = self.board_state[i][j]
                if isinstance(self.board_state[i][j], Pawn) and piece.color == self.whose_turn:
                    piece = Queen(self.whose_turn)  # auto queen
                    piece.row, piece.col = i, j

    def is_square_under_check(self, square): # feed in a square pair(i,j) and determines if in check.
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[0])):
                piece = self.board_state[row][col]
                if piece is not None and piece.color != self.whose_turn:  # enemy piece
                    legal_moves = piece.get_legal_moves(self)
                    for move in legal_moves:
                        if move == square: # if there's a piece who can eat the square in next move
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

    def is_mate(self):
        def has_legal_moves(color):
            for row in range(len(self.board_state)):
                for col in range(len(self.board_state[0])):
                    piece = self.board_state[row][col]
                    if piece is not None and piece.color == color and piece.get_legal_moves(self):
                        return True  # stop once there are legal moves
            return False

        if (not has_legal_moves(self.whose_turn)):  # checks if white or black turn has legal moves
            return "Checkmate" if self.is_under_check() else "Stalemate"
        else:
            return False

# if self.whose_turn == "White":  # changes the turn!!! DO NOT! this one only done aft all the checks!
#     self.whose_turn = "Black"
# else:
#     self.whose_turn = "White"
