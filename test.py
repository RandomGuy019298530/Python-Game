import time
import sys


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.1)

print_slow('Welcome to the game, adventurer!')