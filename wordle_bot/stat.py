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
from wordle_bot.bot import GameState
from wordle_bot.constants import WORD_SIZE

VOWELS: Set[str] = {"a", "e", "i", "o", "u"}


def generateHistogram(table: List[tuple[str, str, int]]) -> str:
    """Generates a simple horizontal histogram string."""
    # Config
    barLength = 50  # Length of each histogram bars

    labelLength = max(len(label) for _, label, _ in table) + 1  # Max Label Size + 1
    maxCohortValue = max(value for _, _, value in table)  # Used to scale values

    histogram = ""  # Histogram output

    # Helpers
    padLabel = lambda label: label + " " * (labelLength - len(label))
    generateBar = lambda value: "#" * int((value / maxCohortValue) * barLength)

    for _, label, value in table:
        histogram += f"{padLabel(label)} | {generateBar(value)}\n"

    return histogram


def generateFormattedTable(table: List[tuple[str, str, int]]) -> PrettyTable:
    """Returns a prettytable table."""
    prettyTable = PrettyTable()
    prettyTable.field_names = ["Category", "Count"]

    for _, label, value in table:
        prettyTable.add_row([label, value])

    return prettyTable


def wordsWithoutVowels(wordList: List[str]) -> int:
    """Returns the count of words without vowels in them."""
    return sum(all(char not in VOWELS for char in word) for word in wordList)


def wordsWithChar(wordList: List[str], char: str) -> int:
    """Returns the counts with words with the given character."""
    return sum(char in word for word in wordList)


def generateVowelTable(wordList: List[str]) -> List[tuple[str, str, int]]:
    """Generates a tables of words with vowels count."""
    vowelTable = []
    vowelTable.append(("", "Words without vowels", wordsWithoutVowels(wordList)))
    for vowel in VOWELS:
        vowelTable.append(
            (vowel, f"Words with '{vowel}'", wordsWithChar(wordList, vowel))
        )

    return vowelTable


def generateGuessCountTable(wordList: List[str]) -> PrettyTable:
    """ Generates a table with guess count for all the words """
    prettyTable = PrettyTable()
    prettyTable.field_names = ["Word", "Guesses"]

    for word in wordList:
        words = list(wordList) # copy word list

        # Play the game
        gameState = GameState()
        for attempt in range(20): # Set to 20 to prevent hanging
            guess = words.pop(0) # Start with the first word

            # Update game state
            correctCount = 0
            for pos, letter in enumerate(guess):
                if letter == word[pos]: # Correct Guess
                    gameState.correctGuesses[pos] = letter
                    gameState.correctGuessSet.add(letter)

                    correctCount += 1
                elif letter in word: # Partial Guess
                    gameState.presentGuesses.add(letter)
                elif letter not in gameState.correctGuessSet and letter not in gameState.presentGuesses:
                    # Absent Guess
                    gameState.absentGuesses.add(letter)

            # If found, update states
            if correctCount == WORD_SIZE:
                prettyTable.add_row([word, attempt + 1])
                break

            # Prune words
            words = list(filter(gameState.filter, words))

    return prettyTable


def generateConsonantTable(wordList: List[str]) -> List[tuple[str, str, int]]:
    """Generates a tables of words with consonant count."""
    consonantTable = []
    for char in string.ascii_lowercase:
        if char not in VOWELS:
            consonantTable.append(
                (char, f"Words with '{char}'", wordsWithChar(wordList, char))
            )

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

    """
    Current Ordering Guess Stats
    """
    with open("words_guess.txt", "w") as file:
        print(generateGuessCountTable(wordList), file=file)


if __name__ == "__main__":
    main()
