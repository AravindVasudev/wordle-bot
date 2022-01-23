import argparse

from wordle_bot import Bot, stat, heuristic_sort

def main() -> None:
    """ Command Line Interface to run all scripts. """
    parser = argparse.ArgumentParser(description="Wordle Bot CLI. The bot plays the game when run with no args.")
    parser.add_argument("--stats", action="store_true", help="Generate word list stats")
    parser.add_argument("--heuristic-sort", action="store_true", help="Heuristically sort word list")
    
    args = parser.parse_args()
    if args.stats:
        stat.main()
    elif args.heuristic_sort:
        heuristic_sort.main()
    else:
        Bot().run()


if __name__ == "__main__":
    main()