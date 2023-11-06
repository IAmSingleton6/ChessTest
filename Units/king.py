from Units.base_unit import BaseUnit

class King(BaseUnit):
    black_image_path = 'Images/bK.png'
    white_image_path = 'Images/wK.png'

    def __init__(self, is_white: bool, square_size: tuple) -> None:
        super().__init__(is_white, square_size)
        self.has_moved = False
        self.can_castle = True
        self.notation = 'K'


    def moveable_squares(self, pos, board):
        output = []
        moves = []

        moves.append((0, 1))
        moves.append((0, -1))
        moves.append((1, 1))
        moves.append((1, -1))
        moves.append((-1, 1))
        moves.append((-1, -1))
        moves.append((1, 0))
        moves.append((-1, 0))

        # TODO
        # Add castling
        # Disallow moves resulting in check/checkmate
        if not self.has_moved:
            if self.can_castle:
                print("ADD CASTLING")

        for move in moves:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if new_pos[1] < board.board_size[1] and new_pos[1] >= 0 and new_pos[0] < board.board_size[0] and new_pos[0] >= 0:
                output.append(board.square_at_position(new_pos))

        output = self.filter_moves(board, output)
        return output

