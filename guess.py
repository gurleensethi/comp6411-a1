from game import game
from stringDatabase import stringDatabase
import random
import enum

menu = """
** The great guessing game **

Current Guess: %s

g = guess, t = tell me, l for a letter, and q to quit
"""

quit_confirmation_message = """
#
# Are you sure you want to quit(y/n)?
#
"""

invalid_option_message = """
#
# Select a valid option!
#
"""

invalid_letter_message = """
@
@ Enter a valid letter!
@
"""

wrong_guess_message = """
@
@ Your guess was absolutely wrong!
@
"""

no_matches_found = "No letter matched!"

matches_found = """
= = = = = = = = = = = = = = = = = =
= Awesome, you found %d matches.   =
= = = = = = = = = = = = = = = = = =
"""

already_guessed_letter = "You have already guessed '%c'"

def log(message):
    formatted_message = "@        " + message + "      @"
    print()
    print("#" * (len(message) + 16))
    print(formatted_message)
    print("#" * (len(message) + 16))
    print()

class menu_options(enum.Enum):
    guess = 0
    tell_me = 1
    letter = 2
    quit_game = 3
    none = 4

class guess:

    def __init__(self):
        self.db = stringDatabase()
        self.db.set_up()
        self.games = []
        self.current_game = None

    def start(self):
        is_game_running = True
        self.start_new_game()
        while is_game_running:
            self.print_menu()

            is_game_running = self.handle_option(self.read_option())

            # if user quits the game print the final table and score
            if not is_game_running:
                self.display_result()

            # check if games has finished (user guessed all letters)
            if self.current_game.is_game_finished():
                if self.current_game.status == "Success":
                    log("Awesome you succeded!")
                log("Starting New Game")
                self.start_new_game()

    def read_option(self):
        user_input = input("")
        if user_input == 'g':
            return menu_options.guess
        elif user_input == 'l':
            return menu_options.letter
        elif user_input == 't':
            return menu_options.tell_me
        elif user_input == 'q':
            return menu_options.quit_game
        else:
            print(invalid_option_message)
            return menu_options.none

    def handle_option(self, option):
        if option == menu_options.quit_game:
            user_input = input(quit_confirmation_message)
            return not (user_input == 'y')
        elif option == menu_options.letter:
            self.handle_letter()
        elif option == menu_options.guess:
            self.handle_guess()
        elif option == menu_options.tell_me:
            self.handle_tell_me()
        return True

    def handle_letter(self):
        user_input = input("Enter a letter:\n")
        if len(user_input) > 1 or len(user_input) < 1 or (not user_input.isalpha()):
            print(invalid_letter_message)
            return True
        else:
            correct_guesses = self.current_game.guess_letter(user_input)
            if correct_guesses == -1:
                log(already_guessed_letter % user_input)
            elif correct_guesses == 0:
                log(no_matches_found)
            else:
                print(matches_found % correct_guesses)

        return True

    def handle_tell_me(self):
        self.current_game.give_up()
        log("The word was '%s'" % self.current_game.word)

    def handle_guess(self):
        user_input = input("Enter a guess:\n")
        has_guessed = self.current_game.guess_word(user_input)

    def print_menu(self):
        print()
        print(self.current_game.word)
        print()
        print(menu % self.current_game.build_guessed_word())

    def start_new_game(self):
        # generate random word and game id
        random_word = self.db.random_entry()
        game_id = len(self.games) + 1
        # create new game
        self.current_game = game(game_id, random_word)
        # store the game in list
        self.games.append(self.current_game)

    def display_result(self):
        print("\n")
        print("Game     Word     Status     Bad Guesses     Missed Letters     Score")
        print("____     ____     ______     ___________     ______________     _____")
        print("\n")
        for game in self.games:
            if game.is_game_finished():
                print(game)
        print("\n")

if __name__ == '__main__':
    g = guess()
    g.start()