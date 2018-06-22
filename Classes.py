import math
import tkinter.messagebox


class Square:
    def __init__(self, position):
        self.position = position

    def update_position(self, newposition):
        self.position = newposition


class Piece(Square):
    def __init__(self, position, player):
        Square.__init__(self, position)
        self.player = player

    def move_available(self, other_position, black_turn):
        pass

    def update_position(self, newposition):
        Square.update_position(self, newposition)

    def capture_available(self, other_position, black_turn, l, b):
        pass

    def piece_pressed(self, blackturn):
        if blackturn:
            if self.player == 'C':
                return True
            else:
                return False
        elif not blackturn:
            if self.player == 'B':
                return True
            else:
                return False


class Men(Piece):
    def __init__(self, position, player):
        Piece.__init__(self, position, player)

    def move_available(self, other_position, black_turn):
        if black_turn:
            try:
                if other_position[0] != self.position[0] - 1 or abs(self.position[1] - other_position[1]) != 1:
                    raise GameErrorException
            except GameErrorException:
                tkinter.messagebox.showerror("ERROR!", 'Cant Move like that!')
                return False
            return True
        if not black_turn:
            try:
                if other_position[0] != self.position[0] + 1 or abs(self.position[1] - other_position[1]) != 1:
                    raise GameErrorException
            except GameErrorException:
                tkinter.messagebox.showerror("ERROR!", 'Cant Move like that!')
                return False
            return True

    def capture_available(self, other_position, black_turn, l, b):
        if self.player == 'C':
            if other_position[0] > self.position[0]:
                return False
        elif self.player == 'B':
            if other_position[0] < self.position[0]:
                return False
        x1 = self.position[0]
        y1 = other_position[0]
        x2 = self.position[1]
        y2 = other_position[1]
        f1 = lambda x=x1, y=y1: (x + y) / 2
        f2 = lambda x=x2, y=y2: (x + y) / 2
        victimposition = [math.ceil(f1(x1, y1)),
                          math.ceil(f2(x2, y2))]
        if type(l.board[victimposition[0]][victimposition[1]]) == Men or type(
                l.board[victimposition[0]][victimposition[1]]) == King:
            if l.board[victimposition[0]][victimposition[1]].player is not self.player:
                l.captured(victimposition, black_turn, b)
                return True
            else:
                return False

    def update_position(self, newposition):
        Piece.update_position(self, newposition)

    def promotion(self, l):
        l.put_in_board(self.position, self.player)

    def piece_pressed(self, blackturn):
        Piece.piece_pressed(self, blackturn)


class King(Piece):
    def __init__(self, position, player):
        super().__init__(position, player)

    def move_available(self, other_position, black_turn):
        try:
            if abs(other_position[0] - self.position[0]) != 1 and abs(self.position[1] - other_position[1]) != 1:
                raise GameErrorException
        except GameErrorException:
            tkinter.messagebox.showerror("ERROR!", 'Cant Move like that!')
            return False
        return True

    def capture_available(self, other_position, black_turn, l, b):
        x1 = self.position[0]
        y1 = other_position[0]
        x2 = self.position[1]
        y2 = other_position[1]
        f1 = lambda x=x1, y=y1: (x + y) / 2
        f2 = lambda x=x2, y=y2: (x + y) / 2
        victimposition = [math.ceil(f1(x1, y1)),
                          math.ceil(f2(x2, y2))]
        if (type(l.board[victimposition[0]][victimposition[1]]) == Men or type(
                l.board[victimposition[0]][victimposition[1]]) == King) and l.board[victimposition[0]][
            victimposition[1]].player is not self.player:
            l.captured(victimposition, black_turn, b)

            return True
        else:
            return False

    def update_position(self, newposition):
        Piece.update_position(self, newposition)

    def piece_pressed(self, blackturn):
        Piece.piece_pressed(self, blackturn)


class GameErrorException(Exception):
    def __init__(self):
        super().__init__()
