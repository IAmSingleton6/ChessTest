from Units.base_unit import BaseUnit

class Knight(BaseUnit):
    black_image_path = 'Images/bN.png'
    white_image_path = 'Images/wN.png'

    def __init__(self, is_white: bool, square_size: tuple) -> None:
        super().__init__(is_white, square_size)
        self.notation = 'N'
        self.material_value = 3


    def moveable_squares(self, pos, board):
        output = []
        moves = []

        moves.append((2, 1))
        moves.append((2, -1))
        moves.append((-2, 1))
        moves.append((-2, -1))
        moves.append((1, 2))
        moves.append((-1, 2))
        moves.append((1, -2))
        moves.append((-1, -2))

        for move in moves:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if new_pos[1] < board.board_size[1] and new_pos[1] >= 0 and new_pos[0] < board.board_size[0] and new_pos[0] >= 0:
                output.append(board.square_at_position(new_pos))

        output = self.filter_moves(board, output)
        return output

