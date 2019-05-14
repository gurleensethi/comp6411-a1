formatted_result = "%d        %s     %s    %d               %d                  %0.2f"

class game:

    def __init__(self, game_number, word):
        self.game_number = game_number
        self.word = word
        self.bad_guesses = 0
        self.missed_letters = 0
        self.num_letters_requested = 0
        self.score = 0.0
        self.status = 'failure'
        self.num_matched_letters = 0
        self.matched_letters = set()
        self.guessed_letters = set()

    def guess_letter(self, guessed_letter):
        # check if user has already guessed the letter
        if guessed_letter in self.guessed_letters:
            return -1

        # record the guessed letter
        self.guessed_letters.add(guessed_letter)

        # find the number of letter matches
        guesses = 0
        for letter in self.word:
            if letter == guessed_letter:
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
        self.status = "Success"

    def give_up(self):
        self.score = 0.0

        for letter in self.word:
            if not (letter in self.matched_letters):
                self.score -= frequencies[letter]

        self.status = "Gave Up"

    def calculate_score(self):
        calculated_score = self.score

        if self.status == "Gave Up":
            return calculated_score
        else:
            if self.num_letters_requested != 0:
                calculated_score /= self.num_letters_requested

            if self.bad_guesses != 0:
                calculated_score -= self.bad_guesses * 0.9

            return calculated_score

    def build_guessed_word(self):
        printable_word = ""

        for letter in self.word:
            if letter in self.matched_letters:
                printable_word = printable_word + letter
            else:
                printable_word = printable_word + "-"

        return printable_word

    def is_game_finished(self):
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