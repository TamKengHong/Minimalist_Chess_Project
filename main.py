from Chessboard import *
from GUI import *


def main():
    cbd, screen, mate = ChessBoard(), gui_board(), False
    sq_selected, player_clicks = (), []  # sq is tuple of (row, col), player_clicks is array of sq_selected
    castle_kingside_move, castle_queenside_move, enpassant_move = None, None, None

    def refresh_screen():
        draw_pieces(gui_board(), cbd.board_state)
        p.display.update()

    refresh_screen()  # initialise the screen

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()

            elif e.type == p.MOUSEBUTTONDOWN:  # player input
                if len(player_clicks) == 0:
                    sq_selected = get_sq_selected()

                    if is_legal_piece(sq_selected, cbd):
                        show_legal_moves(screen, sq_selected, cbd)
                        piece = cbd.board_state[sq_selected[0]][sq_selected[1]]

                        if isinstance(piece, King):  # checks for castle and displays the move
                            if cbd.can_castle("Kingside"):
                                castle_kingside_move = ([sq_selected, (0,6)] if cbd.whose_turn == "Black"
                                                        else [sq_selected, (7,6)])
                                display_circle(screen, castle_kingside_move[1])

                            if cbd.can_castle("Queenside"):
                                castle_queenside_move = ([sq_selected, (0, 2)] if cbd.whose_turn == "Black"
                                                        else [sq_selected, (7, 2)])
                                display_circle(screen, castle_queenside_move[1])

                        if isinstance(piece, Pawn):
                            if piece.enpassant_move:
                                enpassant_move = piece.enpassant_move
                                display_circle(screen, enpassant_move)

                        player_clicks.append(sq_selected)

                elif len(player_clicks) == 1:
                    if sq_selected == get_sq_selected():  # deselects if he clicks on same square
                        sq_selected, player_clicks = (), []
                        refresh_screen()
                    else:
                        sq_selected = get_sq_selected()
                        player_clicks.append(sq_selected)

                        if cbd.can_move(player_clicks[0], player_clicks[1]):  # move the piece and does checks.
                            cbd.move_piece(player_clicks[0], player_clicks[1])
                            piece = cbd.board_state[player_clicks[1][0]][player_clicks[1][1]]
                            if isinstance(piece, Pawn) and abs(player_clicks[1][0] - player_clicks[0][0]) == 2:
                                piece.enpassantable = True  # pawn moves 2 rows forward
                            if isinstance(piece, Pawn) or isinstance(piece, King) or isinstance(piece, Rook):
                                piece.first_move = False
                            cbd.pawn_promotion()
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black"

                        # special moves (eg: castle, enpassant)
                        if player_clicks == castle_kingside_move:
                            cbd.castle("Kingside")
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black"

                        if player_clicks == castle_queenside_move:
                            cbd.castle("Queenside")
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black" #repeated, refactor out.

                        if sq_selected == enpassant_move:
                            pawn_selected = cbd.board_state[player_clicks[0][0]][player_clicks[0][1]]
                            cbd.capture_enpassant(pawn_selected)
                            pawn_selected.enpassant_move = None
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black"

                        if cbd.is_mate():
                            mate = True

                        cbd.reset_enpassant()

                        refresh_screen()
                        sq_selected, player_clicks = (), []

                        print("Turn now is", cbd.whose_turn)

        if mate is True:
            show_checkmate(screen, cbd)


if __name__ == '__main__':
    main()
