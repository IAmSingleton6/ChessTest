from Units.base_unit import BaseUnit

class Bishop(BaseUnit):
    black_image_path = 'Images/bB.png'
    white_image_path = 'Images/wB.png'

    def __init__(self, is_white: bool, square_size: tuple) -> None:
        super().__init__(is_white, square_size)
        self.notation = 'B'
        self.material_value = 3


    def moveable_squares(self, pos, board):
        output = []
        board_size = board.board_size
        board_size_x = board.board_size[0]
        board_size_y = board.board_size[1]
        max_board_size = max(board_size)

        moves_ne = []
        for i in range(1, max_board_size):
            if pos[0] + i > board_size_x - 1 or pos[1] - i < 0:
                break
            moves_ne.append(board.square_at_position(
                (pos[0] + i, pos[1] - i)
            ))
        moves_se = []
        for i in range(1, max_board_size):
            if pos[0] + i > board_size_x - 1 or pos[1] + i > board_size_y - 1:
                break
            moves_se.append(board.square_at_position(
                (pos[0] + i, pos[1] + i)
            ))
        moves_sw = []
        for i in range(1, max_board_size):
            if pos[0] - i < 0 or pos[1] + i > board_size_y - 1:
                break
            moves_sw.append(board.square_at_position(
                (pos[0] - i, pos[1] + i)
            ))
        moves_nw = []
        for i in range(1, max_board_size):
            if pos[0] - i < 0 or pos[1] - i < 0:
                break
            moves_nw.append(board.square_at_position(
                (pos[0] - i, pos[1] - i)
            ))

        output = self.filter_directions(board, moves_ne, moves_nw, moves_se, moves_sw)
        return output

