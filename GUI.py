import pygame as p

HEIGHT, WIDTH = 800, 800
ROWS, COLS = 7, 7
SQ_SIZE = HEIGHT / ROWS + 1
PIECE_SIZE = 100
CIRCLE_SIZE = 0.1 * SQ_SIZE


def gui_board():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chess')
    img = p.transform.scale(p.image.load("Images/Chessboard.png"), (HEIGHT, WIDTH))
    screen.blit(img, (0, 0))
    return screen


def draw_pieces(screen, board_state):
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece is not None:
                screen.blit(piece.img, p.Rect(col * PIECE_SIZE, row * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))


def get_sq_selected():  # no issue
    location = p.mouse.get_pos()     # (x, y) pos of mouse
    row, col = int(location[1] // PIECE_SIZE), int(location[0] // PIECE_SIZE)
    return (row, col)


def is_legal_piece(sq_selected, chessboard): #no issue
    piece = chessboard.board_state[sq_selected[0]][sq_selected[1]]
    if piece is not None:
        return chessboard.whose_turn == piece.color
    else:
        return False


def show_legal_moves(screen, sq_selected, chessboard):
    piece = chessboard.board_state[sq_selected[0]][sq_selected[1]]
    legal_moves = piece.get_legal_moves(chessboard)
    for move in legal_moves:
        p.draw.circle(screen, "green",
                      (move[1] * PIECE_SIZE + 0.5 * PIECE_SIZE, move[0] * PIECE_SIZE + 0.5 * PIECE_SIZE),
                      CIRCLE_SIZE)
        p.display.update()


def show_checkmate(screen, chessboard):
    winner = "White" if chessboard.whose_turn == "Black" else "Black"
    font = p.font.Font('freesansbold.ttf', 50)
    text = font.render(f'CHECKMATE {winner} WINS', True, "black")
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)
    p.display.update()
