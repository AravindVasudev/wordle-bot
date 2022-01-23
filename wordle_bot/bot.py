from dataclasses import dataclass, field
import enum
import time
from typing import List, Set

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from .constants import WORD_LIST_PATH, WORDLE_URL, DEFAULT_WAIT_SECONDS, GUESS_WAIT_SECONDS,WORD_SIZE


class TileState(str, enum.Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"


@dataclass
class GameState:
    """ Game State Object """
    # Yellow Guesses
    presentGuesses: Set[str] = field(default_factory=set)

    # Black Guesses
    absentGuesses: Set[str] = field(default_factory=set)

    # Green Guesses
    correctGuesses: List[str] = field(default_factory=lambda: [None] * WORD_SIZE)
    correctGuessSet: Set[str] = field(default_factory=set)

    def filter(self, word):
        """ returns true if the word is a legit guess else false """
        # TODO: Improve search to support repeated characters
        # Check for the green characters
        for pos, char in enumerate(self.correctGuesses):
            if char and char != word[pos]:
                return False

        # Check if word has all must haves and doesn't have any shouldn't haves
        wordSet = set(word)
        return self.presentGuesses <= wordSet and \
            not (self.absentGuesses & wordSet)


class Bot:
    def __init__(self) -> None:
        self.wordList = Bot.loadWords()
        self.gameState = GameState()
        self.isDone = False

        # Init Chrome Web Driver
        options = Options()
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(chrome_options=options)
        self.actions = ActionChains(self.driver)

        # TODO: Switch to explicit waits for finer control
        self.driver.implicitly_wait(DEFAULT_WAIT_SECONDS)

    def __del__(self) -> None:
        self.driver.close() # Close Chrome Web Driver

    @staticmethod
    def loadWords(wordListPath: str = WORD_LIST_PATH) -> List[str]:
        """ Loads and returns a list of words from `wordListPath` """
        with open(wordListPath) as file:
            return [line.strip() for line in file.readlines()]

    def nextWord(self):
        """ Returns the next eligible guess """
        return self.wordList.pop(0)

    def tryWord(self) -> str:
        nextWord = self.nextWord()
        self.actions.send_keys(nextWord)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()

        return nextWord

    def filterWords(self, attempt: int) -> None:
        # Get the current attempt results
        gameRow = self.gameBoard.find_elements(By.CSS_SELECTOR, "game-row")[attempt]
        gameRowShadowRoot = self.driver.execute_script("return arguments[0].shadowRoot", gameRow)

        # Update game state
        correctCount = 0
        for pos, tile in enumerate(gameRowShadowRoot.find_elements(By.CSS_SELECTOR, "game-tile")):
            state = tile.get_attribute("evaluation")
            letter = tile.get_attribute("letter")

            # TODO: Improve search to support repeated characters
            if state == "correct":
                self.gameState.correctGuesses[pos] = letter
                self.gameState.correctGuessSet.add(letter)
                
                correctCount += 1
            elif state == "present":
                self.gameState.presentGuesses.add(letter)
            elif letter not in self.gameState.correctGuessSet and letter not in self.gameState.presentGuesses:
                self.gameState.absentGuesses.add(letter)

        if correctCount == WORD_SIZE:
            self.isDone = True

        # Filter word List
        self.wordList = list(filter(self.gameState.filter, self.wordList))

    def run(self) -> None:
        # Goto wordle site
        self.driver.get(WORDLE_URL)
        
        # Close the instructions pop-up
        gameApp = self.driver.find_element(By.CSS_SELECTOR, "game-app") # Get <game-app>
        gameAppShadowRoot = self.driver.execute_script("return arguments[0].shadowRoot", gameApp)

        gameModal = gameAppShadowRoot.find_element(By.CSS_SELECTOR, "game-modal") # Get <game-modal>
        gameModalShadowRoot = self.driver.execute_script("return arguments[0].shadowRoot", gameModal)

        closeIcon = gameModalShadowRoot.find_element(By.CSS_SELECTOR, ".close-icon") # Get <div class="close-icon">
        closeIcon.click()

        # Get game board
        self.gameBoard = gameAppShadowRoot.find_element(By.CSS_SELECTOR, "#board") # Get <div id="board">

        # Play the game
        print(f"Initial Search space: {len(self.wordList)}")
        for attempt in range(6):
            # try a word
            guess = self.tryWord()

            # filter wordList
            self.filterWords(attempt) 
            print(f"Search space after {guess}: {len(self.wordList)}")

            # Check if done
            if self.isDone:
                print("Yay!")
                time.sleep(DEFAULT_WAIT_SECONDS)
                return

            # Wait between each attempt for animations to load
            time.sleep(GUESS_WAIT_SECONDS)

        print("Nay :(")
        time.sleep(DEFAULT_WAIT_SECONDS)