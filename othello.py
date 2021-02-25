import time
import random

# NO_CIRCLE = no circle
NO_CIRCLE = None
# white player in board
WHITE = False
# black player board
BLACK = True
# number of rows and columns
SIZE = 8
# This variable indicates depth of alpha beta tree
DEPTH = 1
# This var indicates number of nodes in current alpha beta search tree
NUMBER_OF_NODES = 0

MAX_NUMB_OF_RAND_NODES = 4


def comparison(current_node):
    return heuristic(current_node[0], False)


def calculate_len_of_selection(overall_len, percentage_of_selection):
    return int((percentage_of_selection * ((overall_len - 1) // 100)))


def list_copy(main_list):
    copy_list = [x[:] for x in main_list]
    return copy_list


WEIGHTS = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120],
]

COPY_WEIGHT = list_copy(WEIGHTS)


def is_corner(cell_col, cell_row):
    return ((cell_row % (SIZE - 1)) == 0) and ((cell_col % (SIZE - 1)) == 0)


def check_is_good_border(col, row):
    if (row == 0 or row == 7) and (col == 5 or col == 2):
        return True
    if (col == 0 or col == 7) and (row == 2 or row == 5):
        return True
    return False


def check_is_fair_border(col, row):
    if (row == 0 or row == 7) and (col == 3 or col == 4):
        return True
    if (col == 0 or col == 7) and (row == 3 or row == 4):
        return True
    return False


def check_is_in_bad_lines(col, row):
    if (row == 1 or row == 6) and (2 <= col <= 5):
        return True
    if (col == 1 or col == 6) and (2 <= row <= 5):
        return True
    return False


def check_is_fair_diagonal(col, row):
    if (row == 2 or row == 5) and (col == 2 or col == 5):
        return True
    return False


def check_is_good_neighbor(board, col, row):
    if (col == 1 and row == 0) or (col == 0 and row == 1):
        if board[0][0] != NO_CIRCLE:
            return True
    elif (col == 6 and row == 0) or (col == 7 and row == 1):
        if board[7][0] != NO_CIRCLE:
            return True
    elif (col == 0 and row == 6) or (col == 1 and row == 7):
        if board[0][7] != NO_CIRCLE:
            return True
    elif (col == 7 and row == 3) or (col == 3 and row == 7):
        if board[7][7] != NO_CIRCLE:
            return True
    return False


def check_is_good_corner_diagonal(board, col, row):
    if col == 1 and row == 1:
        if board[0][0] != NO_CIRCLE:
            return True
    elif col == 6 and row == 1:
        if board[7][0] != NO_CIRCLE:
            return True
    elif col == 2 and row == 6:
        if board[0][7] != NO_CIRCLE:
            return True
    elif col == 6 and row == 6:
        if board[7][7] != NO_CIRCLE:
            return True
    return False


def change_color_for_AI(current_board, points, current_turn):
    copy_board = list_copy(current_board)
    for point in points:
        copy_board[point[0]][point[1]] = current_turn
    return copy_board


def is_corner(cell_row, cell_col):
    return ((cell_row % (SIZE - 1)) == 0) and ((cell_col % (SIZE - 1)) == 0)


def is_neighbor_of_the_corners(cell_row, cell_col):
    if (cell_row == 0 and cell_col == SIZE - 1) or (cell_row == 0 and cell_col == 1):
        return True
    if (cell_row == 1 and cell_col == 0) or (cell_row == SIZE - 2 and cell_col == 0):
        return True
    if (cell_row == SIZE - 1 and cell_col == 1) or (cell_row == SIZE - 1 and cell_col == SIZE - 2):
        return True
    if (cell_row == 1 and cell_col == SIZE - 1) or (cell_row == SIZE - 2 and cell_col == SIZE - 1):
        return True
    return False


def is_corner_diagonal(cell_row, cell_col):
    if cell_row == 1 and cell_col == 1:
        return True
    if cell_row == 1 and cell_col == SIZE - 2:
        return True
    if cell_row == SIZE - 2 and cell_col == 1:
        return True
    if cell_row == SIZE - 2 and cell_col == SIZE - 2:
        return True
    return False


def cal_weight(board, turn):
    result = 0
    for col in range(len(board)):
        for row in range(len(board[col])):
            if board[col][row] == NO_CIRCLE:
                continue
            elif board[col][row] == turn:
                result += COPY_WEIGHT[col][row]
    return result


def update_cell_weight(board, turn):
    global COPY_WEIGHT
    COPY_WEIGHT = list_copy(WEIGHTS)
    updated_weight = 5
    if board[0][0] == turn:
        COPY_WEIGHT[0][1] = updated_weight
        COPY_WEIGHT[1][1] = updated_weight
        COPY_WEIGHT[1][0] = updated_weight
    if board[7][7] == turn:
        COPY_WEIGHT[7][6] = updated_weight
        COPY_WEIGHT[6][6] = updated_weight
        COPY_WEIGHT[6][7] = updated_weight
    if board[7][0] == turn:
        COPY_WEIGHT[6][0] = updated_weight
        COPY_WEIGHT[6][1] = updated_weight
        COPY_WEIGHT[7][1] = updated_weight
    if board[0][7] == turn:
        COPY_WEIGHT[0][6] = updated_weight
        COPY_WEIGHT[1][6] = updated_weight
        COPY_WEIGHT[1][7] = updated_weight


def heuristic(current_board, turn):
    current_points_of_this_player = 0
    current_points_of_opposite = 0
    all_opposite_circle_destroyed = 0
    update_cell_weight(current_board, turn)
    calc_weight = 0
    calc_opposite_weight = 0
    for cell_col in range(len(current_board)):
        for cell_row in range(len(current_board[cell_col])):
            if current_board[cell_col][cell_row] != turn and current_board[cell_col][cell_row] != NO_CIRCLE:
                all_opposite_circle_destroyed = 1
                current_points_of_opposite += 1
                calc_opposite_weight += WEIGHTS[cell_col][cell_row]
            if current_board[cell_col][cell_row] == turn:
                calc_weight += COPY_WEIGHT[cell_col][cell_row]
                current_points_of_this_player += 1

    all_opposite_circle_destroyed = (all_opposite_circle_destroyed + 1) % 2
    result = calc_weight
    result += (-1) * calc_opposite_weight
    result += 30 * current_points_of_this_player
    result += 5 * all_opposite_circle_destroyed
    result += (-20) * current_points_of_opposite
    return result


def heuristic_for_ai_vs_ai(current_board, turn, feature_list):
    current_points_of_this_player = 0
    current_points_of_opposite = 0
    all_opposite_circle_destroyed = 0
    update_cell_weight(current_board, turn)
    calc_weight = 0
    calc_opposite_weight = 0
    for cell_col in range(len(current_board)):
        for cell_row in range(len(current_board[cell_col])):
            if current_board[cell_col][cell_row] != turn and current_board[cell_col][cell_row] != NO_CIRCLE:
                all_opposite_circle_destroyed = 1
                current_points_of_opposite += 1
                # calc_opposite_weight += weight_mat[cell_col][cell_row]
                if is_corner(cell_col, cell_row):
                    calc_opposite_weight += feature_list[0]
                elif is_neighbor_of_the_corners(cell_row, cell_col):
                    calc_opposite_weight += feature_list[1]
                elif is_corner_diagonal(cell_row, cell_col):
                    calc_opposite_weight += feature_list[2]
                elif check_is_good_border(cell_col, cell_row):
                    calc_opposite_weight += feature_list[3]
                elif check_is_fair_border(cell_col, cell_row):
                    calc_opposite_weight += feature_list[4]
                elif check_is_fair_diagonal(cell_col, cell_row):
                    calc_opposite_weight += feature_list[5]
                elif check_is_in_bad_lines(cell_col, cell_row):
                    calc_opposite_weight += feature_list[6]
                else:
                    calc_opposite_weight += feature_list[7]

            if current_board[cell_col][cell_row] == turn:
                current_points_of_this_player += 1
                if is_corner(cell_col, cell_row):
                    calc_weight += feature_list[0]
                elif is_neighbor_of_the_corners(cell_row, cell_col):
                    calc_weight += feature_list[1]
                elif is_corner_diagonal(cell_row, cell_col):
                    calc_weight += feature_list[2]
                elif check_is_good_border(cell_col, cell_row):
                    calc_weight += feature_list[3]
                elif check_is_fair_border(cell_col, cell_row):
                    calc_weight += feature_list[4]
                elif check_is_fair_diagonal(cell_col, cell_row):
                    calc_weight += feature_list[5]
                elif check_is_in_bad_lines(cell_col, cell_row):
                    calc_weight += feature_list[6]
                else:
                    calc_weight += feature_list[7]

    all_opposite_circle_destroyed = (all_opposite_circle_destroyed + 1) % 2
    result = calc_weight
    result += (-1) * calc_opposite_weight
    result += feature_list[8] * current_points_of_this_player
    result += feature_list[9] * all_opposite_circle_destroyed
    result += (feature_list[10]) * current_points_of_opposite
    return result


class MoveIsNotValidException(Exception):
    pass


class TheGameIsOverException(Exception):
    pass


def valid_column_index(column_number):
    if type(column_number) != int or not 0 <= column_number < SIZE:
        raise ValueError()


# To determine if there is any move that player can make
# If there is not, nothing will be happened
def can_player_make_a_move(a):
    if True not in a:
        raise MoveIsNotValidException()


def valid_row_index(row_number):
    if type(row_number) != int or not 0 <= row_number < SIZE:
        raise ValueError()


class GameLogic:

    def __init__(self):
        self.total_search_time = 0
        self.total_number_of_searches = 0
        self._board = []
        self.create_board()
        self._turn = True
        self._black_points = 2
        self._white_points = 2
        self._winner = None
        self._fliplist = []

    # First, we initialize the board with NONE cells.
    # Then, we place 2 black and 2 white.
    def create_board(self):
        board = []
        for col in range(SIZE):
            board.append([])
            for row in range(SIZE):
                board[col].append(NO_CIRCLE)

        board[4][4] = WHITE
        board[3][3] = WHITE
        board[4][3] = BLACK
        board[3][4] = BLACK

        self._board = board

    # A cell has been clicked so :
    # First of all, we make flip list empty for new ones.
    # Then, we should check for valid row and column indexes.
    # Also, the game should not be over.
    # Then we can search all eight directions of cell (j)(i) for valid move and cells that we can flip
    # If there was not any valid move, we actually do nothing.
    def render_after_click(self, row_number, column_number):

        self._fliplist = []
        valid_column_index(column_number)
        valid_row_index(row_number)
        self._require_game_not_over()
        can_player_make_a_move(self.search_all_directions(row_number, column_number))

        if self._board[column_number][row_number] != NO_CIRCLE:
            raise MoveIsNotValidException()

        else:
            self._board[column_number][row_number] = self._turn
            self.change_color(self._fliplist)
            self.change_turn()
            self.update_score()

    # Search one direction, until we reach same color as cell(j)(i).
    # Then we can add all cells between them to flip list, to change their color.
    # Also we determine the validation of the move in that direction
    def search_one_direction(self, row, col, direction):

        change_color_list = []
        valid = False
        while self.valid_coordinates(col, row, direction):

            # Reached to an empty cell so we should stop searching.
            if self.check_cell_value(self._board, col, row, direction, NO_CIRCLE):
                break

            # Reached to a cell with opposite color of turn's color so we
            # keep on searching on that direction.
            elif not self.check_cell_value(self._board, col, row, direction, self._turn):
                change_color_list.append([col + direction[0], row + direction[1]])
                valid = True
                row += direction[1]
                col += direction[0]

            # Reached to a cell with the same color as turn's color so we stop
            # the searching and if there was one or more opposite color cell
            # between them, we add them to the flip list to change their color.
            elif self.check_cell_value(self._board, col, row, direction, self._turn):
                if valid:
                    self._fliplist.extend(change_color_list)
                    return True
                else:
                    break

        return False

    def check_cell_value(self, current_board, col, row, direction, value):
        return current_board[col + direction[0]][row + direction[1]] == value

    # To check if the point (col + deltaJ)(rew + deltaI) is still on the board or not
    @staticmethod
    def valid_coordinates(col, row, direction):
        return SIZE > col + direction[0] >= 0 and SIZE > row + direction[1] >= 0

    # Search all eight around direction of one cell
    # To see if there is any valid move or not
    def search_all_directions(self, row, col):
        directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        result = []
        for direction in directions:
            result.append(self.search_one_direction(row, col, direction))

        return result

    def change_color(self, points):
        for point in points:
            self._board[point[0]][point[1]] = self._turn

    # Recalculate and update scores of both players.
    def update_score(self):
        self._black_points = 0
        self._white_points = 0
        for item in self._board:
            for thing in item:
                if thing == BLACK:
                    self._black_points += 1
                elif thing == WHITE:
                    self._white_points += 1

    # Check if there is any empty cell too choose and if player can choose them
    # based on validation of move
    # If there is not any, then the game is over and we should determine the winner
    # and show the game is over message.
    def player_has_any_move(self) -> None:
        empty_spaces_left = self.empty_spaces_left()
        game_continues = self.is_game_over()

        if not empty_spaces_left:
            self.determine_winner()
        else:
            if not game_continues:
                self.determine_winner()

    def opposite_can_not_make_move_AI(self):
        game_continues = self.is_game_over()

        if not game_continues:
            return True
        return False

    # To check if there is any empty space on the board.
    def empty_spaces_left(self) -> bool:
        # if an empty cell exists return True else return False
        empty_spaces_left = False

        for i in range(SIZE):
            for j in range(SIZE):
                if self._board[j][i] == NO_CIRCLE:
                    empty_spaces_left = True

        return empty_spaces_left

    # If there is not any empty cells or valid move to make in all directions of every cell,
    # then the game is over
    def is_game_over(self) -> bool:
        validmovesleft = False
        for i in range(SIZE):
            for j in range(SIZE):
                if self._board[j][i] == NO_CIRCLE:
                    if True in self.search_all_directions(i, j):
                        validmovesleft = True

        return validmovesleft

    def valid_cells_for_draw_gold_circle(self, turn):
        valid_cells = []
        temp_list = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self._board[j][i] == NO_CIRCLE:
                    if True in self.search_all_directions_for_AI(self._board, i, j, temp_list, turn):
                        valid_cells.append([j, i])

        return valid_cells

    def determine_winner(self) -> None:
        # Determines the winner based on the points earned
        self.update_score()
        if self._black_points > self._white_points:
            self._winner = BLACK
        elif self._black_points < self._white_points:
            self._winner = WHITE
        else:
            self._winner = 'NONE'

    def change_turn(self):
        self._turn = BLACK if self._turn == WHITE else WHITE

    # If the game is over, clicking on the cells will do nothing
    def _require_game_not_over(self) -> None:
        if self._winner != None:
            raise TheGameIsOverException()

    # AI Part!

    def search_one_direction_for_AI(self, current_board, row, col, direction, current_board_flip_list, current_turn):
        change_color_list = []
        valid = False
        while self.valid_coordinates(col, row, direction):

            # Reached to an empty cell so we should stop searching.
            if self.check_cell_value(current_board, col, row, direction, NO_CIRCLE):
                break

            # Reached to a cell with opposite color of turn's color so we
            # keep on searching on that direction.
            elif not self.check_cell_value(current_board, col, row, direction, current_turn):
                change_color_list.append([col + direction[0], row + direction[1]])
                valid = True
                row += direction[1]
                col += direction[0]

            # Reached to a cell with the same color as turn's color so we stop
            # the searching and if there was one or more opposite color cell
            # between them, we add them to the flip list to change their color.
            elif self.check_cell_value(current_board, col, row, direction, current_turn):
                if valid:
                    current_board_flip_list.extend(change_color_list)
                    return True
                else:
                    break

        return False

    def search_all_directions_for_AI(self, current_board, row, col, current_board_flip_list, current_turn):
        directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        result = []
        for direction in directions:
            result.append(self.search_one_direction_for_AI(current_board, row, col, direction, current_board_flip_list,
                                                           current_turn))

        return result

    def is_valid(self, current_board, cell_row, cell_col, current_board_flip_list, current_turn):
        if current_board[cell_col][cell_row] != NO_CIRCLE:
            return False
        else:
            list_of_dir = self.search_all_directions_for_AI(current_board, cell_row, cell_col, current_board_flip_list,
                                                            current_turn)
            for i in list_of_dir:
                if i:
                    return True
            return False

    def add_to_total_search_time(self, diff_time):
        self.total_search_time += diff_time

    def alpha_beta(self, current_board, depth, alpha, beta, maximizing, current_turn):
        global NUMBER_OF_NODES
        NUMBER_OF_NODES += 1
        # print(current_board)

        main_boards_choices = []

        corner_boards_choices = []

        corner_neighbor_boards_choices = []

        corner_diagonal_boards_choices = []

        fair_corner_diagonal_boards_choices = []

        good_border_boards_choices = []

        fair_border_boards_choices = []

        bad_lines_boards_choices = []

        normal_boards_choices = []

        bad_boards_choices = []

        for cell_col in range(SIZE):
            for cell_row in range(SIZE):
                current_board_flip_list = []
                if self.is_valid(current_board, cell_row, cell_col, current_board_flip_list, current_turn):
                    if ((cell_row % (SIZE - 1)) == 0) and ((cell_col % (SIZE - 1)) == 0):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        corner_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif is_neighbor_of_the_corners(cell_row, cell_col):
                        if check_is_good_neighbor(current_board, cell_col, cell_row):
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                            normal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                        else:
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                            corner_neighbor_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif is_corner_diagonal(cell_row, cell_col):
                        if check_is_good_corner_diagonal(current_board, cell_col, cell_row):
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                            normal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                        else:
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                            corner_diagonal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_good_border(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        good_border_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_fair_diagonal(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        fair_corner_diagonal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_fair_border(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        fair_border_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_in_bad_lines(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        bad_lines_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    else:
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        normal_boards_choices.append([new_board_temp, [cell_col, cell_row]])

        if len(corner_boards_choices) > 0:
            # print("we have a good cell")
            main_boards_choices = corner_boards_choices

            # normal_boards_choices.extend(fair_border_boards_choices)
            # normal_boards_choices.extend(good_border_boards_choices)
            # normal_boards_choices.extend(fair_corner_diagonal_boards_choices)
            # len_of_random_selection = 2 - len(corner_boards_choices)
            # i = 0
            # while i < len_of_random_selection and len(normal_boards_choices) > 0:
            #     random_index = random.randint(0, len(normal_boards_choices) - 1)
            #     main_boards_choices.append(normal_boards_choices[random_index])
            #     del normal_boards_choices[random_index]
            #     i += 1

        elif len(good_border_boards_choices) > 0:
            main_boards_choices = good_border_boards_choices
            normal_boards_choices.extend(fair_border_boards_choices)
            normal_boards_choices.extend(fair_corner_diagonal_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(good_border_boards_choices)
            i = 0
            while i < len_of_random_selection and len(normal_boards_choices) > 0:
                random_index = random.randint(0, len(normal_boards_choices) - 1)
                main_boards_choices.append(normal_boards_choices[random_index])
                del normal_boards_choices[random_index]
                i += 1
        elif len(fair_corner_diagonal_boards_choices) > 0:

            main_boards_choices = fair_corner_diagonal_boards_choices
            normal_boards_choices.extend(fair_border_boards_choices)
            normal_boards_choices.extend(bad_lines_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(fair_corner_diagonal_boards_choices)
            i = 0
            while i < len_of_random_selection and len(normal_boards_choices) > 0:
                random_index = random.randint(0, len(normal_boards_choices) - 1)
                main_boards_choices.append(normal_boards_choices[random_index])
                del normal_boards_choices[random_index]
                i += 1
        elif len(fair_border_boards_choices) > 0:

            main_boards_choices = fair_border_boards_choices
            normal_boards_choices.extend(bad_lines_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(fair_border_boards_choices)
            i = 0
            while i < len_of_random_selection and len(normal_boards_choices) > 0:
                random_index = random.randint(0, len(normal_boards_choices) - 1)
                main_boards_choices.append(normal_boards_choices[random_index])
                del normal_boards_choices[random_index]
                i += 1
        elif len(normal_boards_choices) > 0:
            # print("normal cell")
            main_boards_choices = normal_boards_choices

            bad_boards_choices.extend(bad_lines_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(normal_boards_choices)
            i = 0
            while i < len_of_random_selection and len(bad_boards_choices) > 0:
                random_index = random.randint(0, len(bad_boards_choices) - 1)
                main_boards_choices.append(bad_boards_choices[random_index])
                del bad_boards_choices[random_index]
                i += 1

        elif len(bad_lines_boards_choices) > 0:
            # print("bad cell")
            main_boards_choices = bad_lines_boards_choices
            # bad_boards_choices.extend(corner_neighbor_boards_choices)
            # len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(bad_lines_boards_choices)
            # i = 0
            # while i < len_of_random_selection and len(bad_boards_choices) > 0:
            #     random_index = random.randint(0, len(bad_boards_choices) - 1)
            #     main_boards_choices.append(bad_boards_choices[random_index])
            #     del bad_boards_choices[random_index]
            #     i += 1
        elif len(corner_neighbor_boards_choices) > 0:
            # print("bad cell")
            main_boards_choices = corner_neighbor_boards_choices
        elif len(corner_diagonal_boards_choices) > 0:
            # print("very bad cell")
            main_boards_choices = corner_diagonal_boards_choices

        # dynamic depth based on number of nodes
        if depth == 0:
            if NUMBER_OF_NODES > 6000:
                # print("depth is zero !")
                return [heuristic(current_board, self._turn), current_board]
        if 0 > depth >= -1:
            if NUMBER_OF_NODES > 11500:
                # print("depth is between 0 and -3 !")
                return [heuristic(current_board, self._turn), current_board]

        if -1 > depth >= -3:
            if NUMBER_OF_NODES > 16000:
                # print("depth is between 0 and -5 !")
                return [heuristic(current_board, self._turn), current_board]

        if depth < -4:
            # print("depth is less than -2 !")
            return [heuristic(current_board, self._turn), current_board]

        if len(main_boards_choices) == 0:
            # print("no choices!")
            return [heuristic(current_board, self._turn), current_board]

        if maximizing:
            v = -float("inf")
            best_board = []
            best_choice = []
            for board_choice in main_boards_choices:
                # print("selected cell is : ", board_choice[1])
                board_value = self.alpha_beta(board_choice[0], depth - 1, alpha, beta, 0, not current_turn)[0]
                if board_value > v:
                    v = board_value
                    best_board = board_choice[0]
                    best_choice = board_choice[1]
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return [v, best_board, best_choice]

        # minimizing
        else:
            v = float("inf")
            best_board = []
            best_choice = []
            for board_choice in main_boards_choices:
                # print("selected cell is : ", board_choice[1])
                board_value = self.alpha_beta(board_choice[0], depth - 1, alpha, beta, 1, not current_turn)[0]
                if board_value < v:
                    v = board_value
                    best_board = board_choice[0]
                    best_choice = board_choice[1]
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return [v, best_board, best_choice]

    def alpha_beta_for_ai_vs_ai(self, current_board, depth, alpha, beta, maximizing, current_turn, feature_list):
        global NUMBER_OF_NODES
        NUMBER_OF_NODES += 1
        # print(current_board)
        main_boards_choices = []
        corner_boards_choices = []
        corner_neighbor_boards_choices = []
        corner_diagonal_boards_choices = []
        fair_corner_diagonal_boards_choices = []
        good_border_boards_choices = []
        fair_border_boards_choices = []
        bad_lines_boards_choices = []
        normal_boards_choices = []
        bad_boards_choices = []
        for cell_col in range(SIZE):
            for cell_row in range(SIZE):
                current_board_flip_list = []
                if self.is_valid(current_board, cell_row, cell_col, current_board_flip_list, current_turn):
                    if ((cell_row % (SIZE - 1)) == 0) and ((cell_col % (SIZE - 1)) == 0):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        corner_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif is_neighbor_of_the_corners(cell_row, cell_col):
                        if check_is_good_neighbor(current_board, cell_col, cell_row):
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list,
                                                                 current_turn)
                            normal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                        else:
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list,
                                                                 current_turn)
                            corner_neighbor_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif is_corner_diagonal(cell_row, cell_col):
                        if check_is_good_corner_diagonal(current_board, cell_col, cell_row):
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list,
                                                                 current_turn)
                            normal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                        else:
                            new_board_temp = change_color_for_AI(current_board, current_board_flip_list,
                                                                 current_turn)
                            corner_diagonal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_good_border(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        good_border_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_fair_diagonal(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        fair_corner_diagonal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_fair_border(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        fair_border_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    elif check_is_in_bad_lines(cell_col, cell_row):
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        bad_lines_boards_choices.append([new_board_temp, [cell_col, cell_row]])
                    else:
                        new_board_temp = change_color_for_AI(current_board, current_board_flip_list, current_turn)
                        normal_boards_choices.append([new_board_temp, [cell_col, cell_row]])
        if len(corner_boards_choices) > 0:
            # print("we have a good cell")
            main_boards_choices = corner_boards_choices
            # normal_boards_choices.extend(fair_border_boards_choices)
            # normal_boards_choices.extend(good_border_boards_choices)
            # normal_boards_choices.extend(fair_corner_diagonal_boards_choices)
            # len_of_random_selection = 2 - len(corner_boards_choices)
            # i = 0
            # while i < len_of_random_selection and len(normal_boards_choices) > 0:
            #     random_index = random.randint(0, len(normal_boards_choices) - 1)
            #     main_boards_choices.append(normal_boards_choices[random_index])
            #     del normal_boards_choices[random_index]
            #     i += 1
        elif len(good_border_boards_choices) > 0:
            main_boards_choices = good_border_boards_choices
            normal_boards_choices.extend(fair_border_boards_choices)
            normal_boards_choices.extend(fair_corner_diagonal_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(good_border_boards_choices)
            i = 0
            while i < len_of_random_selection and len(normal_boards_choices) > 0:
                random_index = random.randint(0, len(normal_boards_choices) - 1)
                main_boards_choices.append(normal_boards_choices[random_index])
                del normal_boards_choices[random_index]
                i += 1
        elif len(fair_corner_diagonal_boards_choices) > 0:
            main_boards_choices = fair_corner_diagonal_boards_choices
            normal_boards_choices.extend(fair_border_boards_choices)
            normal_boards_choices.extend(bad_lines_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(fair_corner_diagonal_boards_choices)
            i = 0
            while i < len_of_random_selection and len(normal_boards_choices) > 0:
                random_index = random.randint(0, len(normal_boards_choices) - 1)
                main_boards_choices.append(normal_boards_choices[random_index])
                del normal_boards_choices[random_index]
                i += 1
        elif len(fair_border_boards_choices) > 0:
            main_boards_choices = fair_border_boards_choices
            normal_boards_choices.extend(bad_lines_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(fair_border_boards_choices)
            i = 0
            while i < len_of_random_selection and len(normal_boards_choices) > 0:
                random_index = random.randint(0, len(normal_boards_choices) - 1)
                main_boards_choices.append(normal_boards_choices[random_index])
                del normal_boards_choices[random_index]
                i += 1
        elif len(normal_boards_choices) > 0:
            # print("normal cell")
            main_boards_choices = normal_boards_choices
            bad_boards_choices.extend(bad_lines_boards_choices)
            len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(normal_boards_choices)
            i = 0
            while i < len_of_random_selection and len(bad_boards_choices) > 0:
                random_index = random.randint(0, len(bad_boards_choices) - 1)
                main_boards_choices.append(bad_boards_choices[random_index])
                del bad_boards_choices[random_index]
                i += 1
        elif len(bad_lines_boards_choices) > 0:
            # print("bad cell")
            main_boards_choices = bad_lines_boards_choices
            # bad_boards_choices.extend(corner_neighbor_boards_choices)
            # len_of_random_selection = MAX_NUMB_OF_RAND_NODES - len(bad_lines_boards_choices)
            # i = 0
            # while i < len_of_random_selection and len(bad_boards_choices) > 0:
            #     random_index = random.randint(0, len(bad_boards_choices) - 1)
            #     main_boards_choices.append(bad_boards_choices[random_index])
            #     del bad_boards_choices[random_index]
            #     i += 1
        elif len(corner_neighbor_boards_choices) > 0:
            # print("bad cell")
            main_boards_choices = corner_neighbor_boards_choices
        elif len(corner_diagonal_boards_choices) > 0:
            # print("very bad cell")
            main_boards_choices = corner_diagonal_boards_choices
        # dynamic depth based on number of nodes
        if depth == 0:
            if NUMBER_OF_NODES > 6000:
                # print("depth is zero !")
                return [heuristic_for_ai_vs_ai(current_board, self._turn, feature_list), current_board]
        if 0 > depth >= -1:
            if NUMBER_OF_NODES > 11500:
                # print("depth is between 0 and -3 !")
                return [heuristic_for_ai_vs_ai(current_board, self._turn, feature_list), current_board]
        if -1 > depth >= -3:
            if NUMBER_OF_NODES > 16000:
                # print("depth is between 0 and -5 !")
                return [heuristic_for_ai_vs_ai(current_board, self._turn, feature_list), current_board]
        if depth < -4:
            # print("depth is less than -2 !")
            return [heuristic_for_ai_vs_ai(current_board, self._turn, feature_list), current_board]
        if len(main_boards_choices) == 0:
            # print("no choices!")
            return [heuristic_for_ai_vs_ai(current_board, self._turn, feature_list), current_board]
        if maximizing:
            v = -float("inf")
            best_board = []
            best_choice = []
            for board_choice in main_boards_choices:
                # print("selected cell is : ", board_choice[1])
                board_value = \
                    self.alpha_beta_for_ai_vs_ai(board_choice[0], depth - 1, alpha, beta, 0, not current_turn,
                                                 feature_list)[0]
                if board_value > v:
                    v = board_value
                    best_board = board_choice[0]
                    best_choice = board_choice[1]
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return [v, best_board, best_choice]
        # minimizing
        else:
            v = float("inf")
            best_board = []
            best_choice = []
            for board_choice in main_boards_choices:
                # print("selected cell is : ", board_choice[1])
                board_value = \
                    self.alpha_beta_for_ai_vs_ai(board_choice[0], depth - 1, alpha, beta, 1, not current_turn,
                                                 feature_list)[0]
                if board_value < v:
                    v = board_value
                    best_board = board_choice[0]
                    best_choice = board_choice[1]
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return [v, best_board, best_choice]

    def play_AI(self):
        start_time = time.time()
        # print("our board and currently board is: !", self._board)
        self._fliplist = []
        self._require_game_not_over()
        global NUMBER_OF_NODES
        NUMBER_OF_NODES = 0
        alpha_beta_search = self.alpha_beta(self._board, DEPTH, -float("inf"), float("inf"), 1,
                                            self._turn)
        # print(alpha_beta_search)
        if len(alpha_beta_search) == 3:
            coordinates_of_move = alpha_beta_search[2]
            # print(coordinates_of_move)

            can_player_make_a_move(self.search_all_directions(coordinates_of_move[1], coordinates_of_move[0]))

            if self._board[coordinates_of_move[0]][coordinates_of_move[1]] != NO_CIRCLE:
                raise MoveIsNotValidException()

            else:
                self._board[coordinates_of_move[0]][coordinates_of_move[1]] = self._turn
                self.change_color(self._fliplist)
                self.change_turn()
                self.update_score()

        end_time = time.time()
        diff_time = int(end_time - start_time)
        self.add_to_total_search_time(diff_time)
        self.total_number_of_searches += 1
        print("Search time ---> ", diff_time)
        # check if turn is AI rec
        try:
            if self.opposite_can_not_make_move_AI() and self.empty_spaces_left():
                self.change_turn()
                self.play_AI()
            else:
                raise Exception("return back")
        except Exception as e:
            print("in return back exc", e)
            return

    def play_AI_for_ai_vs_ai(self, feature_list):
        start_time = time.time()
        # print("our board and currently board is: !", self._board)
        self._fliplist = []
        self._require_game_not_over()
        global NUMBER_OF_NODES
        NUMBER_OF_NODES = 0
        alpha_beta_search = self.alpha_beta_for_ai_vs_ai(self._board, DEPTH, -float("inf"), float("inf"), 1,
                                                         self._turn, feature_list)
        # print(alpha_beta_search)
        if len(alpha_beta_search) == 3:
            coordinates_of_move = alpha_beta_search[2]
            # print(coordinates_of_move)

            can_player_make_a_move(self.search_all_directions(coordinates_of_move[1], coordinates_of_move[0]))

            if self._board[coordinates_of_move[0]][coordinates_of_move[1]] != NO_CIRCLE:
                raise MoveIsNotValidException()

            else:
                self._board[coordinates_of_move[0]][coordinates_of_move[1]] = self._turn
                self.change_color(self._fliplist)
                self.change_turn()
                self.update_score()

        end_time = time.time()
        diff_time = int(end_time - start_time)
        self.add_to_total_search_time(diff_time)
        self.total_number_of_searches += 1
        # print("Search time ---> ", diff_time)
        # check if turn is AI rec
        try:
            if self.opposite_can_not_make_move_AI() and self.empty_spaces_left():
                self.change_turn()
                self.play_AI_for_ai_vs_ai(feature_list)
            else:
                raise Exception("return back")
        except Exception as e:
            # print("in return back exc", e)

            return


def write_log(str_log):
    f = open("log.txt", "a")
    f.write(str_log)
    # f.close()
