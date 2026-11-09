
import random

# List of words
words = ["python", "computer", "programming", "developer", "keyboard"]

# Select a random word
word = random.choice(words)

guessed_letters = []
wrong_guesses = 0
max_attempts = 6

print("===== WELCOME TO HANGMAN GAME =====")

while wrong_guesses < max_attempts:

    # Display hidden word
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    print("\nWord:", display)
    print("Wrong guesses left:", max_attempts - wrong_guesses)

    # Check winning condition
    if all(letter in guessed_letters for letter in word):
        print("\nCongratulations! You Won!")
        break

    # Take user input
    guess = input("Guess a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter only one alphabet!")
        continue

    if guess in guessed_letters:
        print("You already guessed this letter!")
        continue

    guessed_letters.append(guess)

    if guess in word:
        print("Correct Guess!")
    else:
        print("Wrong Guess!")
        wrong_guesses += 1

else:
    print("\nGame Over! You Lost.")
    print("The correct word was:", word)

print("\nThanks for playing!")
