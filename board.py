import numpy
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.draw import rect, circle
from pygame import Rect
from config import SCREEN_SIZE
from components import Renderer, Update, Input
from piece import Piece

from Units.base_unit import BaseUnit
from Units.king import King
from Units.pawn import Pawn
from Units.bishop import Bishop
from Units.knight import Knight
from Units.queen import Queen
from Units.rook import Rook


class Board():
    base_board = [[Piece.bR, Piece.bN, Piece.bB, Piece.bQ, Piece.bK, Piece.bB, Piece.bN, Piece.bR],
                  [Piece.bP, Piece.bP, Piece.bP, Piece.bP, Piece.bP, Piece.bP, Piece.bP, Piece.bP],
                  [Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA],
                  [Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA],
                  [Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA],
                  [Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA, Piece.NA],
                  [Piece.wP, Piece.wP, Piece.wP, Piece.wP, Piece.wP, Piece.wP, Piece.wP, Piece.wP],
                  [Piece.wR, Piece.wN, Piece.wB, Piece.wQ, Piece.wK, Piece.wB, Piece.wN, Piece.wR]]


    def __init__(self, board = base_board) -> None:
        board_size = numpy.shape(board)
        # in shape, [0] is the y so need to invert
        self.is_white_turn = True
        self.board_size = (board_size[1], board_size[0])
        self.board_margin = 100
        self._calculate_draw_variables(SCREEN_SIZE, self.board_size, self.board_margin)
        
        squares = []
        for y in range(0, self.board_size[1]):
            for x in range(0, self.board_size[0]):
                # shape of initialiser board is y then x so invert unit creation
                unit = self._initialise_unit(board[y][x])
                squares.append(Square((x, y), self, unit))

        self.squares = squares


    # Find size of individual square on the board and the origin position in pixels
    def _calculate_draw_variables(self, screen_size, board_size, margin) -> None:
        square_size = numpy.divide(numpy.subtract(screen_size, 2 * margin), board_size)
        self.square_size = (min(square_size), min(square_size))
        display_board_size = numpy.multiply(self.square_size, board_size) 
        self.origin_pos = numpy.subtract(screen_size, display_board_size) / 2


    def _initialise_unit(self, piece: Piece) -> BaseUnit:
        # Use the bit shift to detect if piece is black or white
        # If bit 0 is 1, then white else black
        match piece:
            case Piece.bP | Piece.wP:
                return Pawn(piece & (1 << 0), self.square_size)
            case Piece.bQ | Piece.wQ:
                return Queen(piece & (1 << 0), self.square_size)
            case Piece.bK | Piece.wK:
                return King(piece & (1 << 0), self.square_size)
            case Piece.bB | Piece.wB:
                return Bishop(piece & (1 << 0), self.square_size)
            case Piece.bN | Piece.wN:
                return Knight(piece & (1 << 0), self.square_size)
            case Piece.bR | Piece.wR:
                return Rook(piece & (1 << 0), self.square_size)
            case other:
                return None


    def square_at_position(self, pos: (int, int)):
        for square in self.squares:
            if square.pos == pos:
                return square
            

    def square_from_mouse_position(self, mouse_pos):
        for square in self.squares:
            if square.is_mouse_touching_square(mouse_pos):
                return square
        return None
            

    # TODO: implement castling
    # TODO: add material_values and display removed pieces on each color's side
    # TODO: possibly display an eval bar
    # TODO: sound effect when piece is taken
    def move_piece_to_square(self, piece, from_square, to_square):
        if piece.is_white != self.is_white_turn:
            # TODO
            # Start AI turn here, which will eventually call board.move_piece_to_square() to move the opposite pieces
            return
        
        self.is_white_turn = not self.is_white_turn

        from_square.place_piece_on_square(None)

        if piece.notation == 'P':
            piece.can_move_two_spaces = False
            if to_square.pos[1] == 0 or to_square.pos[1] == self.board_size[1] - 1:
                print("Upgrade pawn: to be implemented")
        if piece.notation == 'K':
            piece.has_moved = True

        to_square.place_piece_on_square(piece)
            


    def piece_at_position(self, pos: (int, int)):
        assert pos[0] >= self.board_size[0] or pos[0] < 0 or pos[1] >= self.board_size[1] or pos[1] < 0
        square = self.square_at_position(pos)
        return square.piece if square.piece else None
           
    
    def show_moveable_squares(self, show: bool, pos: tuple = None, piece: BaseUnit = None) -> None:
        if show:
            moveable_squares = piece.moveable_squares(pos, self)
            if moveable_squares:
                for square in moveable_squares:
                    square.piece_can_move_to_square = True
        else:
            for square in self.squares:
                    square.piece_can_move_to_square = False 



# More than one component so run their deletes
class Square(Renderer, Input):
    black = (20, 123, 155)
    white = (255, 255, 200)
    highlight = (0, 255, 0)
    moveable = (255, 0, 0)

    def __init__(self, pos: (int, int), board: Board, piece: BaseUnit = None) -> None:
        self.pos: tuple = pos
        self.highlight_square: bool = False
        self.piece_can_move_to_square = False
        self.board: Board = board
        self.square_color: tuple = self._square_color(self.pos)
        self.draw_rect: Rect = self._calculate_draw_rect(pos, board)
        input_r: Rect = self.draw_rect.copy()
        # Make input rect slightly smaller so multiple pieces cannot be selected at once
        self.input_rect = input_r.scale_by(0.95, 0.95)
        self.piece = None
        self.place_piece_on_square(piece)
    

    def place_piece_on_square(self, piece):
        if piece:
            if self.piece:
                self.piece.delete()
            piece.set_image_position(self.draw_rect.center)
        self.piece = piece




    def draw(self, window) -> None:
        sq_color = self.square_color if not self.highlight_square else self.highlight
        rect(window, sq_color, self.draw_rect)
        if self.piece_can_move_to_square:
            circle(window, self.moveable, self.draw_rect.center, self.draw_rect.size[0] * 0.25)
            
            
    # Deal with input from the player
    def handle_input(self, event, mouse_pos) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if self.is_mouse_touching_square(mouse_pos):
                if self.piece:
                    self.piece.pickup_piece(True)
                    self.highlight_square = True
                    self.board.show_moveable_squares(True, self.pos, self.piece)
        if event.type == MOUSEBUTTONUP:
            if self.piece:
                if self.piece.is_piece_held():
                    self.piece.pickup_piece(False)
                    mouse_release_square = self.board.square_from_mouse_position(mouse_pos)
                    if mouse_release_square:
                        if mouse_release_square.piece_can_move_to_square:
                            self.board.move_piece_to_square(self.piece, self, mouse_release_square)
                    self.highlight_square = False
                    self.board.show_moveable_squares(False)


    
    def is_mouse_touching_square(self, mouse_pos) -> bool:
        return self.input_rect.collidepoint(mouse_pos[0], mouse_pos[1])


    def _calculate_draw_rect(self, pos, board) -> Rect:
        square_pos_from_origin = numpy.multiply(board.square_size, pos)
        draw_pos = numpy.add(board.origin_pos, square_pos_from_origin)
        # +1 to rect size to ensure borders fully overlap with no white space due to discrete pixels using float math
        return Rect(draw_pos[0], draw_pos[1], board.square_size[0] + 1, board.square_size[1] + 1)


    def _square_color(self, pos: tuple) -> tuple:
        if pos[0] % 2 == 1:
            return Square.white if pos[1] % 2 == 1 else Square.black
        else:
            return Square.black if pos[1] % 2 == 1 else Square.white
        

    def delete(self) -> None:
        Renderer.delete(self)
        Input.delete(self)