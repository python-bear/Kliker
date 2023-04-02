import os
import pickle
import hashlib
import sys


if not os.path.exists('Data'):
    os.makedirs('Data')

if os.path.exists('App/klik_engine.py'):
    with open('App/klik_engine.py', 'rb') as file:
        file_hash = hashlib.sha256(file.read()).hexdigest()

with open('App/klik_anti_cheat.pkl', 'wb') as file:
    pickle.dump(file_hash, file)

sys.exit()
