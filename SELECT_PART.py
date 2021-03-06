import random
import othello as oth

DEPTH_OF_ALGORITHM = 2
CURRENT_GAME_NUMBER = 0


def write_log(str_log, adr, file_name):
    comp_adr = adr + "/" + file_name + ".txt"
    f = open(comp_adr, "a")
    f.write(str_log)
    # f.close()


def read_pop(adr, file_name):
    comp_adr = adr + "/" + file_name + ".txt"
    f = open(comp_adr, "r")
    return f.read()


def pop_sort(current_node):
    return current_node[2]


def ai_vs_ai(game_logic_instance, population, k, r, turn_inp):
    i = 0
    if turn_inp:
        while game_logic_instance._winner == None:
            print(i)
            try:
                if game_logic_instance._turn:
                    print(population[r][k][0])

                    game_logic_instance.play_AI_for_ai_vs_ai(population[r][k][0])
                else:
                    game_logic_instance.play_AI()
            except Exception as e:
                print(e)
                pass
            if not game_logic_instance.is_game_over():
                game_logic_instance.determine_winner()
            i += 1
    else:
        while game_logic_instance._winner == None:
            print(i)
            try:
                if game_logic_instance._turn:
                    game_logic_instance.play_AI()

                else:
                    print(population[r][k][0])
                    game_logic_instance.play_AI_for_ai_vs_ai(population[r][k][0])

            except Exception as e:
                print(e)
                pass
            if not game_logic_instance.is_game_over():
                game_logic_instance.determine_winner()
            i += 1


def print_board(game_logic_instance):
    for t in game_logic_instance._board:
        for pp in t:
            print(pp, end=" ")
        print()


