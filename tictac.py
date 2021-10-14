from abc import ABC, abstractmethod
import tkinter as tk
from winning_conditions import winning_conditions
from itertools import groupby


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
        tk.Button(self, text="Exit", font=('Segoe Print', 15, 'bold'), bg='white', command=master.destroy).grid(column=0, row=3, pady=2)


class CreateBoard(tk.Canvas, ABC):
    def __init__(self, master, *args, **kwargs):
        """Setting our base board to play with/ Создаём поле для игры"""
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack(pady=(20, 60), padx=40)
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

    def create_board(self):
        for i in range(100):
            self.board[i] = ''

    def create_buttons(self):
        x = 0
        for i in range(10):
            for n in range(10):
                self.buttons.append(x)
                self.buttons[x] = tk.Button(
                    self, text='', bd=4, height=1, width=4, font=("Segoe Print", 14, 'bold'), state=tk.DISABLED, command=lambda x=x: self.make_move(x))
                self.buttons[x].grid(row=i + 1, column=n)
                x += 1

    def check_winner_conditions(self):
        """Checking if player or bot won / Проверяем возможность выигрыша игрока или бота"""
        win = False
        for condition in winning_conditions:
            not_empty = all(self.board[ele] != '' for ele in condition)
            x_sign = all(self.board[ele] == 'X' for ele in condition)
            o_sign = all(self.board[ele] == 'O' for ele in condition)
            print(not_empty)
            if not_empty and (x_sign or o_sign):
                win = True
                for i in condition:
                    self.buttons[i].configure(bg='green')
                break
        return win

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
        self.who_plays = self.player_one
        self.start_game('x')

    def start_game(self, sign):
        for i in self.buttons:
            i['state'] = tk.NORMAL
        self.restart.configure(command=lambda: self.master.switch_canvas(PlayerVsPlayer))
        self.move_label['text'] = f'{self.who_plays}\nturn...'
        self.move_label.grid(column=10, row=4, rowspan=2, padx=(32, 0))
        self.restart['state'] = tk.NORMAL

    def make_move(self, button_number):
        """Checking if it's allowed to make a move to certain position. Disable all buttons in case current player won
        Проверяем не занята ли нужная ячейка. Изменяем ее и проверяем не выиграл ли текущий игрок."""
        print(self.board)
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
            self.check_player_win()

    def check_player_win(self):
        """Disable all buttons in case current player won. Проверяем выиграл ли игрок,
         в случае выигрыша отключаем все кнопки на поле"""
        check_win = self.check_winner_conditions()
        if check_win:
            self.move_label['text'] = f'{self.who_plays}\nwins!'
            for i in self.buttons:
                i.configure(command=lambda: None)
        else:
            if self.who_plays == self.player_one:
                self.who_plays = self.player_two
            else:
                self.who_plays = self.player_one
            self.move_label['text'] = f'{self.who_plays}\nturn...'


class PlayerVsAi(CreateBoard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_label['text'] = 'Player Vs AI'
        self.player = ''
        self.ai = ''
        self.x_button = tk.Button(self, text="X", font=('Segoe Print', 13, 'bold'),
                                 bg='white', height=0, width=4, bd=4, command=lambda: self.start_game('x'), fg="red")
        self.x_button.grid(column=10, row=5, padx=(30, 0))
        self.o_button = tk.Button(self, text="O", font=('Segoe Print', 13, 'bold'),
                                 bg='white', height=0, width=4, bd=4, command=lambda: self.start_game('o'), fg="blue")
        self.o_button.grid(column=11, row=5, padx=(30, 0))

    def start_game(self, sign):
        for i in self.buttons:
            i['state'] = tk.NORMAL
        self.x_button.grid_forget()
        self.o_button.grid_forget()
        self.restart['state'] = tk.NORMAL
        self.restart.configure(command=lambda: self.master.switch_canvas(PlayerVsAi))
        if sign == 'x':
            self.player = 'x'
            self.ai = 'o'
            self.move_label['text'] = 'Your Turn'
        if sign == 'o':
            self.player = 'o'
            self.ai = 'x'
            self.move_label['text'] = 'AI thinking'

    def make_move(self, button_number):
        pass


if __name__ == '__main__':
    gui = TicTacToe()
    gui.mainloop()
