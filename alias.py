from classes import Arguments, Alias


def main():
    arguments = Arguments()
    arg = arguments.create_args()
    alias = Alias(arg.dictionary, arg.number_of_teams, arg.time, arg.number_of_words)
    alias.get_data()


if __name__ == "__main__":
    main()
