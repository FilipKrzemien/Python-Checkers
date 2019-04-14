from square import Square


class Piece(Square):
    def __init__(self, position, player):
        Square.__init__(self, position)
        self.player = player

    def move_available(self, other_position, black_turn):
        pass

    def update_position(self, new_position):
        Square.update_position(self, new_position)

    def capture_available(self, other_position, black_turn, l, b):
        pass

    def piece_pressed(self, black_turn):
        if black_turn:
            if self.player == 'C':
                return True
            else:
                return False
        elif not black_turn:
            if self.player == 'B':
                return True
            else:
                return False
