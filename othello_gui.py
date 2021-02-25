import tkinter
import time

import othello as oth

LIGHT_FONT = ("Nexa light", 12)
BOLD_FONT = ("Nexa Bold", 11)
CELL_LENGTH = 60
COL_ROW_NAME_LENGTH = 40
DELAY = 1.5
CRED2 = '\33[91m'
CYELLOW2 = '\33[93m'
CURRENT_NUMB_CALL = 0


class OthelloBoard:
    def __init__(self):
        # creat an instance from tkinter library
        self._root_window = tkinter.Tk()
        self._root_window.title("8X8 Othello")

        self.set_window_size()
        self.rows_cols_name_show()

        # Draw main rectangle
        self._canvas = tkinter.Canvas(
            master=self._root_window, background='green', width=oth.SIZE * CELL_LENGTH,
            height=oth.SIZE * CELL_LENGTH)
        # Create cells
        self._canvas.grid(
            row=2, column=1, padx=8, pady=5,
            sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        # select method for events
        self._canvas.bind('<Configure>', self.window_resize)
        self._canvas.bind('<Button-1>', self._on_canvas_click)

        # Configure the selected row and column with weight option.
        # Weight causes a row or column to grow if there's extra space
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.columnconfigure(0, weight=1)

        # for show point of black and white
        self._counter_text = tkinter.StringVar()
        self.title_label = tkinter.Label(
            master=self._root_window, background="gold2",
            textvariable=self._counter_text,
            font=LIGHT_FONT)
        self.title_label.grid(row=5, column=1, padx=0, pady=(0, 7),
                              sticky=tkinter.N)

        self.turn_canvas = tkinter.Canvas(
            master=self._root_window, background="gold2", width=oth.SIZE * CELL_LENGTH,
            height=COL_ROW_NAME_LENGTH)

        self.turn_canvas.grid(row=0, column=1, padx=10, pady=10,
                              sticky=tkinter.N)

        # for show current turn and when game is over it show winner
        self._turn_text = tkinter.StringVar()
        self._turn_text.set('Winner')
        self.bottom_label = tkinter.Label(
            master=self.turn_canvas, background="gold2", textvariable=self._turn_text,
            font=LIGHT_FONT)
        self.bottom_label.grid(row=0, column=1, padx=(25, 5), pady=5,
                               sticky=tkinter.S)

        self.turn_rect = self.turn_canvas.create_rectangle(7, 10, 22, 25, fill='gray15', width=0)

    def set_window_size(self):
        # this def set max and min size of game window!
        # max and min size of game window are same!
        width_of_window = 530
        height_of_window = 650
        self._root_window.maxsize(width_of_window, height_of_window)
        self._root_window.minsize(width_of_window, height_of_window)

    def rows_cols_name_show(self):
        # this def create a row above game board for name of every column
        # also this function create a column left side of game board for number of every row

        # creat columns name's root component
        cols_up = tkinter.Canvas(
            master=self._root_window, width=oth.SIZE * CELL_LENGTH,
            height=COL_ROW_NAME_LENGTH)

        cols_up.grid(
            row=1, column=1, padx=10, pady=0,
            sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        # Create cells for name of columns
        for i in range(oth.SIZE):
            _title_cols_text = tkinter.StringVar()
            _title_cols_text.set(chr(i + 65))
            title_cols = tkinter.Label(
                master=cols_up, textvariable=_title_cols_text,
                font=BOLD_FONT)

            title_cols.grid(row=1, column=i, padx=22, pady=0,
                            sticky=tkinter.N)

        # creat rows name's root component
        rows_left = tkinter.Canvas(
            master=self._root_window, width=COL_ROW_NAME_LENGTH,
            height=oth.SIZE * CELL_LENGTH)

        rows_left.grid(
            row=2, column=0, padx=(7, 5), pady=0,
            sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        # Create cells for name of rows
        for i in range(oth.SIZE):
            _title_rows_text = tkinter.StringVar()
            _title_rows_text.set((i + 1))
            title_rows = tkinter.Label(
                master=rows_left, textvariable=_title_rows_text,
                font=BOLD_FONT)

            title_rows.grid(row=i, column=0, padx=0, pady=21,
                            sticky=tkinter.N)

    def _on_canvas_click(self, event: tkinter.Event):
        # Determines the point of the click event.
        moves = self.which_cell(event.y, event.x)

        if game_logic_instance._turn:
            try:
                game_logic_instance.render_after_click(moves[0], moves[1])
                self.draw_board()
                self._canvas.update()
                if not game_logic_instance._turn:
                    try:
                        game_logic_instance.play_AI()
                        time.sleep(DELAY)
                        self.draw_board()
                    except Exception as e:
                        print("first   ", e)

                    list_of_possible_cells = game_logic_instance.valid_cells_for_draw_gold_circle(True)
                    self.draw_gold_cir_for_possible_cells(list_of_possible_cells)

            except Exception as e:
                print("second    ", e)
        else:
            try:
                game_logic_instance.play_AI()
                time.sleep(DELAY)
                self.draw_board()

            except Exception as e:
                print(e)

        # self.draw_board()

    def draw_gold_cir_for_possible_cells(self, possible_cells):
        size_of_cells = self.cells_size()
        for cell in possible_cells:
            self._canvas.create_oval(20 + cell[0] * (CELL_LENGTH * size_of_cells[0]) + 3,
                                     20 + cell[1] * (CELL_LENGTH * size_of_cells[1]) + 3,
                                     (CELL_LENGTH * size_of_cells[0]) + cell[0] * (
                                             CELL_LENGTH * size_of_cells[0]) - 19,
                                     (CELL_LENGTH * size_of_cells[1]) + cell[1] * (
                                             CELL_LENGTH * size_of_cells[1]) - 22,
                                     fill='#ffa801',
                                     outline='#ffa801', width=1)

    def canvas_size(self):
        # this function return size of game board(in pixels)
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        return canvas_width, canvas_height

    def cells_size(self):
        # this function return size of cells (in pixels)
        current_size_of_canvas = self.canvas_size()
        # width of every cell in game board
        cell_width = current_size_of_canvas[0] / (oth.SIZE * CELL_LENGTH)
        # height of every cell in game board
        cell_height = current_size_of_canvas[1] / (oth.SIZE * CELL_LENGTH)

        return cell_width, cell_height

    def which_cell(self, a, b):
        # Find x and y coordinates of clicked point based on click position on canvas
        every_cell_size = self.cells_size()
        x = int(a / (every_cell_size[1] * CELL_LENGTH))
        y = int(b / (every_cell_size[0] * CELL_LENGTH))

        return x, y

    def window_resize(self, event: tkinter.Event):
        # If the window size changes, this method rebuilds the window
        self._canvas.delete(tkinter.ALL)
        self.draw_board()

    def draw_board(self):
        # draw game board and create white and black circles
        # Delete everything that already exists
        self._canvas.delete(tkinter.ALL)

        size_of_cells = self.cells_size()
        self.create_squares(size_of_cells)

        list_of_possible_cells = game_logic_instance.valid_cells_for_draw_gold_circle(game_logic_instance._turn)
        if len(list_of_possible_cells) == 0:
            list_of_possible_cells = game_logic_instance.valid_cells_for_draw_gold_circle(not game_logic_instance._turn)
        self.draw_gold_cir_for_possible_cells(list_of_possible_cells)

        self.create_circles(size_of_cells)
        self.points_shower()

    def create_squares(self, size_of_cells):
        # this method draw square cells
        for i in range(oth.SIZE + 1):
            for j in range(oth.SIZE + 1):
                if (j % 2 == 0 and i % 2 == 0) or (j % 2 == 1 and i % 2 == 1):
                    self._canvas.create_rectangle(1 + j * (CELL_LENGTH * size_of_cells[0]),
                                                  1 + i * (CELL_LENGTH * size_of_cells[1]),
                                                  (CELL_LENGTH * size_of_cells[0]) + j * (
                                                          CELL_LENGTH * size_of_cells[0]),
                                                  (CELL_LENGTH * size_of_cells[1]) + i * (
                                                          CELL_LENGTH * size_of_cells[1]),
                                                  fill='dark green',
                                                  outline='dark green', width=1)
                else:
                    self._canvas.create_rectangle(1 + j * (CELL_LENGTH * size_of_cells[0]),
                                                  1 + i * (CELL_LENGTH * size_of_cells[1]),
                                                  (CELL_LENGTH * size_of_cells[0]) + j * (
                                                          CELL_LENGTH * size_of_cells[0]),
                                                  (CELL_LENGTH * size_of_cells[1]) + i * (
                                                          CELL_LENGTH * size_of_cells[1]),
                                                  fill='green4',
                                                  outline='dark green', width=1)

    def create_circles(self, size_of_cells):
        # this method draw black and white circle
        for i in range(oth.SIZE):
            for j in range(oth.SIZE):
                # create white circles
                if game_logic_instance._board[j][i] == oth.WHITE:
                    self._canvas.create_oval(1 + j * (CELL_LENGTH * size_of_cells[0]) + 3,
                                             1 + i * (CELL_LENGTH * size_of_cells[1]) + 3,
                                             (CELL_LENGTH * size_of_cells[0]) + j * (
                                                     CELL_LENGTH * size_of_cells[0]) - 3,
                                             (CELL_LENGTH * size_of_cells[1]) + i * (
                                                     CELL_LENGTH * size_of_cells[1]) - 3,
                                             fill='#f5f6fa',
                                             outline='#f5f6fa', width=1)
                # create black circles
                elif game_logic_instance._board[j][i] == oth.BLACK:
                    self._canvas.create_oval(1 + j * (CELL_LENGTH * size_of_cells[0]) + 3,
                                             1 + i * (CELL_LENGTH * size_of_cells[1]) + 3,
                                             (CELL_LENGTH * size_of_cells[0]) + j * (
                                                     CELL_LENGTH * size_of_cells[0]) - 3,
                                             (CELL_LENGTH * size_of_cells[1]) + i * (
                                                     CELL_LENGTH * size_of_cells[1]) - 3,
                                             fill='gray17',
                                             outline='gray17', width=1)

    def points_shower(self):
        # Show earned points
        self._counter_text.set(
            'Black Points: ' + str(game_logic_instance._black_points) + '     |     White Points: ' + str(
                game_logic_instance._white_points))

        self.check_winner()
        self.show_turn()

    def show_turn(self):
        # If the game is not over, it shows the current turn
        if game_logic_instance._winner == None:
            turn_player = ''
            if game_logic_instance._turn == oth.BLACK:
                turn_player = "Turn -> Black"
                self.turn_canvas.itemconfig(self.turn_rect, fill='gray15')
            elif game_logic_instance._turn == oth.WHITE:
                turn_player = "Turn -> White"
                self.turn_canvas.itemconfig(self.turn_rect, fill='snow2')

            self._turn_text.set(turn_player)

    def end_of_game(self, state_of_win):
        # at the end of game this function shows winner of game in a golden box
        # create text of box based on input (for example -> The winner is White)
        winner_text = tkinter.StringVar()
        winner_text.set(state_of_win)

        # create box for show winner
        winner_show = tkinter.Label(
            master=self._canvas, background='gold3', textvariable=winner_text,
            font=LIGHT_FONT)
        winner_show.grid(
            row=4, column=4, padx=160, pady=230, ipadx=5, ipady=10,
            sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def check_winner(self):
        # this function check if game ended set winner in bottom of game board and call end_of_game
        self.show_turn()
        if not game_logic_instance.is_game_over():
            game_logic_instance.change_turn()
            self.show_turn()

            game_logic_instance.player_has_any_move()
            if game_logic_instance._winner != None:
                average_search_time = game_logic_instance.total_search_time / game_logic_instance.total_number_of_searches
                print(CYELLOW2 + "Total search time is ---> " + CYELLOW2,
                      CRED2 + str(game_logic_instance.total_search_time) + CRED2)
                print(CYELLOW2 + "Average search time is ---> " + CYELLOW2,
                      CRED2 + str(average_search_time) + CRED2)
                write_log(str(average_search_time) + ",")
                if game_logic_instance._winner == oth.WHITE:
                    self._turn_text.set('Finished')
                    self.turn_canvas.itemconfig(self.turn_rect, fill='snow2')
                    self.end_of_game("The winner is White")
                    write_log("WHITE\n")
                elif game_logic_instance._winner == oth.BLACK:
                    self._turn_text.set('Finished')
                    self.turn_canvas.itemconfig(self.turn_rect, fill='gray15')
                    self.end_of_game("The winner is Black")
                    write_log("BLACK\n")
                elif game_logic_instance._winner == 'NONE':
                    self._turn_text.set('Finished')
                    self.turn_canvas.itemconfig(self.turn_rect, fill='gold2')
                    self.end_of_game("The game equalised")
                    write_log("EQU\n")

    def run(self):
        # Runs the game board
        self._root_window.mainloop()


def write_log(str_log):
    f = open("log.txt", "a")
    f.write(str_log)
    # f.close()


if __name__ == '__main__':
    game_logic_instance = oth.GameLogic()
    game_logic_instance.create_board()
    OthelloBoard().run()
