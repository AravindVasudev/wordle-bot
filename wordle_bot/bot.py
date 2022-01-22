import time
from typing import List
from filelock import sys

from selenium import webdriver
from selenium.webdriver.common.by import By

from .constants import WORD_LIST_PATH, START_WORD, WORDLE_URL, DEFAULT_WAIT_SECONDS

class Bot:
    def __init__(self) -> None:
        self.wordList = Bot.loadWords()
        self.driver = webdriver.Chrome() # Chrome Web Driver

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
        # TODO: Add logic to support custom start word
        return self.wordList[0]

    def tryWord(self):
        pass

    def filterWords(self):
        pass

    def isDone(self):
        pass

    def run(self):
        # Goto wordle site
        self.driver.get(WORDLE_URL)
        
        # Close the instructions pop-up
        gameApp = self.driver.find_element(By.CSS_SELECTOR, "game-app") # Get <game-app>
        gameAppShadowRoot = self.driver.execute_script("return arguments[0].shadowRoot", gameApp)

        gameModal = gameAppShadowRoot.find_element(By.CSS_SELECTOR, "game-modal") # Get <game-modal>
        gameModalShadowRoot = self.driver.execute_script("return arguments[0].shadowRoot", gameModal)

        closeIcon = gameModalShadowRoot.find_element(By.CSS_SELECTOR, ".close-icon") # Get <div class="close-icon">
        closeIcon.click()

        # Play the game
        for attempt in range(6):
            self.tryWord() # try a word
            self.filterWords(attempt) # filter wordList

            if self.isDone(): # Check if done
                print("Yay!")
                time.sleep(DEFAULT_WAIT_SECONDS)
                return

        print("Nay :(")
        time.sleep(DEFAULT_WAIT_SECONDS)