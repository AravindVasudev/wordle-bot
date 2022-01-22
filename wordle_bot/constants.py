import os

WORD_LIST_PATH = os.path.normpath("./words.txt")
WORDLE_URL = "https://www.powerlanguage.co.uk/wordle/"
START_WORD = "adieu"
DEFAULT_WAIT_SECONDS = 10 # Selenium load wait time
GUESS_WAIT_SECONDS = 2 # Wait time between each guess
WORD_SIZE = 5