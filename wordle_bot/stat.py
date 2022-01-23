"""
Word List Statistics
====================
This script generates general statistics on word list which will be used to
sort the dictionary.
"""
from typing import List, Set

from prettytable import PrettyTable
import string

from wordle_bot import Bot

VOWELS: Set[str] = {"a", "e", "i", "o", "u"}


def generateHistogram(table: List[tuple[str, str, int]]) -> str:
    """ Generates a simple horizontal histogram string. """
    # Config
    barLength = 50 # Length of each histogram bars

    labelLength = max(len(label) for _, label, _ in table) + 1 # Max Label Size + 1
    maxCohortValue = max(value for _, _, value in table) # Used to scale values

    histogram = "" # Histogram output

    # Helpers
    padLabel = lambda label: label + " " * (labelLength - len(label))
    generateBar = lambda value: "#" * int((value / maxCohortValue) * barLength)

    for _, label, value in table:
        histogram += f"{padLabel(label)} | {generateBar(value)}\n"

    return histogram


def generateFormattedTable(table: List[tuple[str, str, int]]) -> PrettyTable:
    """ Returns a prettytable table. """
    prettyTable = PrettyTable()
    prettyTable.field_names = ["Category", "Count"]

    for _, label, value in table:
        prettyTable.add_row([label, value])

    return prettyTable


def wordsWithoutVowels(wordList: List[str]) -> int:
    """ Returns the count of words without vowels in them. """
    return sum(all(char not in VOWELS for char in word) for word in wordList)


def wordsWithChar(wordList: List[str], char: str) -> int:
    """ Returns the counts with words with the given character. """
    return sum(char in word for word in wordList)


def generateVowelTable(wordList: List[str]) -> List[tuple[str, str, int]]:
    """ Generates a tables of words with vowels count. """
    vowelTable = []
    vowelTable.append(("", "Words without vowels", wordsWithoutVowels(wordList)))
    for vowel in VOWELS:
        vowelTable.append((vowel, f"Words with '{vowel}'", wordsWithChar(wordList, vowel)))

    return vowelTable


def generateConsonantTable(wordList: List[str]) -> List[tuple[str, str, int]]:
    """ Generates a tables of words with consonant count. """
    consonantTable = []
    for char in string.ascii_lowercase:
        if char not in VOWELS:
            consonantTable.append((char, f"Words with '{char}'", wordsWithChar(wordList, char)))

    return consonantTable


def main() -> None:
    # Load word list
    wordList = Bot.loadWords()

    """
    Vowel Stats
    """
    vowelTable = generateVowelTable(wordList)
    print(generateFormattedTable(vowelTable))
    print(generateHistogram(vowelTable))

    """
    Consonant Stats
    """
    consonantTable = generateConsonantTable(wordList)
    print(generateFormattedTable(consonantTable))
    print(generateHistogram(consonantTable))


if __name__ == "__main__":
    main()
