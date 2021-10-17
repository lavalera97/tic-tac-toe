from abc import ABC, abstractmethod
import tkinter as tk
from winning_conditions import winning_conditions
import random


class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TicTacToe 10x10')
        self._main_canvas = None
        self.switch_canvas(StartPage)

    def switch_canvas(self, canvas_class):
        """Initializing func to switch between canvases / Создаём функцию для смены работающего окна"""
        if self._main_canvas:
            self._main_canvas.pack_forget()
        canvas = canvas_class(self)
        self._main_canvas = canvas


class StartPage(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        """Creating starting page / Начальная страница"""
        super().__init__(master, *args, **kwargs)
        self.pack(pady=25, padx=30)
        tk.Label(self, text="TIC-TAC-TOE", font=('Segoe Print', 20, 'bold')).grid(column=0, row=0, pady=5, padx=30)
        tk.Button(self, text="Player vs Player", font=('Segoe Print', 15, 'bold'), bg='white',
                  command=lambda: master.switch_canvas(PlayerVsPlayer)).grid(column=0, row=1, pady=2)
        tk.Button(self, text="Player vs AI", font=('Segoe Print', 15, 'bold'), bg='white',
                  command=lambda: master.switch_canvas(PlayerVsAi)).grid(column=0, row=2, pady=2)
        tk.Button(self, text="Player vs AI reverse", font=('Segoe Print', 15, 'bold'), bg='white',
                  command=lambda: master.switch_canvas(PlayerVsAiReverse)).grid(column=0, row=3, pady=2)
        tk.Button(self, text="Exit", font=('Segoe Print', 15, 'bold'), bg='white',
                  command=master.destroy).grid(column=0, row=4, pady=2)


class CreateBoard(tk.Canvas, ABC):
    def __init__(self, master, *args, **kwargs):
        """Setting our base board to play with/ Создаём поле для игры"""
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack(pady=(20, 60), padx=40)
        self.player_one = ''
        self.player_two = ''
        self.who_plays = ''
        self.board = {}
        self.buttons = []
        self.create_buttons()
        self.create_board()
        self.move_label = tk.Label(self, text="Choose side!", font=('Segoe Print', 20, 'bold'), bd=4)
        self.move_label.grid(column=10, row=4, columnspan=2, padx=(32, 0))
        self.name_label = tk.Label(self, text="", font=('Segoe Print', 20, 'bold'), bd=4)
        self.name_label.grid(column=0, row=0, columnspan=10, pady=(0, 20))
        self.restart = tk.Button(self, text="Restart", font=('Segoe Print', 14, 'bold'),
                                 bg='white', width=10, bd=4, state=tk.DISABLED)
        self.restart.grid(column=10, row=8, columnspan=2, padx=(30, 0))
        self.main_button = tk.Button(self, text="Main menu", font=('Segoe Print', 14, 'bold'), bd=4, bg='white',
                                     width=10, command=lambda: master.switch_canvas(StartPage))
        self.main_button.grid(column=10, row=9, rowspan=2, columnspan=2, padx=(30, 0))
        self.all_winning_conditions = winning_conditions

    def create_board(self):
        for i in range(100):
            self.board[i] = ''

    def create_buttons(self):
        x = 0
        for i in range(10):
            for n in range(10):
                self.buttons.append(x)
                self.buttons[x] = tk.Button(
                    self, text='', bd=4, height=1, width=4, font=("Segoe Print", 14, 'bold'),
                    state=tk.DISABLED, command=lambda x=x: self.make_move(x))
                self.buttons[x].grid(row=i + 1, column=n)
                x += 1

    def check_winner_conditions(self):
        """Checking if player or bot won / Проверяем возможность выигрыша игрока или бота"""
        win = False
        for condition in self.all_winning_conditions:
            not_empty = all(self.board[ele] != '' for ele in condition)
            x_sign = all(self.board[ele] == 'X' for ele in condition)
            o_sign = all(self.board[ele] == 'O' for ele in condition)
            if not_empty and (x_sign or o_sign):
                win = True
                self.move_label['text'] = f'{self.who_plays}\nwins!'
                for i in condition:
                    self.buttons[i].configure(bg='#b7e4c7')
                break
        return win

    def check_draw(self):
        """Checking if it's draw or not / Проверяем не закончилась ли игра ничьей"""
        draw = False
        x = [k for k, v in self.board.items() if v == '']
        if not x:
            draw = True
            self.move_label['text'] = f"It's Draw!"
        return draw

    def check_play_state(self):
        """Disable all buttons in case current player won or it's tie. Рассматриваем положение в игре,
        если игрок выигрывает или наступает ничья, отключаем все кнопки на поле
        """
        check_win = self.check_winner_conditions()
        check_draw = self.check_draw()

        endgame = False
        if check_win:
            for i in self.buttons:
                i.configure(command=lambda: None)
                endgame = True
        elif check_draw:
            for i in self.buttons:
                i.configure(command=lambda: None)
                endgame = True
        return endgame

    @abstractmethod
    def start_game(self, sign):
        pass

    @abstractmethod
    def make_move(self, button_number):
        pass


class PlayerVsPlayer(CreateBoard):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name_label['text'] = 'Player Vs Player'
        self.player_one = 'First Player'
        self.player_two = 'Second Player'
        self.start_game('x')

    def start_game(self, sign):
        """Make board available to play / Включаем работу кнопок и начинаем игру"""
        for i in self.buttons:
            i['state'] = tk.NORMAL
        self.who_plays = self.player_one
        self.restart.configure(command=lambda: self.master.switch_canvas(PlayerVsPlayer))
        self.move_label['text'] = f'{self.who_plays}\nturn'
        self.move_label.grid(column=10, row=4, rowspan=2, padx=(32, 0))
        self.restart['state'] = tk.NORMAL

    def make_move(self, button_number):
        """Checking if it's allowed to make a move to certain position. Disable all buttons in case current player won
        Проверяем не занята ли нужная ячейка. Изменяем ее и проверяем не выиграл ли текущий игрок.
        """
        if self.buttons[button_number]['text'] != '':
            pass
        else:
            if self.who_plays == self.player_one:
                self.buttons[button_number]['text'] = 'X'
                self.buttons[button_number]['fg'] = 'red'
                self.board[button_number] = 'X'
            else:
                self.buttons[button_number]['text'] = 'O'
                self.buttons[button_number]['fg'] = 'blue'
                self.board[button_number] = 'O'
            x = self.check_play_state()
            if not x:
                if self.who_plays == self.player_one:
                    self.who_plays = self.player_two
                else:
                    self.who_plays = self.player_one
                self.move_label['text'] = f'{self.who_plays}\nturn'


class PlayerVsAiBaseSettings(CreateBoard, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_one = 'Player'
        self.player_two = 'AI'
        self.player_sign = ''
        self.ai_sign = ''
        self.move_label['text'] = 'Choose side!'
        self.bot_dict = {}
        self.player_dict = {}
        self.all_data = {}
        self.button = 0
        self.x_button = tk.Button(self, text="X", font=('Segoe Print', 13, 'bold'), bg='white', height=0, width=4,
                                  bd=4, command=lambda: self.start_game('X'), fg="red")
        self.x_button.grid(column=10, row=5, padx=(30, 0))
        self.o_button = tk.Button(self, text="O", font=('Segoe Print', 13, 'bold'), bg='white', height=0, width=4,
                                  bd=4, command=lambda: self.start_game('O'), fg="blue")
        self.o_button.grid(column=11, row=5, padx=(30, 0))

    def start_game(self, sign):
        """Allowing player to choose a sign to play with / Даём игроку выбор за какой знак он хочет начать играть"""
        for i in self.buttons:
            i['state'] = tk.NORMAL
        self.x_button.grid_forget()
        self.o_button.grid_forget()
        self.restart['state'] = tk.NORMAL
        self.move_label.grid(column=10, row=4, rowspan=2, columnspan=2, padx=(32, 0))
        if sign == 'X':
            self.player_sign = 'X'
            self.ai_sign = 'O'
            self.who_plays = self.player_one
        if sign == 'O':
            self.player_sign = 'O'
            self.ai_sign = 'X'
            self.who_plays = self.player_two
            self.ai_move()
        self.move_label['text'] = f'Good luck!'

    def make_move(self, button_number):
        """Make move using buttons and then allow bot to make his move
        Код для кнопок, проверки окончена игра или нет, а так же передачи хода боту
        """
        if self.buttons[button_number]['text'] != '':
            pass
        else:
            if self.who_plays == self.player_one:
                if self.player_sign == 'X':
                    self.buttons[button_number]['text'] = 'X'
                    self.buttons[button_number]['fg'] = 'red'
                    self.board[button_number] = 'X'
                else:
                    self.buttons[button_number]['text'] = 'O'
                    self.buttons[button_number]['fg'] = 'blue'
                    self.board[button_number] = 'O'
            else:
                if self.ai_sign == 'X':
                    self.buttons[button_number]['text'] = 'X'
                    self.buttons[button_number]['fg'] = 'red'
                    self.board[button_number] = 'X'
                else:
                    self.buttons[button_number]['text'] = 'O'
                    self.buttons[button_number]['fg'] = 'blue'
                    self.board[button_number] = 'O'
            x = self.check_play_state()
            if not x:
                if self.who_plays == self.player_one:
                    self.who_plays = self.player_two
                    self.ai_move()
                else:
                    self.who_plays = self.player_one
            self.check_play_state()

    def ai_win_conditions(self):
        """Storing information about current board situation in bot and played dicts
         Собираем информацию о положении игры на данный момент, сохраняем ее в словари для дальнейшей работы бота
         """
        for condition in self.all_winning_conditions:
            x_sign = 0
            o_sign = 0
            empty = 0

            for i in condition:
                if self.board[i] == 'X':
                    x_sign += 1
                elif self.board[i] == 'O':
                    o_sign += 1
                elif self.board[i] == '':
                    empty += 1
            self.all_data[self.all_winning_conditions.index(condition)] = {
                'X': x_sign,
                'O': o_sign,
                '': empty
            }
        for i in range(6):
            self.bot_dict[i] = [self.all_winning_conditions[k] for k, v in self.all_data.items() if v[self.player_sign] < 1 and v[self.ai_sign] == i]

            self.player_dict[i] = [self.all_winning_conditions[k] for k, v in self.all_data.items() if v[self.ai_sign] < 1 and v[self.player_sign] == i]

    @abstractmethod
    def ai_move(self):
        pass


class PlayerVsAi(PlayerVsAiBaseSettings):

    # @staticmethod
    # def minimax(board, ai_sign, player_sign, is_maximizing, depth):
    #
    #     def check_winner(mark):
    #         win = False
    #         for condition in winning_conditions:
    #             not_empty = all(board[ele] != '' for ele in condition)
    #             sign = all(board[ele] == mark for ele in condition)
    #             if not_empty and sign:
    #                 win = True
    #                 break
    #         return win
    #
    #     def check_draw():
    #         """Checking if it's draw or not / Проверяем не закончилась ли игра ничьей"""
    #         draw = False
    #         if '' not in board.values():
    #             draw = True
    #         return draw
    #
    #     if check_winner(ai_sign):
    #         return 100
    #     elif check_winner(player_sign):
    #         return -100
    #     elif check_draw():
    #         return 0
    #     elif depth == 0:
    #         return 0
    #
    #     if is_maximizing:
    #         best_score = -1000
    #
    #         for key in board.keys():
    #             if board[key] == '':
    #                 board[key] = ai_sign
    #                 score = PlayerVsAi.minimax(board, ai_sign, player_sign, False, depth - 1)
    #                 board[key] = ''
    #                 if score > best_score:
    #                     best_score = score
    #         return best_score
    #     else:
    #         best_score = 800
    #         for key in board.keys():
    #             if board[key] == '':
    #                 board[key] = player_sign
    #                 score = PlayerVsAi.minimax(board, ai_sign, player_sign, True, depth - 1)
    #                 board[key] = ''
    #                 if score < best_score:
    #                     best_score = score
    #         return best_score

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.restart.configure(command=lambda: self.master.switch_canvas(PlayerVsAi))
        self.name_label['text'] = 'Player Vs AI'

    def ai_move(self):
        """Implementing AI (commented code is for minimax algorithm) to place 5 signs in a row
         Прописываем поведение бота, чтобы он поставил 5 знаков в одну линию
         """
        if all(self.board[i] == '' for i in range(100)):
            random_numbers = [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66]
            self.button = random.choice(random_numbers)
            self.buttons[self.button].invoke()
        else:
            self.ai_win_conditions()
            if self.bot_dict[0] == self.bot_dict[1] == self.bot_dict[2] == self.bot_dict[3] == self.bot_dict[4] == [] \
                    and self.player_dict[0] == self.player_dict[1] == self.player_dict[2] == self.player_dict[3] == self.player_dict[4] == []:
                spaces_left = [k for k, v in self.board.items() if v == '']
                self.button = random.choice(spaces_left)

            elif len(self.bot_dict[4]) > 0:
                for i in self.bot_dict[4]:
                    for j in i:
                        if self.board[j] == '':
                            self.button = j
                            break

            elif len(self.player_dict[4]) > 1:
                multiple_moves = [i for i in self.player_dict[4]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    multiple_moves = [i for i in self.player_dict[4]]
                    for i in self.player_dict[3]:
                        multiple_moves.append(i)
                    cross_cells = list(set(multiple_moves.pop()).intersection(*map(set, multiple_moves)))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        for i in self.player_dict[4]:
                            for j in i:
                                if self.board[j] == '':
                                    self.button = j
                                    break

            elif len(self.player_dict[4]) > 0:
                for i in self.player_dict[4]:
                    for j in i:
                        if self.board[j] == '':
                            self.button = j
                            break

            elif len(self.bot_dict[3]) < len(self.player_dict[3]):
                multiple_moves = [i for i in self.player_dict[3]]
                moves_without_values = []
                for i in multiple_moves:
                    if self.board[i[0]] == self.board[i[4]] == '':
                        moves_without_values.append(i)
                if moves_without_values:
                    self.button = moves_without_values[0][0]
                else:
                    multiple_moves = [i for i in self.player_dict[3]]
                    moves_without_values = []
                    for i in multiple_moves:
                        for j in i:
                            if self.board[j] == '':
                                moves_without_values.append(j)
                    cross_cells = list(set(moves_without_values))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        changed = False
                        for i in self.bot_dict[3]:
                            for j in i[1:3]:
                                if self.board[j] == '':
                                    changed = True
                                    self.button = j
                                    break
                            if not changed:
                                for j in i:
                                    if self.board[j] == '':
                                        changed = True
                                        self.button = j
                                        break

            elif len(self.bot_dict[3]) > 1 > len(self.player_dict[3]):
                multiple_moves = [i for i in self.bot_dict[3]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    multiple_moves = [i for i in self.bot_dict[3]]
                    for i in self.bot_dict[2]:
                        multiple_moves.append(i)
                    moves_without_values = []
                    for i in multiple_moves:
                        for j in i:
                            if self.board[j] == '':
                                moves_without_values.append(j)
                    cross_cells = list(set(moves_without_values))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        for i in self.bot_dict[3]:
                            for j in i:
                                if self.board[j] == '':
                                    self.button = j
                                    break

            elif len(self.bot_dict[3]) > 0 and len(self.player_dict[3]) > 0:
                cells_bot = [i for i in self.bot_dict[3]]
                cells_player = [i for i in self.player_dict[3]]
                all_cells = cells_bot + cells_player
                moves_without_values = []
                for i in all_cells:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    changed = False
                    for i in self.bot_dict[3]:
                        for j in i[1:3]:
                            if self.board[j] == '':
                                changed = True
                                self.button = j
                                break
                        if not changed:
                            for j in i:
                                if self.board[j] == '':
                                    changed = True
                                    self.button = j
                                    break

            elif len(self.bot_dict[2]) < 1 < len(self.player_dict[2]):
                multiple_moves = [i for i in self.player_dict[2]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    multiple_moves = [i for i in self.player_dict[2]]
                    for i in self.player_dict[1]:
                        multiple_moves.append(i)
                    moves_without_values = []
                    for i in multiple_moves:
                        for j in i:
                            if self.board[j] == '':
                                moves_without_values.append(j)
                    cross_cells = list(set(moves_without_values))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        for i in self.player_dict[2]:
                            for j in i:
                                if self.board[j] == '':
                                    self.button = j
                                    break

            elif len(self.bot_dict[2]) > 1 > len(self.player_dict[2]):
                multiple_moves = [i for i in self.bot_dict[2]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    multiple_moves = [i for i in self.bot_dict[2]]
                    for i in self.bot_dict[1]:
                        multiple_moves.append(i)
                    moves_without_values = []
                    for i in multiple_moves:
                        for j in i:
                            if self.board[j] == '':
                                moves_without_values.append(j)
                    cross_cells = list(set(moves_without_values))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        for i in self.bot_dict[2]:
                            for j in i:
                                if self.board[j] == '':
                                    self.button = j
                                    break

            elif len(self.bot_dict[2]) > 0 and len(self.player_dict[2]) > 0:
                cells_bot = [i for i in self.bot_dict[2]]
                cells_player = [i for i in self.player_dict[2]]
                all_cells = cells_bot + cells_player
                moves_without_values = []
                for i in all_cells:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    for i in self.bot_dict[2]:
                        for j in i:
                            if self.board[j] == '':
                                self.button = j
                                break

            elif len(self.bot_dict[1]) < 1 < len(self.player_dict[1]):
                multiple_moves = [i for i in self.player_dict[1]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    multiple_moves = [i for i in self.player_dict[1]]
                    for i in self.player_dict[0]:
                        multiple_moves.append(i)
                    moves_without_values = []
                    for i in multiple_moves:
                        for j in i:
                            if self.board[j] == '':
                                moves_without_values.append(j)
                    cross_cells = list(set(moves_without_values))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        for i in self.player_dict[1]:
                            for j in i:
                                if self.board[j] == '':
                                    self.button = j
                                    break

            elif len(self.bot_dict[1]) > 1 > len(self.player_dict[1]):
                multiple_moves = [i for i in self.bot_dict[1]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    multiple_moves = [i for i in self.bot_dict[1]]
                    for i in self.bot_dict[0]:
                        multiple_moves.append(i)
                    moves_without_values = []
                    for i in multiple_moves:
                        for j in i:
                            if self.board[j] == '':
                                moves_without_values.append(j)
                    cross_cells = list(set(moves_without_values))
                    self.button = random.choice(cross_cells)
                    if not cross_cells:
                        for i in self.bot_dict[1]:
                            for j in i:
                                if self.board[j] == '':
                                    self.button = j
                                    break

            elif len(self.bot_dict[1]) > 0 and len(self.player_dict[1]) > 0:
                cells_bot = [i for i in self.bot_dict[1]]
                cells_player = [i for i in self.player_dict[1]]
                all_cells = cells_bot + cells_player
                moves_without_values = []
                for i in all_cells:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                if len(cross_cells) > 0:
                    self.button = random.choice(cross_cells)
                else:
                    for i in self.bot_dict[1]:
                        for j in i:
                            if self.board[j] == '':
                                self.button = j
                                break

            elif len(self.bot_dict[0]) < 1 < len(self.player_dict[0]):
                multiple_moves = [i for i in self.player_dict[0]]
                moves_without_values = []
                for i in multiple_moves:
                    for j in i:
                        if self.board[j] == '':
                            moves_without_values.append(j)
                cross_cells = list(set(moves_without_values))
                self.button = random.choice(cross_cells)
                if not cross_cells:
                    for i in self.player_dict[0]:
                        for j in i:
                            if self.board[j] == '':
                                self.button = j
                                break

            else:
                spaces_left = [k for k, v in self.board.items() if v == '']
                self.button = random.choice(spaces_left)
        self.buttons[self.button].invoke()

        # else:
        #     best_score = -1000
        #     best_move = 0
        #     ai_sign = self.ai_sign
        #     player_sign = self.player_sign
        #     board = self.board
        #
        #     for key in board.keys():
        #         if board[key] == '':
        #             board[key] = ai_sign
        #             score = PlayerVsAi.minimax(board, ai_sign, player_sign, False, depth=7)
        #             board[key] = ''
        #             print(score)
        #             print(key)
        #             if score > best_score:
        #                 best_score = score
        #                 best_move = key
        #     if best_score == -1000:
        #         best_move = random.choice([k for k, v in self.board if v != ''])
        #     self.buttons[best_move].invoke()


class PlayerVsAiReverse(PlayerVsAiBaseSettings):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_label['text'] = 'Player Vs AI reverse'
        self.restart.configure(command=lambda: self.master.switch_canvas(PlayerVsAiReverse))
        self.best_ai_move = 0

    def check_winner_conditions(self):
        """Checking if player or bot won / Проверяем возможность выигрыша игрока или бота"""
        win = False
        for condition in self.all_winning_conditions:
            not_empty = all(self.board[ele] != '' for ele in condition)
            x_sign = all(self.board[ele] == 'X' for ele in condition)
            o_sign = all(self.board[ele] == 'O' for ele in condition)
            if not_empty and (x_sign or o_sign):
                win = True
                self.move_label['text'] = f'{self.who_plays}\nlost!'
                for i in condition:
                    self.buttons[i].configure(bg='#FF5C58')
                break
        return win

    def check_play_state(self):
        """Disable all buttons in case current player or bot lost or it's tie. Рассматриваем положение в игре,
        если игрок или бот проигрывает или наступает ничья, отключаем все кнопки на поле
        """
        check_win = self.check_winner_conditions()
        endgame = False
        if check_win:
            for i in self.buttons:
                i.configure(command=lambda: None)
                endgame = True
        return endgame

    def ai_move(self):
        """Implementing AI (commented code is for minimax algorithm) not to place 5 signs in a row
         Прописываем поведение бота, чтобы он не поставил 5 знаков в одну линию
         """
        if all(self.board[i] == '' for i in range(100)):
            random_numbers = [33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66]
            self.button = random.choice(random_numbers)
        else:
            self.ai_win_conditions()

            if len(self.bot_dict[1]) == 0 and len(self.bot_dict[2]) == 0 and len(self.bot_dict[3]) == 0 and len(self.bot_dict[4]) == 0:
                move = random.choice([i for i in self.bot_dict[0]])
                self.button = random.choice(move)

            elif len(self.bot_dict[0]) > 0:
                possible_moves = [i for i in self.bot_dict[0]]
                all_moves = []
                self.best_ai_move = None
                current_length_2 = len(self.bot_dict[2])
                current_length_3 = len(self.bot_dict[3])
                current_length_4 = len(self.bot_dict[4])
                current_length_5 = len(self.bot_dict[5])
                for move in possible_moves:
                    for pos in move:
                        if pos not in all_moves:
                            all_moves.append(pos)
                shuffled_moves = random.sample(all_moves, len(all_moves))
                for move in shuffled_moves:
                    self.board[move] = self.ai_sign
                    self.ai_win_conditions()
                    if len(self.bot_dict[2]) == current_length_2 and len(self.bot_dict[3]) == current_length_3\
                            and len(self.bot_dict[4]) == current_length_4 and len(self.bot_dict[5]) == current_length_5:
                        self.best_ai_move = move
                        self.board[move] = ''
                        break
                    else:
                        self.board[move] = ''
                if self.best_ai_move is None:
                    for move in shuffled_moves:
                        self.board[move] = self.ai_sign
                        self.ai_win_conditions()
                        if len(self.bot_dict[3]) == current_length_3 and len(self.bot_dict[4]) == current_length_4 \
                                and len(self.bot_dict[5]) == current_length_5:
                            self.best_ai_move = move
                            self.board[move] = ''
                            break
                        else:
                            self.board[move] = ''
                if self.best_ai_move is None:
                    for move in shuffled_moves:
                        self.board[move] = self.ai_sign
                        self.ai_win_conditions()
                        if len(self.bot_dict[4]) == current_length_4 and len(self.bot_dict[5]) == current_length_5:
                            self.best_ai_move = move
                            self.board[move] = ''
                            break
                        else:
                            self.board[move] = ''
                if self.best_ai_move is None:
                    for move in shuffled_moves:
                        self.board[move] = self.ai_sign
                        self.ai_win_conditions()
                        if len(self.bot_dict[5]) == current_length_5:
                            self.best_ai_move = move
                            self.board[move] = ''
                            break
                        else:
                            self.board[move] = ''
                if self.best_ai_move is None:
                    self.best_ai_move = random.choice(shuffled_moves)
                self.button = self.best_ai_move

            elif len(self.bot_dict[1]) > 0:
                possible_moves = [i for i in self.bot_dict[1]]
                all_moves = []
                self.best_ai_move = None
                current_length_3 = len(self.bot_dict[3])
                current_length_4 = len(self.bot_dict[4])
                current_length_5 = len(self.bot_dict[5])
                for move in possible_moves:
                    for pos in move:
                        if pos not in all_moves and self.board[pos] != self.ai_sign:
                            all_moves.append(pos)
                shuffled_moves = random.sample(all_moves, len(all_moves))
                for move in shuffled_moves:
                    self.board[move] = self.ai_sign
                    self.ai_win_conditions()
                    if len(self.bot_dict[3]) == current_length_3 and len(self.bot_dict[4]) == current_length_4\
                            and len(self.bot_dict[5]) == current_length_5:
                        self.best_ai_move = move
                        self.board[move] = ''
                        break
                    else:
                        self.board[move] = ''
                if self.best_ai_move is None:
                    for move in shuffled_moves:
                        self.board[move] = self.ai_sign
                        self.ai_win_conditions()
                        if len(self.bot_dict[4]) == current_length_4 and len(self.bot_dict[5]) == current_length_5:
                            self.best_ai_move = move
                            self.board[move] = ''
                            break
                        else:
                            self.board[move] = ''
                if self.best_ai_move is None:
                    for move in shuffled_moves:
                        self.board[move] = self.ai_sign
                        self.ai_win_conditions()
                        if len(self.bot_dict[5]) == current_length_5:
                            self.best_ai_move = move
                            self.board[move] = ''
                            break
                        else:
                            self.board[move] = ''
                if self.best_ai_move is None:
                    self.best_ai_move = random.choice(shuffled_moves)
                self.button = self.best_ai_move

            elif len(self.bot_dict[2]) > 0:
                possible_moves = [i for i in self.bot_dict[2] if i != self.ai_sign]
                all_moves = []
                self.best_ai_move = None
                current_length_4 = len(self.bot_dict[4])
                current_length_5 = len(self.bot_dict[5])
                for move in possible_moves:
                    for pos in move:
                        if pos not in all_moves and self.board[pos] != self.ai_sign:
                            all_moves.append(pos)
                shuffled_moves = random.sample(all_moves, len(all_moves))
                for move in shuffled_moves:
                    self.board[move] = self.ai_sign
                    self.ai_win_conditions()
                    if len(self.bot_dict[4]) == current_length_4 and len(self.bot_dict[5]) == current_length_5:
                        self.best_ai_move = move
                        self.board[move] = ''
                        break
                    else:
                        self.board[move] = ''
                if self.best_ai_move is None:
                    for move in shuffled_moves:
                        self.board[move] = self.ai_sign
                        self.ai_win_conditions()
                        if len(self.bot_dict[5]) == current_length_5:
                            self.best_ai_move = move
                            self.board[move] = ''
                            break
                        else:
                            self.board[move] = ''
                if self.best_ai_move is None:
                    self.best_ai_move = random.choice(shuffled_moves)
                self.button = self.best_ai_move

            elif len(self.bot_dict[3]) > 0:
                possible_moves = [i for i in self.bot_dict[3] if i != self.ai_sign]
                all_moves = []
                self.best_ai_move = None
                current_length_5 = len(self.bot_dict[5])
                for move in possible_moves:
                    for pos in move:
                        if pos not in all_moves and self.board[pos] != self.ai_sign:
                            all_moves.append(pos)
                shuffled_moves = random.sample(all_moves, len(all_moves))
                for move in shuffled_moves:
                    self.board[move] = self.ai_sign
                    self.ai_win_conditions()
                    if len(self.bot_dict[5]) == current_length_5:
                        self.best_ai_move = move
                        self.board[move] = ''
                        break
                    else:
                        self.board[move] = ''
                if self.best_ai_move is None:
                    spaces_left = [k for k, v in self.board.items() if v == '']
                    self.best_ai_move = random.choice(spaces_left)
                self.button = self.best_ai_move

        self.buttons[self.button].invoke()


if __name__ == '__main__':
    gui = TicTacToe()
    gui.mainloop()
