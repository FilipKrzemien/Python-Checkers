import math
import tkinter.messagebox
import men as mn
from piece import Piece
from game_error_exception import GameErrorException



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
        victim_position = [math.ceil(f1(x1, y1)),
                          math.ceil(f2(x2, y2))]
        if (type(l.board[victim_position[0]][victim_position[1]]) == mn.Men or type(
                l.board[victim_position[0]][victim_position[1]]) == King) and l.board[victim_position[0]][
            victim_position[1]].player is not self.player:
            l.captured(victim_position, black_turn, b)

            return True
        else:
            return False

    def update_position(self, new_position):
        Piece.update_position(self, new_position)

    def piece_pressed(self, black_turn):
        Piece.piece_pressed(self, black_turn)
