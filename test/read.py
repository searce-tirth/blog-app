import random

# Open the file and read all the lines into a list
with open('file.txt') as file:
    lines = file.readlines()

# Choose a random line from the list of lines
random_line = random.choice(lines).strip()

# Extract a random word from the chosen line
random_word = random_line.strip()

# Print the random word
print(random_line)