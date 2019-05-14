words_file = open('four_letters.txt')

word_list = []

for line in words_file.readlines():
  word_list.extend(line.rstrip("\r\n").split(" "))

print(word_list)