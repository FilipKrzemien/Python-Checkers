import men as men
import square as sq
import king as king


# noinspection PyTypeChecker
class Logic:
    def __init__(self):
        self.board = [[None for i in range(8)] for j in range(8)]
        self.attack = [[False for i in range(8)] for j in range(8)]
        self.fill_board()

    def fill_board(self):
        self.board = [[men.Men([i, j], 'B') if (i < 3 and (i + j) % 2 == 1) else men.Men([i, j], 'C')
                    if (4 < i < 8 and (i + j) % 2 == 1) else sq.Square([i, j]) if ((i + j) % 2 == 1)
                                                    else None for j in range(8)] for i in range(8)]
        
    # tests boards for teacher
    def test1(self):
        # Man at arms
        self.board = [[men.Men([i, j], 'B') if (i == 6 and j == 1) or (i == 1 and j == 2) else men.Men([i, j], 'C')
                                                if i == 2 and j == 1 else sq.Square([i, j]) if ((i + j) % 2 == 1)
                                                                    else None for j in range(8)] for i in range(8)]

    def test2(self):
        # King attack
        self.board = [[men.Men([i, j], 'B') if ((i == 4 and j == 3)or (i == 4 and j == 1)) else king.King([i, j], 'C') if (i == 3 and j == 4)
                        else sq.Square([i, j]) if ((i + j) % 2 == 1) else None for j in range(8)]for i in range(8)]

    def test3(self):
        # Black winner
        self.board = [[men.Men([i, j], 'B') if (i == 1 and j == 2) else men.Men([i, j], 'C')
                                                if i == 2 and j == 1 else sq.Square([i, j]) if ((i + j) % 2 == 1)
                                                                    else None for j in range(8)] for i in range(8)]

    def swap_position(self, position, active_position):
        tmp = self.board[position[0]][position[1]]
        self.board[position[0]][position[1]] = self.board[active_position[0]][active_position[1]]
        self.board[active_position[0]][active_position[1]] = tmp
        self.board[active_position[0]][active_position[1]].update_position(active_position)
        self.board[position[0]][position[1]].update_position(position)

    def captured(self, position, black_turn, buttons):

        self.board[position[0]][position[1]] = sq.Square([position[0], position[1]])
        self.attack[position[0]][position[1]] = True
        if black_turn:

            buttons.white_pawns -= 1
            buttons.get_rid_off_pawn(position)
            if buttons.white_pawns == 0:
                print('Black is victorious!')
                buttons.game_end()
        else:
            buttons.black_pawns -= 1
            buttons.get_rid_off_pawn(position)
            if buttons.black_pawns == 0:
                print('White is victorious!')
                buttons.game_end()

    def put_in_board(self, position, player):
        if player == 'C':
            self.board[position[0]][position[1]] = king.King([position[0], position[1]], 'C')
        else:
            self.board[position[0]][position[1]] = king.King([position[0], position[1]], 'B')

    def clear(self):
        self.attack = [[False for i in range(8)] for j in range(8)]

    def force_attack(self, black_turn):
        for i in range(8):
            for j in range(8):
                if black_turn:
                    if type(self.board[i][j]) == men.Men and self.board[i][j].player == 'C':
                        if j == 0 or j == 1:
                            if self.check_top_right([i, j], 'C'):
                                self.attack[i][j] = True

                        elif j == 7 or j == 6:
                            if self.check_top_left([i, j], 'C'):
                                self.attack[i][j] = True

                        else:
                            if self.check_top_right([i, j], 'C') or self.check_top_left([i, j], 'C'):
                                self.attack[i][j] = True

                    elif type(self.board[i][j]) == men.King and self.board[i][j].player == 'C':
                        if j == 0 or j == 1:
                            if self.check_top_right([i, j], 'C') or self.check_bottom_right([i, j], 'C'):
                                self.attack[i][j] = True

                        elif j == 7 or j == 6:
                            if self.check_top_left([i, j], 'C') or self.check_bottom_left([i, j], 'C'):
                                self.attack[i][j] = True

                        else:
                            if self.check_top_right([i, j], 'C') or self.check_top_left([i, j], 'C') or self.check_bottom_left([i, j], 'C') or self.check_bottom_right([i, j], 'C'):
                                self.attack[i][j] = True

                if not black_turn:
                    if type(self.board[i][j]) == men.Men and self.board[i][j].player == 'B':
                        if j == 0 or j == 1:
                            if self.check_bottom_right([i, j], 'B'):
                                self.attack[i][j] = True

                        elif j == 7 or j == 6:
                            if self.check_bottom_left([i, j], 'B'):
                                self.attack[i][j] = True

                        else:
                            if self.check_bottom_right([i, j], 'B') or self.check_bottom_left([i, j], 'B'):
                                self.attack[i][j] = True

                    elif type(self.board[i][j]) == men.King and self.board[i][j].player == 'B':
                        if j == 0 or j == 1:
                            if self.check_top_right([i, j], 'B') or self.check_bottom_right([i, j], 'B'):
                                self.attack[i][j] = True

                        elif j == 7 or j == 6:
                            if self.check_top_left([i, j], 'B') or self.check_bottom_left([i, j], 'B'):
                                self.attack[i][j] = True

                        else:
                            if self.check_top_right([i, j], 'B') or self.check_top_left([i, j], 'B') or self.check_bottom_left([i, j], 'B') or self.check_bottom_right([i, j], 'B'):
                                self.attack[i][j] = True

    def check_bottom_right(self, position, player):
        if position[0] == 7 or position[0] == 6:
            return False
        if player == 'C':
            if type(self.board[position[0] + 1][position[1] + 1]) == men.Men or type(self.board[position[0] + 1][position[1] + 1]) == king.King:
                if self.board[position[0]+1][position[1]+1].player == 'B':
                    if type(self.board[position[0]+2][position[1]+2]) == sq.Square:
                        self.attack[position[0] + 2][position[1] + 2] = True
                        return True
        elif player == 'B':
            if type(self.board[position[0] + 1][position[1] + 1]) == men.Men or type(self.board[position[0] + 1][position[1] + 1]) == king.King:
                if self.board[position[0]+1][position[1]+1].player == 'C':
                    if type(self.board[position[0]+2][position[1]+2]) == sq.Square:
                        self.attack[position[0] + 2][position[1] + 2] = True
                        return True
        return False

    def check_bottom_left(self, position, player):
        if position[0] == 7 or position[0] == 6:
            return False
        if player == 'C':
            if type(self.board[position[0] + 1][position[1] - 1]) == men.Men or type(self.board[position[0] + 1][position[1] - 1]) == king.King:
                if self.board[position[0]+1][position[1]-1].player == 'B':
                    if type(self.board[position[0]+2][position[1]-2]) == sq.Square:
                        self.attack[position[0] + 2][position[1] - 2] = True
                        return True
        elif player == 'B':
            if type(self.board[position[0] + 1][position[1] - 1]) == men.Men or type(self.board[position[0] + 1][position[1] - 1]) == king.King:
                if self.board[position[0]+1][position[1]-1].player == 'C':
                    if type(self.board[position[0]+2][position[1]-2]) == sq.Square:
                        self.attack[position[0] + 2][position[1] - 2] = True
                        return True
        return False

    def check_top_right(self, position, player):
        if position[0] == 0 or position[0] == 1:
            return False
        if player == 'C':
            if type(self.board[position[0] - 1][position[1] + 1]) == men.Men or type(self.board[position[0] - 1][position[1] + 1]) == king.King:
                if self.board[position[0]-1][position[1]+1].player == 'B':
                    if type(self.board[position[0]-2][position[1]+2]) == sq.Square:
                        self.attack[position[0] - 2][position[1] + 2] = True
                        return True
        elif player == 'B':
            if type(self.board[position[0] - 1][position[1] + 1]) == men.Men or type(self.board[position[0] - 1][position[1] + 1]) == king.King:
                if self.board[position[0]-1][position[1]+1].player == 'C':
                    if type(self.board[position[0]-2][position[1]+2]) == sq.Square:
                        self.attack[position[0] - 2][position[1] + 2] = True
                        return True
        return False

    def check_top_left(self, position, player):
        if position[0] == 0 or position[0] == 1:
            return False
        if player == 'C':
            if type(self.board[position[0] - 1][position[1] - 1]) == men.Men or type(self.board[position[0] - 1][position[1] - 1]) == king.King:
                if self.board[position[0]-1][position[1]-1].player == 'B':
                    if type(self.board[position[0]-2][position[1]-2]) == sq.Square:
                        self.attack[position[0] - 2][position[1] - 2] = True
                        return True
        elif player == 'B':
            if type(self.board[position[0] - 1][position[1] - 1]) == men.Men or type(self.board[position[0] - 1][position[1] - 1]) == king.King:
                if self.board[position[0] - 1][position[1] - 1].player == 'C':
                    print(player)
                    if type(self.board[position[0]-2][position[1]-2]) == sq.Square:
                        self.attack[position[0] - 2][position[1] - 2] = True
                        return True
        return False

    def check_next_attack(self, position, black_turn):
        if black_turn:
            if type(self.board[position[0]][position[1]]) == men.Men and self.board[position[0]][position[1]].player == 'C':
                if position[1] == 0 or position[1] == 1:
                    if self.check_top_right(position, 'C'):
                        return True
                elif position[1] == 7 or position[1] == 6:
                    if self.check_top_left(position, 'C'):
                        return True
                else:
                    if self.check_top_right(position, 'C') or self.check_top_left(position, 'C'):
                        return True

            elif type(self.board[position[0]][position[1]]) == men.King and self.board[position[0]][position[1]].player == 'C':
                if position[1] == 0 or position[1] == 1:
                    if self.check_top_right(position, 'C') or self.check_bottom_right(position, 'C'):
                        return True
                elif position[1] == 7 or position[1] == 6:
                    if self.check_top_left(position, 'C') or self.check_bottom_left(position, 'C'):
                        return True
                else:
                    if self.check_top_right(position, 'C') or self.check_top_left(position, 'C') or self.check_bottom_left(position, 'C') or self.check_bottom_right(position, 'C'):
                        return True
        elif not black_turn:
            if type(self.board[position[0]][position[1]]) == men.Men and self.board[position[0]][position[1]].player == 'B':
                if position[1] == 0 or position[1] == 1:
                    if self.check_bottom_right(position, 'B'):
                        return True
                elif position[1] == 7 or position[1] == 6:
                    if self.check_bottom_left(position, 'B'):
                        return True
                else:
                    if self.check_bottom_right(position, 'B') or self.check_bottom_left(position, 'B'):
                        return True

            elif type(self.board[position[0]][position[1]]) == men.King and self.board[position[0]][position[1]].player == 'B':
                if position[1] == 0 or position[1] == 1:
                    if self.check_top_left(position, 'B') or self.check_bottom_right(position, 'B'):
                        return True
                elif position[1] == 7 or position[1] == 6:
                    if self.check_top_left(position, 'B') or self.check_bottom_left(position, 'B'):
                        return True
                else:
                    if self.check_top_right(position, 'B') or self.check_top_left(position, 'B') or self.check_bottom_left(position, 'B') or self.check_bottom_right(position, 'B'):
                        return True
