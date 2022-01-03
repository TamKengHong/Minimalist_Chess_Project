from Chessboard import *
from GUI import *


def main():
    cbd = ChessBoard()
    sq_selected = ()  # no square selected, keep track of last click of user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(0, 0), (0, 1)]

    def refresh_screen():
        draw_pieces(gui_board(), cbd.board_state)
        p.display.update()

    screen = gui_board()
    refresh_screen() #initialise the screen
    mate = False

    while True:

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

                        if cbd.can_move(player_clicks[0], player_clicks[1]):  # move the piece and does checks.
                            cbd.move_piece(player_clicks[0], player_clicks[1])
                            piece = cbd.board_state[player_clicks[1][0]][player_clicks[1][1]]
                            if isinstance(piece, Pawn) or isinstance(piece, King) or isinstance(piece, Rook):
                                piece.first_move = False
                            cbd.pawn_promotion()
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black"

                        if cbd.is_mate():  # BUGGED
                            mate = True

                        refresh_screen()

                        sq_selected = ()
                        player_clicks = []

                        print("Turn now is", cbd.whose_turn)

        if mate is True:
            show_checkmate(screen, cbd)


if __name__ == '__main__':
    main()
