from abc import abstractmethod
from pygame import image, transform
from pygame.mouse import get_pos
from components import Renderer

class BaseUnit(Renderer):
    black_image_path = None
    white_image_path = None
    base_z_index = 1

    def __init__(self, is_white: bool, square_size: tuple) -> None:
        self.is_white: bool = is_white
        self.image_size: tuple = square_size
        self.set_z_index(self.base_z_index)
        self._piece_held: bool = False
        self.material_value = 1
        image_path = self.white_image_path if is_white else self.black_image_path
        img = image.load(image_path)
        self.image = transform.scale(img,(self.image_size[0], self.image_size[1]))   #resize image


    def is_white(self) -> bool:
        return self.is_White
    
    # Use mouse to move piece around
    def pickup_piece(self, pickup: bool) -> None:
        if pickup:
            self._piece_held = True
            self.set_z_index(self.base_z_index + 1)
        else:
            self._piece_held = False
            self.set_z_index(self.base_z_index)


    def is_piece_held(self) -> bool:
        return self._piece_held



    def set_image_position(self, center_pos: tuple) -> None:
        # Pygame draws from top left origin, so center the image
        self.image_position = (center_pos[0] - (0.5 * self.image_size[0]), center_pos[1] - (0.5 * self.image_size[1]))


    # Return all positions where the piece can move
    @abstractmethod
    def moveable_squares(self, pos, board): 
        return NotImplementedError
    
    # For each direction, eg for bishops and rooks
    # Return all valid moves from each direction 
    def filter_directions(self, board, *directions: list) -> list:
        output = []

        for direction in directions:
            for square in direction:
                piece = square.piece
                if piece is None:
                    output.append(square)
                    continue
                if piece.is_white != self.is_white:
                    output.append(square)
                break

        return output
    
    # For each move, determine whether it is valid
    def filter_moves(self, board, moves: list) -> list:
        output = []

        for square in moves:
            piece = square.piece
            if piece is None or piece.is_white != self.is_white:
                output.append(square)

        return output
                

    def draw(self, window) -> None:
        if self.image != None:
            if self._piece_held:
                self.z_index = self.base_z_index + 1
                mouse_pos = get_pos()
                window.blit(self.image, (mouse_pos[0] - (0.5 * self.image_size[0]), mouse_pos[1] - (0.5 * self.image_size[1])))
            else:
                self.z_index = self.base_z_index 
                window.blit(self.image, (self.image_position[0], self.image_position[1]))
    