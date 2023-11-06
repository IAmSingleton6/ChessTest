# 0 black, 1 white

#  W    B
# 0001 0000 -> Nothing
# 0011 0010 -> Pawn
# 0101 0100 -> Castle
# 0111 0110 -> Knight
# 1001 1000 -> Bishop
# 1011 1010 -> Queen
# 1101 1100 -> King
class Piece:
        NA = 0b0000
        bP = 0b0010
        wP = 0b0011
        bR = 0b0100
        wR = 0b0101
        bN = 0b0110
        wN = 0b0111
        bB = 0b1000
        wB = 0b1001
        bQ = 0b1010
        wQ = 0b1011
        bK = 0b1100
        wK = 0b1101