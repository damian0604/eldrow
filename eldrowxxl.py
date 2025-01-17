#!/usr/bin/env python3

from colorama import init, Style, Back
from urllib.request import urlopen
from random import choice
from typing import Literal
import argparse

URLS = {"EN": "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"}

# TODO still add more type hints
# TODO return scores, maybe save them?
# TODO add docstrings
# TODO turn into module?
# TODO unittesting ;-) ?
# TODO think about what should be inside and/or outside of the class
# ...


class GuessedLetter:
    def __init__(self, letter: str, status: Literal['RED', 'YELLOW', 'GREEN']):
        self.status = status
        self.letter = letter


def render_result(evaluated_guess):
    colorama_map = {"GREEN": Back.GREEN,
                    "RED": Back.RED,
                    "YELLOW": Back.YELLOW}

    for evaluated_letter in evaluated_guess:
        print(colorama_map[evaluated_letter.status],end="")
        print(evaluated_letter.letter,end="")
    print(Style.RESET_ALL)



def get_words(language: str = 'EN') -> list:
    url = URLS.get(language, None)
    if not url:
        raise NotImplementedError(f"Language {language} not available")
    return [line.strip().decode("utf=8") for line in urlopen(url)]


class Wordle():
    def __init__(self, language="EN", attempts=6):
        self.words = get_words(language)
        self.solution = choice(self.words)
        self.max_attempts = attempts
        self.current_attempt = 0
        self.history = []
        # we need to initalize colorama as well
        init()

    def _check_guess_valid(self, guess):
        if len(guess) != 5:
            print("Please enter a 5-letter word")
            return False
        elif guess not in self.words:
            print("Unknown word, try again")
            return False
        else:
            return True

    def _check_guess_correct(self):
        guess = self.history[-1]
        result = []
        for i in range(len(guess)):
            if guess[i]==self.solution[i]:
                result.append(GuessedLetter(guess[i], 'GREEN'))
            elif guess[i] in self.solution:
                result.append(GuessedLetter(guess[i], 'YELLOW'))
            else:
                result.append(GuessedLetter(guess[i], 'RED'))
        return result


    def play(self):
        while True:
            if self.current_attempt == self.max_attempts:
                print(f"You already had {self.max_attempts} guesses!")
                print("So I guess you lost...")
                break
            guessed = self.guess()
            if guessed:
                print("CONGRATULATIONS!!")
                break

    def guess(self):
        self.current_attempt += 1
        while True:
            current_guess = input(f"[{self.current_attempt}] ")
            if self._check_guess_valid(current_guess):
                break
        self.history.append(current_guess)
        evaluation = self._check_guess_correct()
        render_result(evaluation)
        if sum([e.status=="GREEN" for e in evaluation]) == len(evaluation):
            return True
        else:
            return False

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="A Wordle implementation to test out some coding practices")
    parser.add_argument("--cheat", action="store_true", help="Tell the solution (for testing purposes)")
    args = parser.parse_args()

    print("Let's play wordle!")
    wordle = Wordle()
    if args.cheat:
        print(f"Correct word (for testing): {wordle.solution}")
    wordle.play()
