import pygame
import pygame as p

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 7, 7
SQ_SIZE = HEIGHT / ROWS + 1
PIECE_SIZE = HEIGHT/8
CIRCLE_SIZE = 0.1 * SQ_SIZE

window = p.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


# Helper function to give other modules the window size
def piece_size():
    return window.get_width()//8, window.get_height()//8


def gui_board():
    global window
    p.init()
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            window = p.display.set_mode((width, height), pygame.RESIZABLE)
    p.display.set_caption('Chess')
    img = p.transform.scale(p.image.load("Images/Chessboard.png"), (window.get_width(), window.get_height()))
    window.blit(img, (0, 0))
    return window


def draw_pieces(screen, board_state):
    w, h = window.get_width()//8, window.get_height()//8
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece is not None:
                screen.blit(piece.get_img, p.Rect(col * w, row * h, w, h))


def get_sq_selected():  # no issue
    w, h = window.get_width()/8, window.get_height()/8
    location = p.mouse.get_pos()     # (x, y) pos of mouse
    row, col = int(location[1] // h), int(location[0] // w)
    return row, col


def is_legal_piece(sq_selected, chessboard):  # no issue
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
    winner = "WHITE" if chessboard.whose_turn == "Black" else "BLACK"
    font = p.font.Font('freesansbold.ttf', 50)
    text = font.render(f'CHECKMATE {winner} WINS', True, "black")
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)
    p.display.update()
