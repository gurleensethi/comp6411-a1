formatted_result = "%d        %s     %s    %d               %d                  %0.2f"

class game:
    """Contains the state of a game.

    Contains the data related to a single game round, along with the operations
    that can be performed on the game itself.

    Attributes:
        game_number (int): Index of the game
        word (str): Word for the user to guess
        bad_guesses (int): Count of wrong guesses by the user
        score (int): Current score for the game
        status (str): Denotes if user has successed or give up
        num_matched_letters (int): number of letters uncovered by the user
        matched_letters (set): Set of all the letters successfully uncovered
            by the user.
        guessed_letters (set): Set of all the letters that the user has tried
            to uncover.
    """

    def __init__(self, game_number, word):
        self.game_number = game_number
        self.word = "mall"
        self.bad_guesses = 0
        self.missed_letters = 0
        self.num_letters_requested = 0
        self.score = 0.0
        self.status = 'failure'
        self.num_matched_letters = 0
        self.matched_letters = set()
        self.guessed_letters = set()

    def guess_letter(self, guessed_letter):
        """Guess a letter in the word.

        Guess a letter on the word in this game. If any letter is matched
        it is uncovered when being displayed to the user.

        Args:
            guessed_letter (str): The letter guessed by the user.

        Returns:
            The count of letters that were uncovered.
        """

        # check if user has already guessed the letter
        if guessed_letter in self.guessed_letters:
            return -1

        # record the guessed letter
        self.guessed_letters.add(guessed_letter)

        # find the number of letter matches
        guesses = 0
        for letter in self.word:
            # letter found
            if letter == guessed_letter:
                # increment score
                guesses += 1
                self.matched_letters.add(letter)

        self.num_matched_letters += guesses

        # decrease the number of missed letters
        if guesses == 0:
            self.missed_letters += 1

        # increment number of tries
        self.num_letters_requested += 1

        # if all the letters have been found, change status to success.
        if self.num_matched_letters == 4:
            self.status = "Success"

        return guesses

    def guess_word(self, guessed_word):
        """Guess an entire word.

        Checks if the provided word is equal to the word stored
        in the game. The game should end if correct word is guessed.

        Args:
            guessed_word (str): The word guessed by the user.

        Returns:
            True if the guess was correct, False otherwise.
        """
        has_guessed = self.word == guessed_word

        if has_guessed:
            self.status = "Success"

            #find score of uncovered words
            for letter in self.word:
                if not (letter in self.matched_letters):
                    self.score += frequencies[letter]

            for letter in guessed_word:
                self.matched_letters.add(letter)
        else:
            self.bad_guesses += 1

        return has_guessed

    def game_success(self):
        """Mark the status of game as success."""
        self.status = "Success"

    def give_up(self):
        """Mark the status of game as given up.

        Change the status of current game to 'Gave Up'.
        Abandon the current score and calculate it from the
        letters that are still uncovered.
        """
        self.score = 0.0

        for letter in self.word:
            if letter in self.matched_letters:
                self.score -= frequencies[letter]

        self.status = "Gave Up"

    def calculate_score(self):
        """Get the final score of the game.

        If user has give up, currently recoded score is returned.
        Else, score is calculated with following penalities.
            - Score is divided by the number of letters requested
              by the user. (only if non zero)
            - For every wrong word guess, 10% is deducted from the score.

        Returns:
            Final calculated score.
        """
        calculated_score = self.score

        if self.status == "Gave Up":
            return calculated_score
        else:
            if self.num_letters_requested != 0:
                calculated_score /= self.num_letters_requested

            if self.bad_guesses != 0:
                for i in range(self.bad_guesses):
                    calculated_score *= 0.90

            return calculated_score

    def build_guessed_word(self):
        """Get word with uncovered letters.

        Builds the presentable word by replacing '-' with the
        letters that have been successfully uncovered by the user.

        Returns:
            Hidden word but showing uncovered letters.
        """
        printable_word = ""

        for letter in self.word:
            if letter in self.matched_letters:
                printable_word = printable_word + letter
            else:
                printable_word = printable_word + "-"

        return printable_word

    def is_game_finished(self):
        """Has the game be finished.

        Game only finishes status has been changed to "success"
        or user has given up.

        Returns:
            True if game has finished, False otherwise.
        """
        return self.status == "Gave Up" or self.status == "Success"

    def __str__(self):
        #print("Game    Word     Status      Bad Guesses    Missed Letters    Score")
        return formatted_result % (self.game_number, self.word, self.status, self.bad_guesses, self.missed_letters, self.calculate_score())

if __name__ == '__main__':
    g = game(1, 'test')
    g.increment_bad_guess()
    print(g.formatted_result())

# frequency dict to calculate score
frequencies = {
    'a': 8.17,
    'b': 1.49,
    'c': 2.78,
    'd': 4.25,
    'e': 12.70,
    'f': 2.23,
    'g': 2.02,
    'h': 6.09,
    'i': 6.97,
    'j': 0.15,
    'k': 0.77,
    'l': 4.03,
    'm': 2.41,
    'n': 6.75,
    'o': 7.51,
    'p': 1.93,
    'q': 0.10,
    'r': 5.99,
    's': 6.33,
    't': 9.06,
    'u': 2.76,
    'v': 0.98,
    'w': 2.36,
    'x': 0.15,
    'y': 1.97,
    'z': 0.07,
}