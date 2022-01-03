from Chessboard import *
from GUI import *


def main():
    cbd = ChessBoard()
    sq_selected = ()  # no square selected, keep track of last click of user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(0, 0), (0, 1)]

    def refresh_screen():
        screen = gui_board()
        draw_pieces(screen, cbd.board_state)
        p.display.update()

    screen = gui_board()
    refresh_screen() #initialise the screen

    while True:
        clock = p.time.Clock()

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()

            elif e.type == p.MOUSEBUTTONDOWN:  # player input
                if len(player_clicks) == 0:
                    sq_selected = get_sq_selected()  # no issue
                    if is_legal_piece(sq_selected, cbd):
                        show_legal_moves(screen, sq_selected, cbd)  # ok
                        player_clicks.append(sq_selected)

                elif len(player_clicks) == 1:
                    if sq_selected == get_sq_selected():  # deselects if he clicks on same square
                        sq_selected = ()
                        player_clicks = []
                        refresh_screen()
                    else:
                        sq_selected = get_sq_selected()
                        player_clicks.append(sq_selected)

                        if cbd.can_move(player_clicks[0], player_clicks[1]):
                            cbd.move_piece(player_clicks[0], player_clicks[1])
                            cbd.pawn_promotion()
                            piece = cbd.board_state[player_clicks[1][0]][player_clicks[1][1]]
                            if isinstance(piece, Pawn) or isinstance(piece, King) or isinstance(piece, Rook):
                                piece.first_move = False
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black"

                        refresh_screen()

                        sq_selected = ()
                        player_clicks = []

                        if cbd.is_mate():  # BUGGED
                            show_checkmate(screen, cbd)
                        print("Turn now is", cbd.whose_turn)
            clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
