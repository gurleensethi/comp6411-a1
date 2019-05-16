from game import game
from stringDatabase import stringDatabase
import random
import enum
import sys

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

invalid_option_message = "Select a valid option!"
invalid_letter_message = "Enter a valid letter!"
wrong_guess_message = "Your guess was absolutely wrong!"
no_matches_found = "No letter matched!"
matches_found = "Awesome, you found %d matches."
already_guessed_letter = "You have already guessed '%c'"

def log(message):
    """Helper function for printing logs.

    Prints the provided message in a decorated text box.

    Args:
        message (str): Message to be printed.
    """
    formatted_message = "@        " + message + "      @"
    print()
    print("#" * (len(message) + 16))
    print(formatted_message)
    print("#" * (len(message) + 16))
    print()

class menu_option(enum.Enum):
    """Enums representing the available menu options
    in the game."""
    guess = 0
    tell_me = 1
    letter = 2
    quit_game = 3
    none = 4

class guess:
    """A class that represents the game itself.

    It carries out functionality of displaying the menu,
    getting user input and overall flow of the game.

    Attributes:
        db (stringDatabase): Database containing list of words, also used to get a random word.
        games (list): List of all the games played by the user.
        current_game (game): Points to the current game being played.
    """

    def __init__(self):
        self.db = stringDatabase()
        self.db.set_up()
        self.games = []
        self.current_game = None

    def start(self):
        """Start the game.

        Creates a new game, displays the menu and waits for user input.
        Game keeps on going until the user chosses to quit using 'q' or
        terminates the program.
        """

        # start a new game
        is_game_running = True
        self.start_new_game()

        while is_game_running and self.are_rounds_left():
            self.print_menu()

            is_game_running = self.handle_option(self.read_option())

            # check if games has finished (user guessed all letters)
            if self.current_game.is_game_finished():
                # store the game in list
                self.games.append(self.current_game)

                if self.current_game.status == "Success":
                    log("Awesome you succeded!")

                log("Starting New Game")
                self.start_new_game()

        self.display_result()

    def read_option(self):
        """"Reads user input for the menu.

        Reads input from the user and maps it to appropriate menu_option enum.

        Returns:
            menu_option mapped from user input.
        """
        user_input = input("")
        if user_input == 'g':
            return menu_option.guess
        elif user_input == 'l':
            return menu_option.letter
        elif user_input == 't':
            return menu_option.tell_me
        elif user_input == 'q':
            return menu_option.quit_game
        else:
            log(invalid_option_message)
            return menu_option.none

    def handle_option(self, option):
        """Take action againts the user input.

        Routes the mapped user input to the appropriate function.

        Args:
            option (menu_option): option mapped from user input.

        Returns:
            True if user wants to exit the game, False otherwise.
        """
        if option == menu_option.quit_game:
            user_input = input(quit_confirmation_message)
            return not (user_input == 'y')
        elif option == menu_option.letter:
            self.handle_letter()
        elif option == menu_option.guess:
            self.handle_guess()
        elif option == menu_option.tell_me:
            self.handle_tell_me()

        return True

    def handle_letter(self):
        """Get a letter from user and pass to game object.

        Takes a letter input from the user and guesses the letter on the game.
        """
        user_input = input("Enter a letter:\n")
        if len(user_input) > 1 or len(user_input) < 1 or (not user_input.isalpha()):
            log(invalid_letter_message)
        else:
            correct_guesses = self.current_game.guess_letter(user_input)
            if correct_guesses == -1:
                log(already_guessed_letter % user_input)
            elif correct_guesses == 0:
                log(no_matches_found)
            else:
                log(matches_found % correct_guesses)

    def handle_tell_me(self):
        """Give up and show the correct word.

        Finish the current game by giving up and showing the current word
        to the user."""
        self.current_game.give_up()
        log("The word was '%s'" % self.current_game.word)

    def handle_guess(self):
        """Get a word from user and pass to game object.

        Takes a word input from the user and guesses the letter on the game.
        """
        user_input = input("Enter a guess:\n")
        has_guessed = self.current_game.guess_word(user_input)

    def print_menu(self):
        """Print the menu.

        Print the game menu along with the uncovered letters of the
        current game."""
        if is_debug:
            print()
            print("Current word is: " + self.current_game.word)
            print()
        print(menu % self.current_game.build_guessed_word())

    def start_new_game(self):
        # generate random word and game id
        random_word = self.db.random_entry()
        game_id = len(self.games) + 1
        # create new game
        self.current_game = game(game_id, random_word)

    def display_result(self):
        """Display the final result of all games.

        Print out the result of all games in a tabular form, along with
        the final score."""

        if len(self.games) == 0:
            log("You did not complete any game :(")
        else:
            print("\n")
            print("Game     Word     Status     Bad Guesses     Missed Letters     Score")
            print("____     ____     ______     ___________     ______________     _____")
            print("\n")

            total_score = 0
            for game in self.games:
                if game.is_game_finished():
                    total_score += game.calculate_score()
                    print(game)
            print("\n")
            print("Final Score: %0.2f" % total_score)
            print("\n")

    def are_rounds_left(self):
        """Tells if 100 range rounds are over or not.

        Returns:
            True if 100 rounds are reached, False otherwise.
        """
        return len(self.games) < 100

if __name__ == '__main__':
    # check if running in debug mode
    is_debug = '--debug' in sys.argv
    g = guess()
    g.start()