import random

class stringDatabase:
    """Load words from a file with provided path.
    """

    def __init__(self, filePath = 'four_letters.txt'):
        """
        :param filePath: Path of the file containing the words
        """
        self.filePath = filePath
        self.word_list = []

    def set_up(self):
        """return none

        This methods reads the file from the provided path,
        reads every line and splitting the words with " " (spaces)
        as the regex.
        It stores all the words in words_file.
        """
        words_file = open('four_letters.txt')
        for line in words_file.readlines():
          self.word_list.extend(line.rstrip("\r\n").split(" "))

    def size(self):
        return len(self.word_list)

    def random_entry(self):
        random_int = random.randint(0, self.size())
        return self.word_list[random_int]

if __name__ == '__main__':
    db = stringDatabase()
    db.set_up()
    print(len(db.word_list))
    print(db.random_entry())