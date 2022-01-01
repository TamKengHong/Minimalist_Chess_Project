from Chesspiece import *


class ChessBoard:
    def __init__(self):
        self.board_state = [([None] * 8) for _ in range(8)]
        self.whose_turn = "White"

        # #Test Board
        # self.board_state[7] = [None, None, None, Bishop("White"),
        #                        King("White"), None, None, None]
        # self.board_state[0] = [None, None, None, Bishop("Black"),
        #                        Pawn("Black"), None, None, None]


        # setting up pieces in board.
        self.board_state[7] = [Rook("White"), Knight("White"), Bishop("White"), Queen("White"),
                               King("White"), Bishop("White"), Knight("White"), Rook("White")]
        self.board_state[6] = [Pawn("White"), Pawn("White"), Pawn("White"), Pawn("White"),
                               Pawn("White"), Pawn("White"), Pawn("White"), Pawn("White")]
        self.board_state[0] = [Rook("Black"), Knight("Black"), Bishop("Black"), Queen("Black"),
                               King("Black"), Bishop("Black"), Knight("Black"), Rook("Black")]
        self.board_state[1] = [Pawn("Black"), Pawn("Black"), Pawn("Black"), Pawn("Black"),
                               Pawn("Black"), Pawn("Black"), Pawn("Black"), Pawn("Black")]

        # giving the pieces their row and col positions:
        for i in [0, 1, 6, 7]:
            for j in range(len(self.board_state[i])):
                piece = self.board_state[i][j]
                if isinstance(piece, ChessPiece):
                    piece.row, piece.col = i, j

    def can_move(self, start_pos, end_pos):
        piece = self.board_state[start_pos[0]][start_pos[1]]
        if piece is not None:
            if piece.color == self.whose_turn:
                legal_moves = piece.get_legal_moves(self)
                for move in legal_moves:
                    if end_pos[0] == move[0] and end_pos[1] == move[1]:
                        return True
                if len(legal_moves) == 0:
                    print("no legal moves")
                    return False
        return False

    def move_piece(self, start_pos, end_pos):  # positions are a pair of (row, col)
        piece = self.board_state[start_pos[0]][start_pos[1]]
        if (isinstance(piece, Pawn) or isinstance(piece, Rook) or isinstance(piece, King)) and piece.first_move == True:
            piece.first_move = False  # pawns will now only be able to move 1 step, or King/Rook can't castle anymore.
            # possible bug where legal move will move the pawn but it actually hasnt moved, then first_move set to false

        piece.row, piece.col = end_pos[0], end_pos[1]
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
                piece = self.board_state[i][j]
                if isinstance(self.board_state[i][j], Pawn) and piece.color == self.whose_turn:
                    piece = Queen(self.whose_turn)  # auto queen
                    piece.row, piece.col = i, j

    def is_square_under_check(self, square): # feed in a square pair(i,j) and determines if in check.
        for row in range(len(self.board_state)):
            for col in range(len(self.board_state[0])):
                piece = self.board_state[row][col]
                if piece is not None and piece.color != self.whose_turn:  # enemy piece
                    legal_moves = piece.get_all_moves(self.board_state)  # check every move if it gives rise to check
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

