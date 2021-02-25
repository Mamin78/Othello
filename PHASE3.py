import random
import othello as oth

SIZE_OF_EARLY_POP = 50
DEPTH_OF_ALGORITHM = 15
NUMBER_OF_LEAGUES = 10
NUMBER_OF_CROSSOVER = 10

CURRENT_GAME_NUMBER = 0


def p(pi, mi, ni):
    pass


def write_log(str_log, adr, file_name):
    comp_adr = adr + "/" + file_name + ".txt"
    f = open(comp_adr, "a")
    f.write(str_log)
    # f.close()


def fitness(node):
    if node[3] == 1:
        node[2] = (node[2] + node[1]) / 2
    else:
        node[2] = node[1]


def crossover(population, children):
    # select two random parent for crossover
    first_parent_index = random.randint(0, len(population) - 1)
    second_parent_index = random.randint(0, len(population) - 1)
    # create two random point for multiple points crossover
    first_point = random.randint(0, len(population[first_parent_index][0]) - 2)
    second_point = random.randint(first_point + 1, len(population[first_parent_index][0]) - 1)

    first_child = population[first_parent_index][0][:first_point] + population[second_parent_index][0][
                                                                    first_point:second_point] + population[
                                                                                                    first_parent_index][
                                                                                                    0][
                                                                                                second_point:]
    second_child = population[second_parent_index][0][:first_point] + population[first_parent_index][0][
                                                                      first_point:second_point] + population[
                                                                                                      second_parent_index][
                                                                                                      0][
                                                                                                  second_point:]
    children.append([first_child, 0, 0, 0])
    children.append([second_child, 0, 0, 0])


def mutation(children, child_index):
    possibility_of_mutation = random.randint(0, 100)
    if possibility_of_mutation <= 30:
        for i in range(8):
            noise = random.randint(-35, 35)
            children[child_index][0][i] += noise
        for i in range(8, 11):
            noise = random.randint(-4, 4)
            children[child_index][0][i] += noise


def generate_early_population():
    early_population = []
    for node in range(SIZE_OF_EARLY_POP):
        early_population.append([generate_random_feature(), 0, 0, 0])
        write_log(str(early_population[node][0]), "logs/early_population", str(node))
        # write_log("\n", "logs/early_population", str(node))
        # write_log(str(early_population[node][1]), "logs/early_population", str(node))
    return early_population


def generate_random_feature():
    feature_list = []
    for i in range(8):
        feature_list.append(random.randint(-120, 120))
    for i in range(8, 11):
        feature_list.append(random.randint(-15, 15))
    return feature_list


def ai_vs_ai(game_logic_instance, league, black_ind, white_ind):
    i = 0
    while game_logic_instance._winner == None:
        # print(i)
        try:
            if game_logic_instance._turn:
                game_logic_instance.play_AI_for_ai_vs_ai(league[black_ind][0])
            else:
                game_logic_instance.play_AI_for_ai_vs_ai(league[white_ind][0])
        except Exception as e:
            # print(e)
            pass
        if not game_logic_instance.is_game_over():
            game_logic_instance.determine_winner()
        i += 1


def create_empty_leagues():
    leagues = []
    for i in range(NUMBER_OF_LEAGUES):
        leagues.append([])
    return leagues


def league_sort(current_node):
    return current_node[2]


def print_board(game_logic_instance):
    for t in game_logic_instance._board:
        for pp in t:
            print(pp, end=" ")
        print()


def run_algorithm():
    population = generate_early_population()
    i = 0
    while i < DEPTH_OF_ALGORITHM:
        print("step of algorithm: ", i)
        write_log(str(population), "logs/step" + str(i), str("population"))
        leagues = create_empty_leagues()

        len_of_every_league = len(population) // NUMBER_OF_LEAGUES
        # create leagues from population
        for j in range(NUMBER_OF_LEAGUES):
            leagues[j] = population[len_of_every_league * j:len_of_every_league * (j + 1)]

        children = []
        # crossover part (multiple points[2 points])
        # generate children from parents with crossover
        for j in range(NUMBER_OF_CROSSOVER):
            crossover(population, children)
        write_log(str(children), "logs/step" + str(i), str("crossover"))

        # mutation part with possibility of 30
        for j in range(len(children)):
            mutation(children, j)
        write_log(str(children), "logs/step" + str(i), str("mutation"))
        population = []
        for j in range(NUMBER_OF_LEAGUES):
            write_log("leagues games: \n", "logs/step" + str(i), str("league") + str(j))
            for k in range(len(leagues[j])):
                for r in range(len(leagues[j])):
                    if r == k:
                        continue
                    # create an instance of othello logic
                    game_logic_instance = oth.GameLogic()
                    game_logic_instance.create_board()
                    # play AI VS AI
                    ai_vs_ai(game_logic_instance, leagues[j], k, r)
                    # for fitness func
                    if game_logic_instance._winner == oth.BLACK:
                        leagues[j][k][1] += 1
                    elif game_logic_instance._winner == oth.WHITE:
                        leagues[j][r][1] += 1

                    write_log("black is " + str(k) + "   |   white is " + str(r) + "   /   " +
                              "Black points => " + str(
                        game_logic_instance._black_points) + " | " + "White points => " + str(
                        game_logic_instance._white_points) + " || winner : " + str(game_logic_instance._winner) + "\n",
                              "logs/step" + str(i), str("league") + str(j))

                    global CURRENT_GAME_NUMBER
                    CURRENT_GAME_NUMBER += 1
                    print(CURRENT_GAME_NUMBER)
                    print(game_logic_instance._winner)
                    print(game_logic_instance._black_points)
                    print(game_logic_instance._white_points)
                    print_board(game_logic_instance)

        write_log(str(leagues), "logs/step" + str(i), str("leagues_after_games"))

        for j in range(NUMBER_OF_LEAGUES):
            for k in range(len(leagues[j])):
                fitness(leagues[j][k])
                leagues[j][k][1] = 0
            leagues[j].sort(key=league_sort, reverse=True)

            for r in range(len(leagues[j])):
                leagues[j][r][3] = 1
            # for k in range(3):
            #     population.append(leagues[j][k])

        write_log(str(leagues), "logs/step" + str(i), str("leagues_after_games_after_sort"))
        population = []
        for j in range(NUMBER_OF_LEAGUES):
            leagues[j][3] = children[0]
            del children[0]

            leagues[j][4] = children[0]
            del children[0]

            population.extend(leagues[j])
        i += 1


run_algorithm()
