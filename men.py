import math
import tkinter.messagebox
from piece import Piece
from king import King
from game_error_exception import GameErrorException


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
        victim_position = [math.ceil(f1(x1, y1)),
                          math.ceil(f2(x2, y2))]
        if type(l.board[victim_position[0]][victim_position[1]]) == Men or type(
                l.board[victim_position[0]][victim_position[1]]) == King:
            if l.board[victim_position[0]][victim_position[1]].player is not self.player:
                l.captured(victim_position, black_turn, b)
                return True
            else:
                return False

    def update_position(self, new_position):
        Piece.update_position(self, new_position)

    def promotion(self, l):
        l.put_in_board(self.position, self.player)

    def piece_pressed(self, black_turn):
        Piece.piece_pressed(self, black_turn)

