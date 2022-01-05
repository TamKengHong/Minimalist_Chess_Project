import pygame
import pygame as p
from Chessboard import *

WIDTH, HEIGHT = 800, 800

window = p.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


def check_castle(screen, cbd, sq_selected):
    castle_kingside_move, castle_queenside_move, enpassant_move = None, None, None
    piece = cbd.board_state[sq_selected[0]][sq_selected[1]]

    if isinstance(piece, King):  # checks for castle and displays the move
        if cbd.can_castle("Kingside"):
            castle_kingside_move = ([sq_selected, (0, 6)] if cbd.whose_turn == "Black"
                                    else [sq_selected, (7, 6)])

        if cbd.can_castle("Queenside"):
            castle_queenside_move = ([sq_selected, (0, 2)] if cbd.whose_turn == "Black"
                                     else [sq_selected, (7, 2)])

    if isinstance(piece, Pawn):
        if piece.enpassant_move:
            enpassant_move = piece.enpassant_move

    return castle_kingside_move, castle_queenside_move, enpassant_move


def refresh_screen(cbd, player_clicks):
    screen = gui_board(cbd)
    if len(player_clicks) == 0:
        sq_selected = get_sq_selected()
        ck, cq, emp = check_castle(screen, cbd, sq_selected)
        if is_legal_piece(sq_selected, cbd):
            show_legal_moves(screen, sq_selected, cbd, ck, cq, emp)
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    player_clicks.append(sq_selected)
    elif len(player_clicks) == 1:
        ck, cq, emp = check_castle(screen, cbd, player_clicks[0])
        if is_legal_piece(player_clicks[0], cbd):
            show_legal_moves(screen, player_clicks[0], cbd, ck, cq, emp)
    p.display.update()
    return screen


def gui_board(cbd):
    global window
    p.init()
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            window = p.display.set_mode((width, height), pygame.RESIZABLE)
    p.display.set_caption('Chess')
    img = p.transform.smoothscale(p.image.load("Images/Chessboard.png"), (window.get_width(), window.get_height()))
    window.blit(img, (0, 0))
    draw_pieces(window, cbd.board_state)
    return window


def draw_pieces(screen, board_state):
    w, h = window.get_width() // 8, window.get_height() // 8
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece is not None:
                piece.img = pygame.transform.smoothscale(piece.img, (w, h))
                screen.blit(piece.img, p.Rect(col * w, row * h, w, h))


def get_sq_selected():  # no issue
    w, h = window.get_width() / 8, window.get_height() / 8
    location = p.mouse.get_pos()  # (x, y) pos of mouse
    row, col = int(location[1] // h), int(location[0] // w)
    return row, col


def is_legal_piece(sq_selected, chessboard):  # no issue
    piece = chessboard.board_state[sq_selected[0]][sq_selected[1]]
    if piece is not None:
        return chessboard.whose_turn == piece.color
    else:
        return False


def show_legal_moves(screen, sq_selected, chessboard, castle_kingside_moves=None,
                     castle_queenside_moves=None, enpassant_moves=None):
    piece = chessboard.board_state[sq_selected[0]][sq_selected[1]]
    if piece is not None:
        legal_moves = piece.get_legal_moves(chessboard)
        for move in legal_moves:
            display_circle(screen, move)
        if castle_kingside_moves is not None:
            for move in castle_kingside_moves:
                display_circle(screen, move)
            return
        if castle_queenside_moves is not None:
            for move in castle_queenside_moves:
                display_circle(screen, move)
            return
        if enpassant_moves is not None:
            for move in enpassant_moves:
                display_circle(screen, move)


def display_circle(screen, move):
    piece_w = screen.get_width()//8
    piece_h = screen.get_height()//8
    circle_size = (screen.get_height()/7 + 1) * 0.1
    p.draw.circle(screen, "green", ((piece_w * (move[1] + 0.5)), (piece_h * (move[0] + 0.5))), circle_size)
    p.display.update()


def show_checkmate(screen, chessboard):
    winner = "WHITE" if chessboard.whose_turn == "Black" else "BLACK"
    font = p.font.Font('freesansbold.ttf', 50)
    text = font.render(f'CHECKMATE {winner} WINS', True, "black")
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)
    p.display.update()
