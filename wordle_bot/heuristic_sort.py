"""
Heuristic Sort
==============
This script uses the charcter distribution generated in stat.py to generate a
heuristic weight for each word in the word list and use that to sort the list.

Since bot.py reads the words in the order they are present in the word list,
we can simply pre-compute and store the list in this order.
"""

from typing import Dict, List

from . import Bot
from .constants import WORD_LIST_PATH
from .stat import generateVowelTable, generateConsonantTable


def writeToFile(wordList: List[str], file=WORD_LIST_PATH) -> None:
    """ Writes the wordList to the given file. """
    with open(file, "w") as f:
        for word in wordList:
            print(word, file=f)


class HeuristicWeight:
    """ Determines heuristic weight of a word. """
    def __init__(self, vowelTable: List[tuple[str, str, int]], consonantTable: List[tuple[str, str, int]]):
        self.vowelTable = vowelTable
        self.consonantTable = consonantTable
        self.vowelOrdering = HeuristicWeight.__computeOrdering(vowelTable)
        self.consonantOrdering = HeuristicWeight.__computeOrdering(consonantTable)

        # Helpers
        # Generates a key for sorted fn using vowel and consonant count.
        self.generateKey = lambda vowelOrder, consonantOrder: vowelOrder * 1000 + consonantOrder

    @staticmethod
    def __computeOrdering(table: List[tuple[str, str, int]]) -> Dict[str, int]:
        """ Generates orderind using weightage. """
        # TODO: Make the ordering relative, i.e., if x is 5 and y is 100, the
        # ordering should reflect that.
        return {entry[0]: pos for pos, entry in \
            enumerate(sorted(table, key=lambda x: x[2]))}

    def key(self, word: str) -> int:
        """ Comparison key method for ordering.  """
        vowelOrder, consonantOrder = 0, 0
        for vowel, order in self.vowelOrdering.items():
            if vowel in word:
                vowelOrder += order

        for consonant, order in self.consonantOrdering.items():
            if consonant in word:
                consonantOrder += order

        return self.generateKey(vowelOrder, consonantOrder)


def main():
    # Load word list
    wordList = Bot.loadWords()

    # Init heuristic weight
    heuristicWeight = HeuristicWeight(
        generateVowelTable(wordList),
        generateConsonantTable(wordList)
    )

    writeToFile(sorted(wordList, key=heuristicWeight.key, reverse=True))


if __name__ == "__main__":
    main()
