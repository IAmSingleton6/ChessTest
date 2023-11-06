from Units.base_unit import BaseUnit

class Rook(BaseUnit):
    black_image_path = 'Images/bR.png'
    white_image_path = 'Images/wR.png'

    def __init__(self, is_white: bool, square_size: tuple) -> None:
        super().__init__(is_white, square_size)
        self.notation = 'R'
        self.material_value = 5


    def moveable_squares(self, pos, board):
        output = []
        board_size = board.board_size
        board_size_x = board.board_size[0]
        board_size_y = board.board_size[1]
        max_board_size = max(board_size)

        moves_n = []
        for i in range(1, max_board_size):
            if pos[1] - i < 0:
                break
            moves_n.append(board.square_at_position(
                (pos[0], pos[1] - i)
            ))
        moves_s = []
        for i in range(1, max_board_size):
            if pos[1] + i > board_size_y - 1:
                break
            moves_s.append(board.square_at_position(
                (pos[0], pos[1] + i)
            ))
        moves_w = []
        for i in range(1, max_board_size):
            if pos[0] - i < 0:
                break
            moves_w.append(board.square_at_position(
                (pos[0] - i, pos[1])
            ))
        moves_e = []
        for i in range(1, max_board_size):
            if pos[0] + i > board_size_x - 1:
                break
            moves_e.append(board.square_at_position(
                (pos[0] + i, pos[1])
            ))

        output = self.filter_directions(board, moves_n, moves_s, moves_w, moves_e)
        return output

