import argparse
import random
import time as tm
import json


class Arguments:
    @staticmethod
    def create_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-d",
            "--dictionary",
            default="easy",
            type=str,
            choices=["easy", "medium", "hard", "jazda", "my_dict"],
            help="Possible dictionaries: easy, medium, hard, jazda, my_dict",
        )
        parser.add_argument(
            "-n",
            "--number_of_teams",
            default=2,
            type=int,
            choices=[x for x in range(2, 7)],
            help="Number of teams (2 to 6)",
        )
        parser.add_argument(
            "-t",
            "--time",
            default=60,
            type=int,
            choices=[x for x in range(30, 301, 30)],
            help="Round duration (from 30 to 300 seconds, every 30)",
        )
        parser.add_argument(
            "-w",
            "--number_of_words",
            default=50,
            type=int,
            choices=[x for x in range(10, 101, 10)],
            help="Number of words to win (10 to 100, every 10)",
        )
        args_func = parser.parse_args()
        return args_func


class Alias:
    def __init__(self, dictionary, number_of_teams, time, number_of_words):
        self.dictionary = dictionary
        self.number_of_teams = number_of_teams
        self.time = time
        self.number_of_words = number_of_words
        with open("dictionaries.json") as d:
            self.dictionaries = json.load(d)

    def edit_points(self, round_points, team_points, team):
        try:
            true_points = input()
            if true_points == "":
                team_points[team] += round_points
                return team_points

            elif true_points.isdigit():
                if abs(int(true_points) - round_points) < 5:
                    team_points[team] += int(true_points)
                    return team_points

                else:
                    print("Попахивает брехней. Давай еще раз)")
                    return self.edit_points(round_points, team_points, team)

            elif true_points[0] == "-" and true_points[1:].isdigit():
                if abs(int(true_points[1:]) + round_points) < 5:
                    team_points[team] += int(true_points[1:]) * -1
                    return team_points

                else:
                    print("Попахивает брехней. Давай еще раз)")
                    return self.edit_points(round_points, team_points, team)

            else:
                print("Не верное значение, введите число очков набранных в раунде")
                return self.edit_points(round_points, team_points, team)
        except UnicodeDecodeError:
            print("Что за буквы!?? Число нужно!")
            self.edit_points(round_points, team_points, team)

    def get_data(self):
        selected_dict = self.dictionaries[self.dictionary]
        team_names = [input(f"Имя {x + 1} команды: ") for x in range(self.number_of_teams)]
        check_team_names = [
            f"Безымянные петухи {i + 1}" if val == "" else val for i, val in enumerate(team_names)
        ]
        team_points = {x: 0 for x in check_team_names}
        check = True
        win = {}
        print(
            """
            Правила игры: нужно суметь объяснить другими словами разгадываемое слово с помощью 
            объяснений, синонимов, антонимов и намёков, достичь того, чтобы компаньоны по игре 
            отгадали как можно больше указанных в карточке слов. Команда, которая подойдёт к 
            финишу первой, становится победителем. Если разъясняющий сделает ошибку в своем 
            разъяснении, то ответ не засчитывается и команда получает за это штраф в виде одного 
            минусового шага. Минимальное количество игроков 4, но может и 2 быть.
            
            Чтобы засчитать отгаданное слово - введите '1' и нажмите 'Enter'. В противном случае -
            введите любое иное значение либо просто нажмите 'Enter'.
        """
        )
        while check:
            for i in check_team_names:
                input(f"\nКоманда {i} \nНажмите 'Enter' для начала:")
                random.shuffle(selected_dict)
                circle = 0
                round_points = 0
                start_time = tm.time()
                while tm.time() - start_time < self.time:
                    time_round = self.time - (tm.time() - start_time)
                    print(f"{selected_dict[circle]} ({int(time_round)}с <-> {round_points})")
                    keyword = input()
                    if keyword == "1":
                        round_points += 1
                    else:
                        round_points -= 1
                    if circle < len(selected_dict) - 1:
                        circle += 1
                    else:
                        circle = 0

                print(
                    f"Набрано за раунд {round_points}, если нужно редактировать введите верное "
                    "число иначе нажмите 'Enter':"
                )
                self.edit_points(round_points, team_points, i)
                [print(f"{team} --> {points}") for team, points in team_points.items()]

            for team, points in team_points.items():
                if points >= self.number_of_words:
                    win[team] = points

            if len(win) == 0:
                continue

            elif len(win) == 1:
                print("Мои искренние поздравление умники!!!")
                check = False
            else:
                max_value = max(win.values())
                final_dict = {k: v for k, v in win.items() if v == max_value}
                if len(final_dict) == 1:
                    [print(f"Все красавцы, но {team} лучшие!!!") for team in final_dict.keys()]
                    check = False
                else:
                    check_team_names = []
                    [check_team_names.append(team) for team in final_dict.keys()]
                    team_points = final_dict
                    print("Ох, жара, продолжаем с лучшими!")
