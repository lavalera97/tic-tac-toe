from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox


class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TicTacToe 10x10')
        self._main_canvas = None
        self.switch_canvas(StartPage)

    """Initializing func to switch between canvases / Создаём функцию для смены работающего окна"""
    def switch_canvas(self, canvas_class):
        if self._main_canvas:
            self._main_canvas.pack_forget()
        canvas = canvas_class(self)
        self._main_canvas = canvas


class CreateBoard(tk.Canvas, ABC):
    """Setting our base board to play with/ Создаём поле для игры"""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(pady=(20, 60), padx=40)
        self.board = {}
        self.buttons = []
        self.create_buttons()
        self.create_board()
        self.move_label = tk.Label(self, text="Choose side", font=('Segoe Print', 20, 'bold'), bd=4)
        self.move_label.grid(column=10, row=4, padx=(30, 0))
        # self.x_button = tk.Button(self, text="X", font=('Segoe Print', 15, 'bold'),
        #                          bg='white', width=10, bd=4).grid(column=10, row=5, rowspan=2, padx=(30, 0))
        # self.o_button =
        self.name_label = tk.Label(self, text="", font=('Segoe Print', 20, 'bold'), bd=4)
        self.name_label.grid(column=0, row=0, columnspan=10, pady=(0, 20))
        self.restart = tk.Button(self, text="Restart", font=('Segoe Print', 14, 'bold'),
                                 bg='white', width=10, bd=4, state=tk.DISABLED)
        self.restart.grid(column=10, row=8, padx=(30, 0))
        self.main_button = tk.Button(self, text="Main menu", font=('Segoe Print', 14, 'bold'), bd=4, bg='white',
                                     width=10, command=lambda: master.switch_canvas(StartPage))
        self.main_button.grid(column=10, row=9, rowspan=2, padx=(30, 0))
        print(len(self.buttons))
        print(self.board)

    def create_board(self):
        for i in range(100):
            self.board[i] = ''

    def create_buttons(self):
        x = 0
        for i in range(10):
            for n in range(10):
                self.buttons.append(x)
                self.buttons[x] = tk.Button(
                    self, text='', bd=4, height=3, width=6)
                self.buttons[x].grid(row=i + 1, column=n)
                x += 1

    # @abstractmethod
    # def choose_side(self):
    #     pass


class StartPage(tk.Canvas):
    """Creating starting page / Начальная страница"""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(pady=25, padx=30)
        tk.Label(self, text="TIC-TAC-TOE", font=('Segoe Print', 20, 'bold')).grid(column=0, row=0, pady=5, padx=30)
        tk.Button(self, text="Player vs Player", font=('Segoe Print', 15, 'bold'), bg='white',
                  command=lambda: master.switch_canvas(PlayerVsPlayer)).grid(column=0, row=1, pady=2)
        tk.Button(self, text="Player vs AI", font=('Segoe Print', 15, 'bold'), bg='white',
                  command=lambda: master.switch_canvas(PlayerVsAi)).grid(column=0, row=2, pady=2)
        tk.Button(self, text="Exit", font=('Segoe Print', 15, 'bold'), bg='white', command=master.destroy).grid(column=0, row=3, pady=2)


class PlayerVsPlayer(CreateBoard):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name_label['text'] = 'Player Vs Player'

    # def choose_side(self):



class PlayerVsAi(CreateBoard):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name_label['text'] = 'Player Vs AI'




if __name__ == '__main__':
    gui = TicTacToe()
    gui.mainloop()
