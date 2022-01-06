from Chesspiece import *


class ChessBoard:
    def __init__(self):
        self.board_state = [([None] * 8) for _ in range(8)]
        self.whose_turn = "White"

        for i in [0, 1, 6, 7]:  # Setting up board + giving pieces their row, col positions.
            c = "Black" if i <= 1 else "White"  # c is the color of the piece
            self.board_state[i] = ([Rook(c), Knight(c), Bishop(c), Queen(c), King(c), Bishop(c),
                                    Knight(c), Rook(c)] if i == 0 or i == 7 else [Pawn(c) for _ in range(8)])
            for j in range(8):
                self.board_state[i][j].row, self.board_state[i][j].col = i, j

    def copy(self):  # recreate the whole board_state to store
        copy = [([None] * 8) for _ in range(8)]
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece is not None:
                    if isinstance(piece, Pawn):
                        new_piece = copy[row][col] = Pawn(piece.color)  # copies the piece and enpassant state
                        new_piece.enpassantable, new_piece.enpassant_move = piece.enpassantable, piece.enpassant_move
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
        if piece is not None and piece.color == self.whose_turn:
            legal_moves = piece.get_legal_moves(self)
            for move in legal_moves:
                if end_pos == move:
                    return True
        return False

    def move_piece(self, start_pos, end_pos):  # positions are a pair of (row, col)
        piece = self.board_state[start_pos[0]][start_pos[1]]
        piece.row, piece.col = end_pos[0], end_pos[1]  # update row and col of piece
        self.board_state[end_pos[0]][end_pos[1]] = piece
        self.board_state[start_pos[0]][start_pos[1]] = None

    def can_castle(self, side):
        i = 7 if self.whose_turn == "White" else 0  # get the row
        the_king = self.board_state[i][4]
        if side == "Kingside":  # initialise constants to use later
            sq_one, sq_two, sq_three = self.board_state[i][5], self.board_state[i][6], None
            j, k, the_rook = 5, 6, self.board_state[i][7]
        else:
            sq_one, sq_two, sq_three = self.board_state[i][3], self.board_state[i][2], self.board_state[i][1]
            j, k, the_rook = 3, 2, self.board_state[i][0]

        if isinstance(the_king, King) and isinstance(the_rook, Rook):  # if it's actually the King and Rook
            if the_king.first_move is True and the_rook.first_move is True:
                if sq_one is None and sq_two is None and sq_three is None:
                    if self.is_square_under_check((i, j)) or self.is_square_under_check((i, k)):
                        return False  # Checks empty squares between King and Rook, then sees if squares are in check.
                    return True
        return False

    def castle(self, side):
        i = 7 if self.whose_turn == "White" else 0
        moves = [(i, 4), (i, 6), (i, 7), (i, 5)] if side == "Kingside" else [(i, 4), (i, 2), (i, 0), (i, 3)]
        self.move_piece(moves[0], moves[1])
        self.move_piece(moves[2], moves[3])

    def reset_enpassant(self):
        for row in range(8):
            for col in range(8):
                if isinstance(self.board_state[row][col], Pawn):
                    self.board_state[row][col].enpassantable = False

    def capture_enpassant(self, pawn):
        new_row, new_col = pawn.enpassant_move[0], pawn.enpassant_move[1]
        self.board_state[pawn.row][new_col] = None  # eats the pawn
        self.move_piece((pawn.row, pawn.col), (new_row, new_col))  # move pawn to new square

    def pawn_promotion(self):  # checks the backrank if there's pawns to queen depending on color.
        for i in [7, 0]:
            for j in range(8):
                if isinstance(self.board_state[i][j], Pawn):
                    self.board_state[i][j] = Queen(self.board_state[i][j].color)  # auto queen
                    self.board_state[i][j].row, self.board_state[i][j].col = i, j

    def is_square_under_check(self, square):  # feed in a square pair(i,j) and determines if in check.
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece is not None and piece.color != self.whose_turn:  # enemy piece
                    all_moves = piece.get_all_moves(self.board_state)  # check every move if it gives rise to check
                    for move in all_moves:
                        if move == square:  # if there's a piece who can eat the square in next move
                            return True
        return False

    def is_under_check(self):
        def checker(color):
            for row in range(8):
                for col in range(8):
                    if isinstance(self.board_state[row][col], King) and self.board_state[row][col].color == color:
                        the_king = self.board_state[row][col]  # selects the correct colored King
            return self.is_square_under_check((the_king.row, the_king.col))

        return checker(self.whose_turn)

    def is_checkmate(self):
        def has_legal_moves(color):
            for row in range(8):
                for col in range(8):
                    piece = self.board_state[row][col]
                    if piece is not None and piece.color == color and piece.get_legal_moves(self):
                        return True  # stop once there are legal moves
            return False

        return (not has_legal_moves(self.whose_turn)) and self.is_under_check()
