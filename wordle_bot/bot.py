from typing import List
from .constants import WORD_LIST_PATH, START_WORD

class Bot:
    def __init__(self) -> None:
        self.wordList = Bot.loadWords()

    @staticmethod
    def loadWords(wordListPath: str = WORD_LIST_PATH) -> List[str]:
        """ Loads and returns a list of words from `wordListPath` """
        with open(wordListPath) as file:
            return [line.strip() for line in file.readlines()]