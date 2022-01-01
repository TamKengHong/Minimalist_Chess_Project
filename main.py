from Chessboard import *
from GUI import *


def main():
    cbd = ChessBoard()
    sq_selected = ()  # no square selected, keep track of last click of user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(0, 0), (0, 1)]

    run = True
    while run:
        screen = gui_board()
        clock = p.time.Clock()

        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
                p.quit()
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:  # player input
                draw_pieces(screen, cbd.board_state)
                p.display.update()

                if len(player_clicks) == 0:
                    sq_selected = get_sq_selected() #no issue
                    if is_legal_piece(sq_selected, cbd):
                        #show_legal_moves(screen, sq_selected, cbd) #work on this later
                        piece = cbd.board_state[sq_selected[0]][sq_selected[1]]
                        print("the piece all moves is ", piece.get_all_moves(cbd.board_state))
                        print("the piece position is ", (piece.row, piece.col))
                        player_clicks.append(sq_selected)
                elif len(player_clicks) == 1:
                    if sq_selected == get_sq_selected():  # deselects if he clicks on same square
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = get_sq_selected()
                        player_clicks.append(sq_selected)

                        if cbd.can_move(player_clicks[0], player_clicks[1]): #by checking whether can move, the piece moved. nice bug
                            print("object at end_point is ", cbd.board_state[player_clicks[1][0]][player_clicks[1][1]])
                            print("actual move is", player_clicks[0], "to", player_clicks[1])
                            cbd.move_piece(player_clicks[0], player_clicks[1])
                            cbd.whose_turn = "White" if cbd.whose_turn == "Black" else "Black"
                            # it somehow ignores this and moves to the last position of all_moves.

                        screen = gui_board()
                        draw_pieces(screen, cbd.board_state)
                        p.display.update()

                        sq_selected = ()
                        player_clicks = []

                        # if cbd.is_mate():  # BUGGED
                        #      show_checkmate(screen, cbd)
                        print("Turn now is", cbd.whose_turn)


            clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
