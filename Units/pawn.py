from Units.base_unit import BaseUnit

class Pawn(BaseUnit):
    black_image_path = 'Images/bP.png'
    white_image_path = 'Images/wP.png'

    def __init__(self, is_white: bool, square_size: tuple) -> None:
        super().__init__(is_white, square_size)
        self.can_move_two_spaces = True
        self.notation = 'P'
        self.material_value = 1


    def moveable_squares(self, pos, board): 
        output = []
        moves = []
        moves_diagonal = []

        if self.is_white:
            moves.append((0, -1))
            if self.can_move_two_spaces:
                moves.append((0, -2))
            moves_diagonal.append((-1, -1))
            moves_diagonal.append((1, -1))
        else:
            moves.append((0, 1))
            if self.can_move_two_spaces:
                moves.append((0, 2))
            moves_diagonal.append((-1, 1))
            moves_diagonal.append((1, 1))

        for move in moves:
            new_pos = (pos[0], pos[1] + move[1])
            if new_pos[1] < board.board_size[1] and new_pos[1] >= 0:
                square = board.square_at_position(new_pos)
                if not square.piece:
                    output.append(board.square_at_position(new_pos))

        for move in moves_diagonal:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if new_pos[1] < board.board_size[1] and new_pos[1] >= 0 and new_pos[0] < board.board_size[0] and new_pos[0] >= 0:
                square = board.square_at_position(new_pos)
                if square.piece:
                    if square.piece.is_white != self.is_white:
                        output.append(square)

        # ADD EN CROISSAINT
        
        return output
