#!/usr/bin/env python3

from colorama import init, Style, Back
from urllib.request import urlopen
from random import choice

DEFAULTURL = "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"


def get_words(url):
    return [line.strip() for line in urlopen(url)]


def check_guess_validity(guess):
    if len(guess) != 5:
        print("Please enter a 5-letter word")
        return False
    elif guess.encode("utf-8") not in words:
        print("Unknown word, try again")
        return False
    else:
        return True


def get_guesses(attempts, words):
    # TODO for some reason attempt doesn't increase
    for attempt in range(1, attempts+1):
        print(f"Enter your next guess:")
        while True:
            guess = input(f"[{attempt}] ")
            if check_guess_validity(guess):
                yield attempt, guess




if __name__=="__main__":
    init()
    words = get_words(DEFAULTURL)
    word = choice(words).decode("utf-8")

    print("Let's play wordle!")
    print(f"Correct word (for testing): {word}")

    output = []
    for attempt, guess in get_guesses(attempts=6, words=words):

        for i in range(len(guess)):
            if guess[i] == word[i]:
                output.append(Back.GREEN)
            elif guess[i] in word:
                output.append(Back.YELLOW)
            output.append(guess[i])
            output.append(Style.RESET_ALL)
        print("".join(output))
        if word == guess:
            print(f"Congrats! You needed {attempt} attempts")
            break
    else:
        print(f"Bad luck! We were looking for {word}")
