from pickle import load as pickle_load
from sys import exit as sys_exit
import hashlib
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import quit as pygame_exit


def finish(pygame_quit=True):
    if pygame_quit:
        pygame_exit()
    sys_exit()


def encrypt(data):
    return hashlib.sha256(data).hexdigest()


def unpickle(pickled_file):
    try:
        unpickled_data = pickle_load(pickled_file)
        return unpickled_data

    except Exception as _error:
        return False