def run_algorithm():
    population = [[[[-68, 67, 96, -52, 98, 9, -12, -124, 7, 2, 8], 0, 4.4375, 1],
                   [[95, 66, -50, -20, 88, 53, -148, 14, -8, -15, -4], 0, 4, 1],
                   [[61, 53, -27, -35, 76, 50, -120, 23, -8, 14, -4], 0, 3.8125, 1],
                   [[108, -38, -55, 45, -48, -29, 123, -116, -13, 6, 3], 0, 3.5, 1],
                   [[-102, -104, 49, -102, 93, 51, 8, -57, 2, 5, -5], 0, 3, 1]],
                  [[[106, -59, -76, -60, 129, -103, -47, 5, -13, 6, 6], 0, 5.0, 1],
                   [[116, 23, -75, 75, -38, -76, -94, -8, -12, 10, 7], 0, 5, 1],
                   [[54, 49, 30, -96, 80, -55, 2, -24, -14, -3, -1], 0, 4.375, 1],
                   [[69, -110, -2, 61, 67, -58, -32, -35, 16, 12, 14], 0, 3.5, 1],
                   [[88, -22, -42, -63, -47, -81, -122, -40, -10, 10, 5], 0, 2, 1]],
                  [[[-103, -110, -2, -66, 119, -81, -64, -23, -13, 3, 9], 0, 5, 1],
                   [[78, 142, -65, -70, 68, -154, -80, -58, -9, 0, 13], 0, 4.625, 1],
                   [[-78, -134, 30, -96, 80, -55, 2, -99, 8, -3, -1], 0, 4.5, 1],
                   [[125, 61, -81, -11, 116, 82, 69, -24, -14, 13, 2], 0, 4.0, 1],
                   [[113, -78, -78, 83, -27, -82, -120, 23, -8, 4, -15], 0, 3, 1]],
                  [[[39, -35, 108, -79, 98, -72, 34, -64, 8, 9, 2], 0, 5.48828125, 1],
                   [[-6, 0, -11, -89, 96, -59, 25, -159, 4, -11, -5], 0, 5, 1],
                   [[31, 63, 12, -39, 93, 24, 3, -19, 8, 1, 2], 0, 4, 1],
                   [[-32, 31, -44, -39, 93, 24, 3, -146, 3, -1, 2], 0, 3.75, 1],
                   [[-32, 31, -44, -39, 93, 24, 3, -146, 3, -9, -6], 0, 3.5, 1]],
                  [[[56, -64, 10, -61, -48, -34, -110, -63, 2, 0, 1], 0, 6.0, 1],
                   [[56, -110, -2, 61, 67, -58, -32, -63, 2, 0, 1], 0, 5, 1],
                   [[61, 53, -27, -35, 76, 50, -120, 23, -8, 2, -4], 0, 4.953125, 1],
                   [[113, -78, -78, 83, -27, -81, -64, -23, -13, 3, 9], 0, 3.1875, 1],
                   [[41, -75, 9, -45, -13, -19, -117, -62, 18, 8, 14], 0, 2, 1]],
                  [[[31, 63, 12, -83, 106, -84, 22, -19, 8, 1, 2], 0, 6.0, 1],
                   [[96, -53, -74, 108, -56, -83, 21, 58, -11, 15, -19], 0, 5, 1],
                   [[78, -60, -101, -66, 119, -82, -58, -70, -7, 8, 11], 0, 3.890625, 1],
                   [[116, -22, -75, 75, -38, -76, -94, -8, -12, 10, 7], 0, 3.4375, 1],
                   [[-145, -93, -127, 59, 101, -35, -65, 22, -16, 14, 10], 0, 3, 1]],
                  [[[83, 129, -87, -50, 68, -184, -83, -63, -23, 1, 15], 0, 6.5, 1],
                   [[90, -44, -80, -77, 68, -154, -72, 5, -13, 10, 7], 0, 4.5, 1],
                   [[69, -110, -2, 61, 67, -103, -32, -35, 16, 12, 14], 0, 4.1875, 1],
                   [[78, 142, -65, -70, 68, -154, -80, -170, 3, 0, 13], 0, 3, 1],
                   [[50, 81, -86, -39, 90, 23, -5, -46, -8, 0, 3], 0, 2, 1]],
                  [[[88, 23, -42, -63, -47, -81, -122, -24, -10, 10, 5], 0, 6, 1],
                   [[-85, 58, 77, -82, 133, -76, 31, -14, -13, 11, 9], 0, 5.84375, 1],
                   [[-103, -44, -78, 66, 55, 25, -148, 14, -8, 5, -15], 0, 3.25, 1],
                   [[-103, -110, -2, -66, 119, -82, -120, 23, -8, 4, -15], 0, 3.0, 1],
                   [[-88, -166, 61, -72, 104, -36, -14, -14, -12, -2, 3], 0, 3, 1]],
                  [[[38, 81, -67, -19, 71, 49, 22, -170, 3, -4, 3], 0, 7.0, 1],
                   [[-64, 36, -47, -21, 26, -35, 11, -158, 11, -9, -3], 0, 4.75, 1],
                   [[61, 66, -50, -20, 88, 20, 12, -70, -7, 8, 11], 0, 4, 1],
                   [[106, -37, -24, 104, -65, -87, -90, -41, -3, 7, 15], 0, 3.34375, 1],
                   [[78, 53, -27, -35, 76, 50, -120, 23, -8, 14, -4], 0, 1, 1]],
                  [[[54, -117, 32, 83, 72, -76, 31, -23, 12, 8, 10], 0, 5.78125, 1],
                   [[-103, -44, -78, 66, 55, 25, 77, -16, 1, 4, -15], 0, 4.9375, 1],
                   [[-78, -134, 30, -96, 80, -55, 2, -24, -14, -3, -1], 0, 3.078125, 1],
                   [[31, 63, 12, -83, 72, -76, 31, -51, -11, 1, 2], 0, 3, 1],
                   [[-92, -114, 32, -73, 106, -84, 22, -19, 8, 15, -3], 0, 3, 1]]]
    i = 0
    turn = True
    while i < DEPTH_OF_ALGORITHM:
        print("step of algorithm: ", i)
        # write_log(str(population), "logs/step" + str(i), str("population"))

        for j in range(2):
            for r in range(10):
                for k in range(len(population[r])):
                    print(population[k][0][0])
                    # create an instance of othello logic
                    game_logic_instance = oth.GameLogic()
                    game_logic_instance.create_board()
                    # play AI VS AI
                    ai_vs_ai(game_logic_instance, population, k, r, turn)
                    # for fitness func
                    if game_logic_instance._winner == oth.BLACK:
                        if turn == True:
                            population[r][k][2] += 1
                        else:
                            pass
                    elif game_logic_instance._winner == oth.WHITE:
                        if turn == True:
                            pass
                        else:
                            population[r][k][2] += 1

                    write_log("turn is " + str(turn) + "  |   winner is " + str(game_logic_instance._winner) + "\n",
                              "logs/step15", "select_part" + str(i))

                    global CURRENT_GAME_NUMBER
                    CURRENT_GAME_NUMBER += 1
                    print(CURRENT_GAME_NUMBER)
                    print(game_logic_instance._winner)
                    print(game_logic_instance._black_points)
                    print(game_logic_instance._white_points)
                    print_board(game_logic_instance)

        i += 1
        turn = not turn
    temp = []
    for i in range(len(population)):
        temp.extend(population[i])

    temp.sort(key=pop_sort)

    write_log(str(population),
              "logs/step15", "pops")
    write_log(str(temp),
              "logs/step15", "temp")
    return temp


run_algorithm()
