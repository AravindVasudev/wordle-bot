"""
Word List Statistics
====================
This script generates general statistics on word list which will be used to
sort the dictionary.
"""
from typing import List, Set

from prettytable import PrettyTable

from wordle_bot import Bot

VOWELS: Set[str] = {"a", "e", "i", "o", "u"}

def generateHistogram(table: List[tuple[str, int]]) -> str:
    """ Generates a simple horizontal histogram string. """
    # Config
    barLength = 50 # Length of each histogram bars

    labelLength = max(len(label) for label, _ in table) + 1 # Max Label Size + 1
    maxCohortValue = max(value for _, value in table) # Used to scale values

    histogram = "" # Histogram output

    # Helpers
    padLabel = lambda label: label + " " * (labelLength - len(label))
    generateBar = lambda value: "#" * int((value / maxCohortValue) * barLength)

    for label, value in table:
        histogram += f"{padLabel(label)} | {generateBar(value)}\n"

    return histogram


def wordsWithoutVowels(wordList: List[str]) -> int:
    """ Returns the count of words without vowels in them. """
    return sum(all(char not in VOWELS for char in word) for word in wordList)


def wordsWithChar(wordList: List[str], char: str) -> int:
    """ Returns the counts with words with the given character. """
    return sum(char in word for word in wordList)


def main():
    # Load word list
    wordList = Bot.loadWords()

    vowelTable = []
    vowelTable.append(("Words without vowels", wordsWithoutVowels(wordList)))
    for vowel in VOWELS:
        vowelTable.append((f"Words with '{vowel}'", wordsWithChar(wordList, vowel)))

    # Formatted Output Table
    vowelOutputTable = PrettyTable()
    for label, value in vowelTable:
        vowelOutputTable.add_column(label, [value])

    print(vowelOutputTable)
    print(generateHistogram(vowelTable))


if __name__ == "__main__":
    main()