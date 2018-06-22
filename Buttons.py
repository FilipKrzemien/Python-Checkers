import tkinter as tk
import Classes as Cl
import tkinter.messagebox
from pygame import mixer
import winsound
# noinspection PyTypeChecker,PyUnusedLocal,PyDefaultArgument


class Buttons(tk.Frame):

    def __init__(self, root, l):
        tk.Frame.__init__(self, root)
        self.__root = root
        self.__root.title('Checkers')
        self.pack(fill="both", expand=1)
        self.black_pawns = 12
        self.white_pawns = 12
        self.__header = tk.Label(self, text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(self.white_pawns) + " - White Pawns",
                                 background='white', bd=5)
        self.__header.pack(side="top", fill="both")
        self.__special_buttons = tk.Frame(self, bg="")
        self.__special_buttons.pack(side="right", fill="both", expand=0)
        self.__board_frame = tk.Frame(self, background="")
        self.__board_frame.pack(side="left", fill="both", expand=True)
        self.__Black_turn = True
        self.__logic = l
        self.__active = None
        self.__specials = [None for i in range(5)]
        # noinspection PyUnusedLocal
        self.__buttons = [[None for i in range(8)] for j in range(8)]
        self.__end = False
        self.draw()
        self.draw_specials()

    def draw(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self.__logic.board[i][j], Cl.Men) and self.__logic.board[i][j].player == 'C':
                    self.__buttons[i][j] = tk.Button(self.__board_frame, height=4, width=10, bg="bisque", text='C',
                                                     command=lambda position=[i, j]: self.pawn_pressed(position))
                    self.__buttons[i][j].grid(row=i, column=j)
                elif isinstance(self.__logic.board[i][j], Cl.King) and self.__logic.board[i][j].player == 'C':
                    self.__buttons[i][j] = tk.Button(self.__board_frame, height=4, width=10, bg="bisque", text='Cd',
                                                     command=lambda position=[i, j]: self.pawn_pressed(position))
                    self.__buttons[i][j].grid(row=i, column=j)
                elif isinstance(self.__logic.board[i][j], Cl.Men) and self.__logic.board[i][j].player == 'B':
                    self.__buttons[i][j] = tk.Button(self.__board_frame, height=4, width=10, bg="bisque", text='B',
                                                     command=lambda position=[i, j]: self.pawn_pressed(position))
                    self.__buttons[i][j].grid(row=i, column=j)
                elif isinstance(self.__logic.board[i][j], Cl.King) and self.__logic.board[i][j].player == 'B':
                    self.__buttons[i][j] = tk.Button(self.__board_frame, height=4, width=10, bg="bisque", text='Bd',
                                                     command=lambda position=[i, j]: self.pawn_pressed(position))
                    self.__buttons[i][j].grid(row=i, column=j)
                elif isinstance(self.__logic.board[i][j], Cl.Square):
                    self.__buttons[i][j] = tk.Button(self.__board_frame, height=4, width=10, bg="bisque", text="",
                                                     command=lambda position=[i, j]: self.square_pressed(position))
                    self.__buttons[i][j].grid(row=i, column=j)
                else:
                    self.__buttons[i][j] = tk.Button(self.__board_frame, height=4, width=10, bg="green", text="", state='disabled')
                    self.__buttons[i][j].grid(row=i, column=j)

    def draw_specials(self):
            self.__specials[0] = tk.Button(self.__special_buttons, height=4, width=10, text="RESET", bg="red",
                                           command=lambda: self.game_reset())
            self.__specials[0].grid(row=0, column=1)

            self.__specials[1] = tk.Button(self.__special_buttons, height=4, width=10, text="Test nr.1",
                                           command=lambda: self.test1())
            self.__specials[1].grid(row=0, column=2)

            self.__specials[2] = tk.Button(self.__special_buttons, height=4, width=10, text="Test nr.2",
                                           command=lambda: self.test2())
            self.__specials[2].grid(row=0, column=3)

            self.__specials[3] = tk.Button(self.__special_buttons, height=4, width=10, text="Test nr.3",
                                           command=lambda: self.test3())
            self.__specials[3].grid(row=0, column=4)

            self.__specials[4] = tk.Button(self.__special_buttons, height=4, width=10, text="Exit",
                                   command=lambda: exit())
            self.__specials[4].grid(row=0, column=5)

    def game_reset(self):
        self.black_pawns = 12
        self.white_pawns = 12
        self.__Black_turn = True
        self.__active = None
        self.__end = False
        self.__logic.board = [[None for i in range(8)] for j in range(8)]
        self.__buttons = [[None for i in range(8)] for j in range(8)]
        self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(self.white_pawns) + " - White Pawns")
        # noinspection PyUnusedLocal
        self.__logic.fill_board()
        self.draw()

    def test1(self):
        self.white_pawns = 2
        self.black_pawns = 1
        self.__Black_turn = True
        self.__active = None
        self.__end = False
        self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(self.white_pawns) + " - White Pawns")
        self.__logic.test1()
        self.draw()

    def test2(self):
        self.white_pawns = 2
        self.black_pawns = 1
        self.__Black_turn = True
        self.__active = None
        self.__end = False
        self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(
            self.white_pawns) + " - White Pawns")
        self.__logic.test2()
        self.draw()

    def test3(self):
        self.white_pawns = 1
        self.black_pawns = 1
        self.__Black_turn = True
        self.__active = None
        self.__end = False
        self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(
            self.white_pawns) + " - White Pawns")
        self.__logic.test3()
        self.draw()

    def pawn_pressed(self, position):
        if self.__Black_turn:
            try:
                if self.__buttons[position[0]][position[1]].cget('text') == 'B' or self.__buttons[position[0]][position[1]].cget('text') == 'Bd':
                    raise Cl.GameErrorException
            except Cl.GameErrorException:
                tkinter.messagebox.showerror("ERROR!", 'ITS NOT YOUR PIECE!')
                return
        elif not self.__Black_turn:
            try:
                if self.__buttons[position[0]][position[1]].cget('text') == 'C' or self.__buttons[position[0]][position[1]].cget('text') == 'Cd':
                    raise Cl.GameErrorException
            except Cl.GameErrorException:
                tkinter.messagebox.showerror("ERROR!", 'ITS NOT YOUR PIECE!')
                return

        if self.__active is None:
            self.__active = position
            active_button_text = '[{}]'.format(self.__buttons[position[0]][position[1]]['text'])
            self.__buttons[position[0]][position[1]].configure(text=active_button_text)

        elif self.__active is not None:
            position2 = self.__active
            if self.__Black_turn:
                active_button_text = 'C'
                if type(self.__logic.board[position2[0]][position2[1]]) == Cl.King:
                    active_button_text = 'Cd'
            elif not self.__Black_turn:
                active_button_text = 'B'
                if type(self.__logic.board[position2[0]][position2[1]]) == Cl.King:
                    active_button_text = 'Bd'

            self.__buttons[position2[0]][position2[1]].configure(text=active_button_text)
            self.__active = position
            active_button_text = '[{}]'.format(self.__buttons[position[0]][position[1]]['text'])
            self.__buttons[position[0]][position[1]].configure(text=active_button_text)

    def square_pressed(self, position):
        blackturn = self.__Black_turn
        active_position = self.__active
        if self.__active is None:
            pass
        else:
            if type(self.__logic.board[position[0]][position[1]]) == Cl.Square:
                if 0 <= position[1] <= 7:
                    if self.__logic.board[active_position[0]][active_position[1]].capture_available(position, blackturn, self.__logic, self):
                        self.swap_buttons(position, blackturn, active_position)
                        if not self.__end:
                            winsound.Beep(1000, 50)
                        if self.__end:
                            if self.__Black_turn:
                                self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(self.white_pawns) + " - White Pawns")
                            elif not self.__Black_turn:
                                self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  White Player Turn  " + str(self.white_pawns) + " - White Pawns")
                            return

                        self.__logic.clear()
                        if not self.__logic.check_next_attack(position, blackturn):
                            self.__Black_turn = not self.__Black_turn
                            blackturn = self.__Black_turn
                            if self.__Black_turn:
                                self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(self.white_pawns) + " - White Pawns")
                            elif not self.__Black_turn:
                                self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  White Player Turn  " + str(self.white_pawns) + " - White Pawns")
                        self.__logic.force_attack(blackturn)
                        self.turn_off_buttons()
                        return
                    elif self.__logic.board[active_position[0]][active_position[1]].move_available(position, blackturn):
                        self.swap_buttons(position, blackturn, active_position)
                        self.__logic.clear()
                        self.__Black_turn = not self.__Black_turn
                        blackturn = self.__Black_turn
                        if self.__Black_turn:
                            self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  Black Player Turn  " + str(self.white_pawns) + " - White Pawns")
                        elif not self.__Black_turn:
                            self.__header.config(text="Black Pawns - " + str(self.black_pawns) + "  White Player Turn  " + str(self.white_pawns) + " - White Pawns")
                        self.__logic.force_attack(blackturn)
                        self.turn_off_buttons()
                        return

    def swap_buttons(self, position, blackturn, active_position):
        self.__logic.swap_position(position, active_position)
        if blackturn:
            if type(self.__logic.board[position[0]][position[1]]) == Cl.King:
                self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text='Cd',
                                                    command=lambda position=position: self.pawn_pressed(position))

                self.__buttons[self.__active[0]][self.__active[1]].config(height=4, width=10, bg="bisque", text="",
                            command=lambda position=[self.__active[0], self.__active[1]]: self.square_pressed(position))
                self.__active = None
                return
            else:
                if position[0] == 0:
                    self.__logic.board[position[0]][position[1]].promotion(self.__logic)
                    self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text='Cd',
                                                        command=lambda position=position: self.pawn_pressed(position))
                    self.__buttons[self.__active[0]][self.__active[1]].config(height=4, width=10, bg="bisque", text="",
                                command=lambda position=[self.__active[0], self.__active[1]]: self.square_pressed(position))
                    self.__active = None
                    return
                else:
                    self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text='C',
                                                    command=lambda position=position: self.pawn_pressed(position))
                    self.__buttons[self.__active[0]][self.__active[1]].config(height=4, width=10, bg="bisque", text="",
                                command=lambda position=[self.__active[0], self.__active[1]]: self.square_pressed(position))
                    self.__active = None
                    return
        else:
            if type(self.__logic.board[position[0]][position[1]]) == Cl.King:
                self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text='Bd',
                                                    command=lambda position=position: self.pawn_pressed(position))
                self.__buttons[self.__active[0]][self.__active[1]].config(height=4, width=10, bg="bisque", text="",
                                command=lambda position=[self.__active[0], self.__active[1]]: self.square_pressed(position))
                self.__active = None
                return
            else:
                if position[0] == 7:
                    self.__logic.board[position[0]][position[1]].promotion(self.__logic)
                    self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text='Bd',
                                                    command=lambda position=position: self.pawn_pressed(position))
                    self.__buttons[self.__active[0]][self.__active[1]].config(height=4, width=10, bg="bisque", text="",
                                 command=lambda position=[self.__active[0], self.__active[1]]: self.square_pressed(position))
                    self.__active = None
                    return
                else:
                    self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text='B',
                                                        command=lambda position=position: self.pawn_pressed(position))
                    self.__buttons[self.__active[0]][self.__active[1]].config(height=4, width=10, bg="bisque", text="",
                                command=lambda position=[self.__active[0], self.__active[1]]: self.square_pressed(position))
                    self.__active = None
                    return

    def get_rid_off_pawn(self, position):
        self.__buttons[position[0]][position[1]].config(height=4, width=10, bg="bisque", text="",
                                    command=lambda position=[position[0], position[1]]: self.square_pressed(position))

    def game_end(self):
        mixer.music.play()
        for i in range(8):
            for j in range(8):
                self.__buttons[i][j].config(state='disabled')
        self.__end = True
        if self.__Black_turn:
            end_window = tk.messagebox.showinfo('The Game has ended', 'Black is victorious!')
        elif not self.__Black_turn:
            if self.__Black_turn:
                end_window = tk.messagebox.showinfo('The Game has ended', 'White is victorious!')

    def turn_off_buttons(self):
        for i in range(8):
            for j in range(8):
                if not self.__logic.attack[i][j]:
                    self.__buttons[i][j].config(state='disabled')
                else:
                    self.__buttons[i][j].config(state='normal')
        tmp = False
        for i in range(8):
            for j in range(8):
                if self.__logic.attack[i][j] is not self.__logic.attack[0][0]:
                    tmp = not tmp
                    break
            if tmp:
                break
        else:
            for i in range(8):
                for j in range(8):
                    if type(self.__logic.board[i][j]) == Cl.Men or type(self.__logic.board[i][j]) == Cl.King or type(
                            self.__logic.board[i][j]) == Cl.Square:
                        self.__buttons[i][j].config(state='normal')
