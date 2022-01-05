import pygame as p

HEIGHT, WIDTH, ROWS, COLS = 800, 800, 7, 7
SQ_SIZE = HEIGHT / ROWS + 1
PIECE_SIZE, CIRCLE_SIZE = 100, 0.1 * SQ_SIZE


def gui_board():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chess')
    screen.blit(p.transform.scale(p.image.load("Images/Chessboard.png"), (HEIGHT, WIDTH)), (0, 0))
    return screen


def draw_pieces(screen, board_state):
    for i in range(8):
        for j in range(8):
            if board_state[i][j] is not None:
                screen.blit(board_state[i][j].img, p.Rect(j * PIECE_SIZE, i * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))


def get_sq_selected():  # no issue
    location = p.mouse.get_pos()     # (x, y) pos of mouse
    row, col = int(location[1] // PIECE_SIZE), int(location[0] // PIECE_SIZE)
    return (row, col)


def is_legal_piece(sq_selected, board): #no issue
    piece = board.board_state[sq_selected[0]][sq_selected[1]]
    return board.whose_turn == piece.color if piece is not None else False


def show_legal_moves(screen, sq_selected, board):
    piece = board.board_state[sq_selected[0]][sq_selected[1]]
    legal_moves = piece.get_legal_moves(board)
    for move in legal_moves:
        display_circle(screen, move)


def display_circle(screen, move):
    p.draw.circle(screen, "green",
                  (move[1] * PIECE_SIZE + 0.5 * PIECE_SIZE, move[0] * PIECE_SIZE + 0.5 * PIECE_SIZE), CIRCLE_SIZE)
    p.display.update()


def show_checkmate(screen, chessboard):
    winner = "WHITE" if chessboard.whose_turn == "Black" else "BLACK"
    font = p.font.Font('freesansbold.ttf', 50)
    text = font.render(f'CHECKMATE {winner} WINS', True, "black")
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)
    p.display.update()
