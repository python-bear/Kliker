import pickle
import pygame
import os
import sys
import hashlib


# Exit function
def finish(pygame_quit=True):
    # Quit program
    if pygame_quit:
        pygame.quit()
    sys.exit()


# Encrypt function
def encrypt(data):
    return hashlib.sha256(data).hexdigest()


# Unpickling function
def unpickle(pickled_file):
    try:
        unpickled_data = pickle.load(pickled_file)
        return unpickled_data

    except Exception as _error:
        return False  # should call cheater alert
